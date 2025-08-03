import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, UnidentifiedImageError
import sqlite3
import time
import math

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
    for y in range(y_start, y_end, spacing):
        canvas.create_oval(
            x_left - 30, y - 14, x_left + 30, y + 14,
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
    if name and time_ and name != "Medicine Name" and time_ != "Time (e.g. 08:00 PM)":
        cursor.execute("INSERT INTO medicines (name, time) VALUES (?, ?)", (name, time_))
        conn.commit()
        show_custom_dialog("Saved", f"{name} scheduled at {time_}")
        med_name.delete(0, tk.END)
        med_time.delete(0, tk.END)
    else:
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
            text.insert("end", f"{idx}. {name} ➔ {time_}\n")
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
        listbox.insert(tk.END, f"{row[0]} ➔ {row[1]} at {row[2]}")
    def delete_selected():
        selection = listbox.curselection()
        if selection:
            item = listbox.get(selection[0])
            med_id = int(item.split("\u2794")[0].strip())
            cursor.execute("DELETE FROM medicines WHERE id=?", (med_id,))
            conn.commit()
            listbox.delete(selection[0])
            show_custom_dialog("Deleted", "Medicine deleted successfully.")
    tk.Button(del_win, text="Delete Selected", font=("Arial", 14), command=delete_selected,
              bg="#7a1f56", fg="white", activebackground="#4a0044", width=20).pack(pady=10)

def simulate_drug_pathway():
    canvas.delete("all")
    canvas.configure(bg="#e5f9ff")
    canvas.create_text(500, 60, text="Drug Action Pathway", font=("Arial", 28, "bold"), fill="#00334d")

    dna_points1 = []
    dna_points2 = []
    for i in range(60):
        x = 100 + i * 12
        y1 = 250 + 40 * math.sin(i * 0.3)
        y2 = 250 + 40 * math.sin(i * 0.3 + math.pi)
        dna_points1.append((x, y1))
        dna_points2.append((x, y2))

    for i in range(len(dna_points1) - 1):
        x1, y1 = dna_points1[i]
        x2, y2 = dna_points1[i+1]
        canvas.create_line(x1, y1, x2, y2, fill="#0077cc", width=2)
        x1b, y1b = dna_points2[i]
        x2b, y2b = dna_points2[i+1]
        canvas.create_line(x1b, y1b, x2b, y2b, fill="#0077cc", width=2)
        if i % 3 == 0:
            canvas.create_line(x1, y1, x1b, y1b, fill="#a0a0a0", width=1)

    receptor_x, receptor_y = dna_points1[-1][0] + 60, 250
    receptor = canvas.create_oval(receptor_x - 30, receptor_y - 30, receptor_x + 30, receptor_y + 30,
                                 fill="#ff4444", outline="#770000", width=3)
    canvas.create_text(receptor_x, receptor_y + 50, text="Receptor", font=("Arial", 14, "bold"), fill="#aa0000")

    molecule = canvas.create_oval(0, 0, 20, 20, fill="#00ccff", outline="#005577")
    label = canvas.create_text(0, 0, text=med_name.get() or "Medicine", font=("Arial", 12, "bold"), fill="#004466")

    def move_molecule(step=0):
        if step >= len(dna_points1):
            binding_animation()
            return
        x, y = dna_points1[step]
        x_b, y_b = dna_points2[step]

        if step % 2 == 0:
            canvas.coords(molecule, x - 10, y - 10, x + 10, y + 10)
            canvas.coords(label, x, y - 20)
        else:
            canvas.coords(molecule, x_b - 10, y_b - 10, x_b + 10, y_b + 10)
            canvas.coords(label, x_b, y_b - 20)

        if step > 0:
            prev = canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="#00ccff", outline="", stipple="gray50")
            canvas.after(300, lambda p=prev: canvas.delete(p))

        root.after(50, lambda: move_molecule(step + 1))

    def binding_animation():
        def flash(i=0):
            if i > 5:
                ripple_wave()
                return
            color = "#ffff00" if i % 2 == 0 else "#ff4444"
            canvas.itemconfig(receptor, fill=color)
            root.after(200, lambda: flash(i + 1))
        flash()

    def ripple_wave():
        rings = []
        def create_ring(r=1):
            ring = canvas.create_oval(receptor_x - 30 - r*10, receptor_y - 30 - r*10,
                                      receptor_x + 30 + r*10, receptor_y + 30 + r*10,
                                      outline="#ffcc00", width=2)
            rings.append(ring)
            canvas.after(500, lambda: canvas.delete(ring))
        for i in range(1, 5):
            canvas.after(i * 250, lambda r=i: create_ring(r))
        root.after(2000, gene_activation)

    def gene_activation():
        bars = []
        for i in range(6):
            y = receptor_y + 80 + i * 25
            bar = canvas.create_rectangle(receptor_x - 15, y, receptor_x + 15, y + 15,
                                         fill="#00cc66", outline="#003322")
            bars.append(bar)
        pulse_step = 0
        def pulse():
            nonlocal pulse_step
            if pulse_step > 10:
                show_custom_dialog("Simulation Complete", f"{med_name.get() or 'Medicine'} has bound and activated genes!")
                return
            for idx, bar in enumerate(bars):
                if (pulse_step + idx) % 2 == 0:
                    canvas.itemconfig(bar, fill="#00ff88")
                else:
                    canvas.itemconfig(bar, fill="#00cc66")
            pulse_step += 1
            root.after(300, pulse)
        pulse()

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

def animate_molecule():
    for i in range(30):
        canvas.move(dot, 10, 0) # type: ignore
        root.update()
        time.sleep(0.05)

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
    root.after(20, lambda: flip_animation(step + 1))

draw_diary_cover()
flip_animation()
root.mainloop()
