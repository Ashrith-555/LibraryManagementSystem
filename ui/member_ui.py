import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from backend.member_dao import add_member, get_members, update_member, delete_member


def member_screen(root):
    win = tk.Toplevel(root)
    win.title("Member Management")
    win.geometry("900x600")
    win.minsize(900, 600)
    win.resizable(True, True)

    # ================= BACKGROUND =================
    original_img = Image.open("images/members.jpg")

    bg_label = tk.Label(win)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def resize_bg(event=None):
        width = win.winfo_width()
        height = win.winfo_height()

        resized = original_img.resize((width, height))
        bg = ImageTk.PhotoImage(resized)

        bg_label.config(image=bg)
        bg_label.image = bg

    win.after(100, resize_bg)
    win.bind("<Configure>", resize_bg)

    # ================= MAIN FRAME =================
    frame = tk.Frame(win, bg="black", bd=2, relief="solid")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # ================= TITLE =================
    tk.Label(
        frame,
        text="MEMBER MANAGEMENT",
        font=("Arial", 22, "bold"),
        bg="black",
        fg="gold"
    ).grid(row=0, column=0, columnspan=3, pady=20)

    # ================= LABELS + ENTRIES =================
    tk.Label(frame, text="Name", font=("Arial", 14, "bold"),
             bg="black", fg="white").grid(row=1, column=0, padx=15, pady=10, sticky="e")

    name = tk.Entry(frame, width=25, font=("Arial", 12))
    name.grid(row=1, column=1, pady=10)

    tk.Label(frame, text="Phone", font=("Arial", 14, "bold"),
             bg="black", fg="white").grid(row=2, column=0, padx=15, pady=10, sticky="e")

    phone = tk.Entry(frame, width=25, font=("Arial", 12))
    phone.grid(row=2, column=1, pady=10)

    tk.Label(frame, text="Member ID", font=("Arial", 14, "bold"),
             bg="black", fg="white").grid(row=3, column=0, padx=15, pady=10, sticky="e")

    member_id = tk.Entry(frame, width=25, font=("Arial", 12))
    member_id.grid(row=3, column=1, pady=10)

    # ================= TABLE STYLE =================
    style = ttk.Style()
    style.theme_use("default")

    style.configure(
        "Treeview",
        background="white",
        foreground="black",
        rowheight=28,
        fieldbackground="white",
        font=("Arial", 10)
    )

    style.configure(
        "Treeview.Heading",
        font=("Arial", 11, "bold"),
        relief="flat"
    )

    style.map(
        "Treeview",
        background=[("selected", "#4a90e2")],
        foreground=[("selected", "white")]
    )

    # ================= TREEVIEW =================
    tree = ttk.Treeview(
        frame,
        columns=("ID", "Name", "Phone"),
        show="headings",
        height=10
    )

    tree.heading("ID", text="ID", anchor="center")
    tree.heading("Name", text="Name", anchor="center")
    tree.heading("Phone", text="Phone", anchor="center")

    tree.column("ID", width=80, anchor="center")
    tree.column("Name", width=220, anchor="center")
    tree.column("Phone", width=180, anchor="center")

    tree.grid(row=5, column=0, columnspan=3, padx=10, pady=20)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=5, column=3, sticky="ns")

    # ================= FUNCTIONS =================
    def clear_fields():
        name.delete(0, tk.END)
        phone.delete(0, tk.END)
        member_id.delete(0, tk.END)

    def refresh():
        for item in tree.get_children():
            tree.delete(item)

        for row in get_members():
            tree.insert("", tk.END, values=row)

    def add():
        if name.get() == "" or phone.get() == "":
            messagebox.showerror("Error", "All fields required", parent=win)
            return

        add_member(name.get(), phone.get())
        messagebox.showinfo("Success", "Member Added", parent=win)
        refresh()
        clear_fields()

    def update():
        if member_id.get() == "":
            messagebox.showerror("Error", "Enter Member ID", parent=win)
            return

        update_member(
            int(member_id.get()),
            name.get(),
            phone.get()
        )

        messagebox.showinfo("Success", "Member Updated", parent=win)
        refresh()
        clear_fields()

    def delete():
        if member_id.get() == "":
            messagebox.showerror("Error", "Enter Member ID", parent=win)
            return

        delete_member(int(member_id.get()))
        messagebox.showinfo("Success", "Member Deleted", parent=win)
        refresh()
        clear_fields()

    def view():
        refresh()

    # ================= BUTTONS =================
    tk.Button(frame, text="ADD", width=14,
              bg="skyblue", font=("Arial", 12, "bold"),
              command=add).grid(row=1, column=2, padx=15)

    tk.Button(frame, text="VIEW", width=14,
              bg="white", font=("Arial", 12, "bold"),
              command=view).grid(row=2, column=2)

    tk.Button(frame, text="UPDATE", width=14,
              bg="lightgreen", font=("Arial", 12, "bold"),
              command=update).grid(row=3, column=2)

    tk.Button(frame, text="DELETE", width=14,
              bg="salmon", font=("Arial", 12, "bold"),
              command=delete).grid(row=4, column=2)