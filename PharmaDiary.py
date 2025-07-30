import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, UnidentifiedImageError
import sqlite3
import time
<<<<<<< HEAD
=======
import random
import math
>>>>>>> 5e41f14 (Add PharmaDiary 60% development with animations and UI improvements)

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
<<<<<<< HEAD
root.geometry("1000x800") 
root.minsize(1000, 800)
=======
root.geometry("1000x800")
>>>>>>> 5e41f14 (Add PharmaDiary 60% development with animations and UI improvements)
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
<<<<<<< HEAD
    radius_x = 30
    radius_y = 14
    for y in range(y_start, y_end, spacing):
        canvas.create_oval(
            x_left - radius_x, y - radius_y,
            x_left + radius_x, y + radius_y,
=======
    for y in range(y_start, y_end, spacing):
        canvas.create_oval(
            x_left - 30, y - 14, x_left + 30, y + 14,
>>>>>>> 5e41f14 (Add PharmaDiary 60% development with animations and UI improvements)
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
<<<<<<< HEAD

    frame = tk.Frame(dialog, bg="#b596bb")
    frame.pack(fill="both", expand=True)

    label = tk.Label(frame, text=message, font=("Arial", 30), bg="#b596bb", fg="white")
    label.pack(pady=100)

    btn = tk.Button(frame, text="OK", font=("Arial", 20), bg="#541760", fg="white",
                    activebackground="#3e0544", activeforeground="white", command=dialog.destroy)
    btn.pack(pady=50)

=======
    frame = tk.Frame(dialog, bg="#b596bb")
    frame.pack(fill="both", expand=True)
    label = tk.Label(frame, text=message, font=("Arial", 30), bg="#b596bb", fg="white")
    label.pack(pady=100)
    btn = tk.Button(frame, text="OK", font=("Arial", 20), bg="#541760", fg="white",
                    activebackground="#3e0544", activeforeground="white", command=dialog.destroy)
    btn.pack(pady=50)
>>>>>>> 5e41f14 (Add PharmaDiary 60% development with animations and UI improvements)
    dialog.wait_window()

def add_medicine():
    name = med_name.get()
    time_ = med_time.get()
<<<<<<< HEAD
    if name and time_:
=======
    if name and time_ and name != "Medicine Name" and time_ != "Time (e.g. 08:00 PM)":
>>>>>>> 5e41f14 (Add PharmaDiary 60% development with animations and UI improvements)
        cursor.execute("INSERT INTO medicines (name, time) VALUES (?, ?)", (name, time_))
        conn.commit()
        show_custom_dialog("Saved", f"{name} scheduled at {time_}")
        med_name.delete(0, tk.END)
        med_time.delete(0, tk.END)
    else:
<<<<<<< HEAD
        show_custom_dialog("Input Error", "Please enter all fields")
=======
        show_custom_dialog("Input Error", "Please enter all fields correctly.")

def view_medicines():
    view_win = tk.Toplevel(root)
    view_win.title("Your Medicine List")
    view_win.geometry("600x500")
    view_win.configure(bg="#ede6f2")
    tk.Label(view_win, text="Saved Medicines", font=("Arial", 24, "bold"), bg="#ede6f2", fg="#4a0072").pack(pady=20)
    list_frame = tk.Frame(view_win, bg="#ede6f2")
    list_frame.pack(expand=True, fill="both", padx=20, pady=10)
    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side="right", fill="y")
    text = tk.Text(list_frame, font=("Arial", 14), yscrollcommand=scrollbar.set, bg="#faf3fc", fg="black")
    text.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=text.yview)
    cursor.execute("SELECT name, time FROM medicines")
    entries = cursor.fetchall()
    if not entries:
        text.insert("end", "No medicines added yet.\n")
    else:
        for idx, (name, time_) in enumerate(entries, 1):
            text.insert("end", f"{idx}. {name} ➤ {time_}\n")
    text.config(state="disabled")

def delete_medicine():
    del_win = tk.Toplevel(root)
    del_win.title("Delete Medicine")
    del_win.geometry("600x500")
    del_win.configure(bg="#fff0f7")
    tk.Label(del_win, text="Select Medicine to Delete", font=("Arial", 20), bg="#fff0f7", fg="#4a0072").pack(pady=20)
    listbox = tk.Listbox(del_win, font=("Arial", 14), width=50, height=15)
    listbox.pack(pady=10)
    cursor.execute("SELECT id, name, time FROM medicines")
    rows = cursor.fetchall()
    for row in rows:
        listbox.insert(tk.END, f"{row[0]} ➤ {row[1]} at {row[2]}")
    def delete_selected():
        selection = listbox.curselection()
        if selection:
            item = listbox.get(selection[0])
            med_id = int(item.split("➤")[0].strip())
            cursor.execute("DELETE FROM medicines WHERE id=?", (med_id,))
            conn.commit()
            listbox.delete(selection[0])
            show_custom_dialog("Deleted", "Medicine deleted successfully.")
    tk.Button(del_win, text="Delete Selected", font=("Arial", 14), command=delete_selected,
              bg="#7a1f56", fg="white", activebackground="#4a0044", width=20).pack(pady=10)
>>>>>>> 5e41f14 (Add PharmaDiary 60% development with animations and UI improvements)

def animate_molecule():
    for i in range(30):
        canvas.move(dot, 10, 0)
        root.update()
        time.sleep(0.05)

