import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from backend.book_dao import add_book, get_books, delete_book, update_book, search_books


def book_screen(root):
    win = tk.Toplevel(root)
    win.title("Books Management")
    win.geometry("900x600")
    win.minsize(900, 600)
    win.resizable(True, True)

    # ================= BACKGROUND =================
    original_img = Image.open("images/books.jpg")

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
        text="BOOK MANAGEMENT",
        font=("Arial", 22, "bold"),
        bg="black",
        fg="gold"
    ).grid(row=0, column=0, columnspan=3, pady=20)

    # ================= LABELS + ENTRIES =================
    tk.Label(frame, text="Title", font=("Arial", 14, "bold"),
             bg="black", fg="white").grid(row=1, column=0, padx=15, pady=8, sticky="e")

    title = tk.Entry(frame, width=25, font=("Arial", 12))
    title.grid(row=1, column=1, pady=8)

    tk.Label(frame, text="Author", font=("Arial", 14, "bold"),
             bg="black", fg="white").grid(row=2, column=0, padx=15, pady=8, sticky="e")

    author = tk.Entry(frame, width=25, font=("Arial", 12))
    author.grid(row=2, column=1, pady=8)

    tk.Label(frame, text="ISBN", font=("Arial", 14, "bold"),
             bg="black", fg="white").grid(row=3, column=0, padx=15, pady=8, sticky="e")

    isbn = tk.Entry(frame, width=25, font=("Arial", 12))
    isbn.grid(row=3, column=1, pady=8)

    tk.Label(frame, text="Book ID", font=("Arial", 14, "bold"),
             bg="black", fg="white").grid(row=4, column=0, padx=15, pady=8, sticky="e")

    book_id = tk.Entry(frame, width=25, font=("Arial", 12))
    book_id.grid(row=4, column=1, pady=8)

    tk.Label(frame, text="Search", font=("Arial", 14, "bold"),
             bg="black", fg="white").grid(row=5, column=0, padx=15, pady=8, sticky="e")

    search_entry = tk.Entry(frame, width=25, font=("Arial", 12))
    search_entry.grid(row=5, column=1, pady=8)

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
        columns=("ID", "Title", "Author", "ISBN", "Available"),
        show="headings",
        height=10
    )

    tree.heading("ID", text="ID", anchor="center")
    tree.heading("Title", text="Title", anchor="center")
    tree.heading("Author", text="Author", anchor="center")
    tree.heading("ISBN", text="ISBN", anchor="center")
    tree.heading("Available", text="Available", anchor="center")

    tree.column("ID", width=50, anchor="center")
    tree.column("Title", width=180, anchor="center")
    tree.column("Author", width=180, anchor="center")
    tree.column("ISBN", width=100, anchor="center")
    tree.column("Available", width=100, anchor="center")

    tree.grid(row=6, column=0, columnspan=3, padx=10, pady=20)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=6, column=3, sticky="ns")

    # ================= FUNCTIONS =================
    def clear_fields():
        title.delete(0, tk.END)
        author.delete(0, tk.END)
        isbn.delete(0, tk.END)
        book_id.delete(0, tk.END)
        search_entry.delete(0, tk.END)

    def refresh():
        for item in tree.get_children():
            tree.delete(item)

        for row in get_books():
            status = "Yes" if row[4] == 1 else "No"
            tree.insert("", tk.END,
                        values=(row[0], row[1], row[2], row[3], status))

    def add():
        if title.get() == "" or author.get() == "" or isbn.get() == "":
            messagebox.showerror("Error", "All fields required", parent=win)
            return

        add_book(title.get(), author.get(), isbn.get())
        messagebox.showinfo("Success", "Book Added", parent=win)
        refresh()
        clear_fields()

    def delete():
        if book_id.get() == "":
            messagebox.showerror("Error", "Enter Book ID", parent=win)
            return

        delete_book(int(book_id.get()))
        messagebox.showinfo("Success", "Book Deleted", parent=win)
        refresh()
        clear_fields()

    def update():
        if book_id.get() == "":
            messagebox.showerror("Error", "Enter Book ID", parent=win)
            return

        update_book(
            int(book_id.get()),
            title.get(),
            author.get(),
            isbn.get()
        )

        messagebox.showinfo("Success", "Book Updated", parent=win)
        refresh()
        clear_fields()

    def view():
        refresh()

    def search():
        keyword = search_entry.get()

        if keyword == "":
            messagebox.showerror("Error", "Enter search value", parent=win)
            return

        for item in tree.get_children():
            tree.delete(item)

        for row in search_books(keyword):
            status = "Yes" if row[4] == 1 else "No"
            tree.insert("", tk.END,
                        values=(row[0], row[1], row[2], row[3], status))

    # ================= BUTTONS =================
    tk.Button(frame, text="ADD", width=14,
              bg="skyblue", font=("Arial", 12, "bold"),
              command=add).grid(row=1, column=2, padx=15)

    tk.Button(frame, text="VIEW", width=14,
              bg="white", font=("Arial", 12, "bold"),
              command=view).grid(row=2, column=2)

    tk.Button(frame, text="DELETE", width=14,
              bg="salmon", font=("Arial", 12, "bold"),
              command=delete).grid(row=3, column=2)

    tk.Button(frame, text="UPDATE", width=14,
              bg="lightgreen", font=("Arial", 12, "bold"),
              command=update).grid(row=4, column=2)

    tk.Button(frame, text="SEARCH", width=14,
              bg="khaki", font=("Arial", 12, "bold"),
              command=search).grid(row=5, column=2)