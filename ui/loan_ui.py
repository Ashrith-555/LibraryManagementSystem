import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from backend.loan_dao import borrow_book, return_book


def loan_screen(root):
    win = tk.Toplevel(root)
    win.title("Loan Management")
    win.geometry("900x600")
    win.minsize(900, 600)
    win.resizable(True, True)

    # ================= BACKGROUND =================
    original_img = Image.open("images/borrow.jpg")

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

    # ================= CENTER FRAME =================
    frame = tk.Frame(win, bg="black", bd=2, relief="solid")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # ================= TITLE =================
    tk.Label(
        frame,
        text="LOAN MANAGEMENT",
        font=("Arial", 22, "bold"),
        bg="black",
        fg="gold"
    ).grid(row=0, column=0, columnspan=2, pady=20)

    # ================= LABELS =================
    tk.Label(
        frame,
        text="Book ID",
        font=("Arial", 14, "bold"),
        bg="black",
        fg="white"
    ).grid(row=1, column=0, padx=20, pady=15, sticky="e")

    book_id = tk.Entry(frame, width=25, font=("Arial", 12))
    book_id.grid(row=1, column=1, padx=20, pady=15)

    tk.Label(
        frame,
        text="Member ID",
        font=("Arial", 14, "bold"),
        bg="black",
        fg="white"
    ).grid(row=2, column=0, padx=20, pady=15, sticky="e")

    member_id = tk.Entry(frame, width=25, font=("Arial", 12))
    member_id.grid(row=2, column=1, padx=20, pady=15)

    # ================= FUNCTIONS =================
    def borrow():
        if book_id.get() == "" or member_id.get() == "":
            messagebox.showerror(
                "Error",
                "Enter both IDs",
                parent=win
            )
            return

        try:
            b_id = int(book_id.get())
            m_id = int(member_id.get())
        except:
            messagebox.showerror(
                "Error",
                "IDs must be numbers",
                parent=win
            )
            return

        try:
            borrow_book(b_id, m_id)
            messagebox.showinfo(
                "Success",
                "Book Borrowed Successfully",
                parent=win
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e),
                parent=win
            )

    def return_b():
        if book_id.get() == "" or member_id.get() == "":
            messagebox.showerror(
                "Error",
                "Enter both IDs",
                parent=win
            )
            return

        try:
            b_id = int(book_id.get())
            m_id = int(member_id.get())
        except:
            messagebox.showerror(
                "Error",
                "IDs must be numbers",
                parent=win
            )
            return

        try:
            return_book(b_id, m_id)
            messagebox.showinfo(
                "Success",
                "Book Returned Successfully",
                parent=win
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e),
                parent=win
            )

    # ================= BUTTONS =================
    tk.Button(
        frame,
        text="BORROW BOOK",
        width=18,
        bg="skyblue",
        font=("Arial", 12, "bold"),
        command=borrow
    ).grid(row=3, column=0, pady=25, padx=10)

    tk.Button(
        frame,
        text="RETURN BOOK",
        width=18,
        bg="lightgreen",
        font=("Arial", 12, "bold"),
        command=return_b
    ).grid(row=3, column=1, pady=25, padx=10)