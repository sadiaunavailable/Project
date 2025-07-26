import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, UnidentifiedImageError
import sqlite3
import time

conn = sqlite3.connect('pharmadiary.db')
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        time TEXT NOT NULL
    )
""")
conn.commit()

root = tk.Tk()
root.title("PharmaDiary")
root.geometry("1000x800") 
root.minsize(1000, 800)
root.resizable(False, False)

canvas = tk.Canvas(root, width=1000, height=800, highlightthickness=0)
canvas.pack(fill="both", expand=True)

try:
    bg_img = Image.open("medicine_bg.png")
    bg_img = bg_img.resize((1000, 800))
    bg_img_tk = ImageTk.PhotoImage(bg_img)
    bg_id = canvas.create_image(0, 0, anchor="nw", image=bg_img_tk)
    canvas.itemconfig(bg_id, state="hidden")
except (FileNotFoundError, UnidentifiedImageError):
    bg_img_tk = None
    bg_id = None
    canvas.configure(bg="#e0e0e0")

def draw_spiral_binding(x_left=200, y_start=150, y_end=650, spacing=30):
    radius_x = 30
    radius_y = 14
    for y in range(y_start, y_end, spacing):
        canvas.create_oval(
            x_left - radius_x, y - radius_y,
            x_left + radius_x, y + radius_y,
            fill="", outline="black", width=3, tags="cover"
        )

def draw_diary_cover():
    canvas.create_rectangle(200, 140, 800, 660, fill="#5e1668", outline="#5c1caa", width=6, tags="cover")
    draw_spiral_binding()
    canvas.create_oval(460, 300, 540, 340, fill="#afb2b4", outline="#000", tags="cover")
    canvas.create_line(500, 300, 500, 340, fill="#5F2866", width=4, tags="cover")
    canvas.create_text(500, 400, text="PharmaDiary 💊", font=("Helvetica", 40, "bold"), fill="white", tags="cover")

def show_custom_dialog(title, message):
    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.geometry("1000x800")
    dialog.transient(root)
    dialog.grab_set()

    frame = tk.Frame(dialog, bg="#b596bb")
    frame.pack(fill="both", expand=True)

    label = tk.Label(frame, text=message, font=("Arial", 30), bg="#b596bb", fg="white")
    label.pack(pady=100)

    btn = tk.Button(frame, text="OK", font=("Arial", 20), bg="#541760", fg="white",
                    activebackground="#3e0544", activeforeground="white", command=dialog.destroy)
    btn.pack(pady=50)

    dialog.wait_window()

def add_medicine():
    name = med_name.get()
    time_ = med_time.get()
    if name and time_:
        cursor.execute("INSERT INTO medicines (name, time) VALUES (?, ?)", (name, time_))
        conn.commit()
        show_custom_dialog("Saved", f"{name} scheduled at {time_}")
        med_name.delete(0, tk.END)
        med_time.delete(0, tk.END)
    else:
        show_custom_dialog("Input Error", "Please enter all fields")

def animate_molecule():
    for i in range(30):
        canvas.move(dot, 10, 0)
        root.update()
        time.sleep(0.05)

def load_main_interface():
    if bg_id is not None:
        canvas.itemconfig(bg_id, state="normal")
    else:
        canvas.configure(bg="#c2afc6")

    title = tk.Label(root, text="PharmaDiary 💊", font=("Arial", 36, "bold"),
                     bg="#b596bb" if bg_id is None else "#b596bb", fg="#4a0072")
    canvas.create_window(500, 80, window=title)

    global med_name, med_time
    med_name = tk.Entry(root, width=40, font=("Arial", 24), bg="#b596bb", fg="black")
    med_name.insert(0, "Medicine Name")
    canvas.create_window(500, 180, window=med_name)

    med_time = tk.Entry(root, width=40, font=("Arial", 24), bg="#b596bb", fg="black")
    med_time.insert(0, "Time (e.g. 08:00 PM)")
    canvas.create_window(500, 260, window=med_time)

    add_btn = tk.Button(root, text="Add to Diary", command=add_medicine,
                        bg="#541760", fg="white", font=("Arial", 20),
                        activebackground="#3e0544", activeforeground="white", width=20)
    canvas.create_window(500, 340, window=add_btn)

    global dot
    canvas_main = tk.Canvas(root, width=700, height=150, bg="white")
    canvas.create_window(500, 460, window=canvas_main)
    dot = canvas_main.create_oval(30, 60, 70, 100, fill="skyblue")

    sim_btn = tk.Button(root, text="Simulate Binding", command=animate_molecule,
                        bg="#541760", fg="white", font=("Arial", 20),
                        activebackground="#3e0544", activeforeground="white", width=20)
    canvas.create_window(500, 620, window=sim_btn)

flip_polygon = None
shadow_polygon = None

def flip_animation(step=0):
    global flip_polygon, shadow_polygon

    if flip_polygon:
        canvas.delete(flip_polygon)
    if shadow_polygon:
        canvas.delete(shadow_polygon)
    canvas.delete("flip_page")
    canvas.delete("cover")

    draw_diary_cover()

    max_step = 80
    if step > max_step:
        canvas.delete("all")
        if bg_id is not None:
            canvas.itemconfig(bg_id, state="normal")
        load_main_interface()
        return

    left_x = 200
    right_x = 200 + (step * 8)

    fold_x = left_x + (right_x - left_x) * 0.7

    points = [
        (left_x, 140),
        (right_x, 140),
        (right_x, 660),
        (left_x, 660)
    ]

    fold_points = [
        (fold_x, 140),
        (right_x, 140),
        (right_x, 660),
        (fold_x, 660)
    ]

    flip_polygon = canvas.create_polygon(points, fill="white", outline="gray20", width=3, tags="flip_page")
    shadow_polygon = canvas.create_polygon(fold_points, fill="#bbbbbb", outline="gray40", width=2, stipple="gray50", tags="flip_page")

    root.after(20, lambda: flip_animation(step + 1))

draw_diary_cover()
flip_animation()

root.mainloop()