<<<<<<< HEAD
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
=======
def simulate_drug_pathway():
    canvas.delete("all")
    canvas.configure(bg="#e5f9ff")
    canvas.create_text(500, 60, text="Drug Action Pathway", font=("Arial", 28, "bold"), fill="#00334d")
    pathway = []
    for i in range(30):
        angle = i * 0.2
        x = 100 + int(10 * i + 40 * math.sin(angle))
        y = 150 + int(30 * math.cos(angle))
        dot = canvas.create_oval(x, y, x+15, y+15, fill="#00ccff", outline="")
        pathway.append(dot)
    target = canvas.create_oval(800, 300, 850, 350, fill="#ff4444", outline="#770000", width=3)
    canvas.create_text(825, 355, text="Receptor", font=("Arial", 10), fill="#aa0000")
    def move_molecule(step=0):
        if step >= len(pathway):
            bind_animation()
            return
        for i in range(step):
            canvas.itemconfig(pathway[i], fill="#007799")
        root.after(50, lambda: move_molecule(step + 1))
    def bind_animation():
        for i in range(4):
            canvas.after(i * 200, lambda: canvas.itemconfig(target, fill="#ffff00" if i % 2 == 0 else "#ff4444"))
        root.after(1000, cascade_signaling)
    def cascade_signaling():
        for i in range(6):
            y = 400 + i * 30
            canvas.create_oval(820, y, 840, y + 20, fill="#009900", outline="white")
        show_custom_dialog("Simulation Complete", "Drug has bound and signal cascade started.")
    move_molecule()

def load_main_interface():
    if bg_id:
        canvas.itemconfig(bg_id, state="normal")
    else:
        canvas.configure(bg="#c2afc6")
    global med_name, med_time
    title = tk.Label(root, text="PharmaDiary 💊", font=("Arial", 36, "bold"), bg="#b596bb", fg="#4a0072")
    canvas.create_window(500, 80, window=title)
    med_name = tk.Entry(root, width=40, font=("Arial", 24), bg="#b596bb")
    med_name.insert(0, "Medicine Name")
    med_time = tk.Entry(root, width=40, font=("Arial", 24), bg="#b596bb")
    med_time.insert(0, "Time (e.g. 08:00 PM)")
    def clear_placeholder(e, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")
    def set_placeholder(e, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="gray")
    med_name.bind("<FocusIn>", lambda e: clear_placeholder(e, med_name, "Medicine Name"))
    med_name.bind("<FocusOut>", lambda e: set_placeholder(e, med_name, "Medicine Name"))
    med_time.bind("<FocusIn>", lambda e: clear_placeholder(e, med_time, "Time (e.g. 08:00 PM)"))
    med_time.bind("<FocusOut>", lambda e: set_placeholder(e, med_time, "Time (e.g. 08:00 PM)"))
    med_name.config(fg="gray")
    med_time.config(fg="gray")
    canvas.create_window(500, 180, window=med_name)
    canvas.create_window(500, 260, window=med_time)
    canvas.create_window(500, 340, window=tk.Button(root, text="Add to Diary", command=add_medicine,
        bg="#541760", fg="white", font=("Arial", 20), width=20))
    global dot
    canvas_main = tk.Canvas(root, width=700, height=150, bg="white")
    canvas.create_window(500, 460, window=canvas_main)
    dot = canvas_main.create_oval(30, 60, 70, 100, fill="#3e0544")
    canvas.create_window(500, 620, window=tk.Button(root, text="Simulate Binding", command=animate_molecule,
        bg="#541760", fg="white", font=("Arial", 20), width=20))
    canvas.create_window(500, 670, window=tk.Button(root, text="Simulate Medicine Animation", command=simulate_drug_pathway,
        bg="#A774BA", fg="white", font=("Arial", 18), width=30))
    canvas.create_window(500, 720, window=tk.Button(root, text="View Saved Medicines", command=view_medicines,
        bg="#541760", fg="white", font=("Arial", 18), width=25))
    canvas.create_window(150, 760, window=tk.Button(root, text="Delete Medicine", command=delete_medicine,
        bg="#882244", fg="white", font=("Arial", 16), width=15))
    canvas.create_window(900, 760, window=tk.Button(root, text="Exit", command=root.destroy,
        bg="gray30", fg="white", font=("Arial", 16), width=10))
>>>>>>> 5e41f14 (Add PharmaDiary 60% development with animations and UI improvements)

flip_polygon = None
shadow_polygon = None

def flip_animation(step=0):
    global flip_polygon, shadow_polygon
<<<<<<< HEAD

=======
>>>>>>> 5e41f14 (Add PharmaDiary 60% development with animations and UI improvements)
    if flip_polygon:
        canvas.delete(flip_polygon)
    if shadow_polygon:
        canvas.delete(shadow_polygon)
    canvas.delete("flip_page")
    canvas.delete("cover")
<<<<<<< HEAD

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

=======
    draw_diary_cover()
    max_step = 80
    if step > max_step:
        canvas.delete("all")
        if bg_id:
            canvas.itemconfig(bg_id, state="normal")
        load_main_interface()
        return
    left_x = 200
    right_x = 200 + (step * 8)
    fold_x = left_x + (right_x - left_x) * 0.7
    points = [(left_x, 140), (right_x, 140), (right_x, 660), (left_x, 660)]
    fold_points = [(fold_x, 140), (right_x, 140), (right_x, 660), (fold_x, 660)]
    flip_polygon = canvas.create_polygon(points, fill="white", outline="gray20", width=3, tags="flip_page")
    shadow_polygon = canvas.create_polygon(fold_points, fill="#bbbbbb", outline="gray40", width=2,
                                           stipple="gray50", tags="flip_page")
>>>>>>> 5e41f14 (Add PharmaDiary 60% development with animations and UI improvements)
    root.after(20, lambda: flip_animation(step + 1))

draw_diary_cover()
flip_animation()
<<<<<<< HEAD

=======
>>>>>>> 5e41f14 (Add PharmaDiary 60% development with animations and UI improvements)
root.mainloop()
