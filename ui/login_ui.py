import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from ui.main_ui import start_ui


def start_login():
    root = tk.Tk()
    root.title("Librarian Login")
    root.geometry("900x600")
    root.minsize(800, 500)
    root.state("zoomed")   # opens maximized
    root.resizable(True, True)

    # Load original image
    original_img = Image.open("images/login.jpg")

    # Background label
    bg_label = tk.Label(root)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Login frame (transparent look effect using black)
    frame = tk.Frame(root, bg="black", bd=3, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Resize background properly
    def resize_bg(event):
        width = root.winfo_width()
        height = root.winfo_height()

        resized = original_img.resize((width, height))
        bg = ImageTk.PhotoImage(resized)

        bg_label.config(image=bg)
        bg_label.image = bg

    root.bind("<Configure>", resize_bg)

    # Title
    tk.Label(
        frame,
        text="LIBRARY MANAGEMENT SYSTEM",
        font=("Arial", 24, "bold"),
        bg="black",
        fg="gold",
        padx=20,
        pady=15
    ).grid(row=0, column=0, columnspan=2, pady=(10, 25))

    # Username
    tk.Label(
        frame,
        text="Username",
        font=("Arial", 14, "bold"),
        bg="black",
        fg="white"
    ).grid(row=1, column=0, padx=15, pady=12, sticky="e")

    username = tk.Entry(frame, width=28, font=("Arial", 13))
    username.grid(row=1, column=1, padx=15, pady=12)

    # Password
    tk.Label(
        frame,
        text="Password",
        font=("Arial", 14, "bold"),
        bg="black",
        fg="white"
    ).grid(row=2, column=0, padx=15, pady=12, sticky="e")

    password = tk.Entry(frame, width=28, show="*", font=("Arial", 13))
    password.grid(row=2, column=1, padx=15, pady=12)

    def login():
        user = username.get()
        pwd = password.get()

        if user == "admin" and pwd == "admin123":
            root.destroy()
            start_ui()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

    # Login button
    tk.Button(
        frame,
        text="LOGIN",
        width=18,
        bg="black",
        fg="gold",
        activebackground="gold",
        activeforeground="black",
        font=("Arial", 13, "bold"),
        command=login
    ).grid(row=3, column=0, columnspan=2, pady=25)

    root.mainloop()