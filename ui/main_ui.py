import tkinter as tk
from PIL import Image, ImageTk
from ui.book_ui import book_screen
from ui.member_ui import member_screen
from ui.loan_ui import loan_screen


def start_ui():
    root = tk.Tk()
    root.title("Library Dashboard")
    root.geometry("900x600")
    root.minsize(800, 500)
    root.state("zoomed")        # Open maximized
    root.resizable(True, True)

    # Load original image
    original_img = Image.open("images/login.jpg")

    # Background label
    bg_label = tk.Label(root)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Resize background when window changes
    def resize_bg(event):
        width = root.winfo_width()
        height = root.winfo_height()

        resized = original_img.resize((width, height))
        bg = ImageTk.PhotoImage(resized)

        bg_label.config(image=bg)
        bg_label.image = bg

    root.bind("<Configure>", resize_bg)

    # Center Main Frame
    frame = tk.Frame(root, bg="black", bd=3, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Title
    tk.Label(
        frame,
        text="MAIN MENU",
        font=("Arial", 24, "bold"),
        bg="black",
        fg="gold",
        padx=20,
        pady=15
    ).grid(row=0, column=0, pady=(10, 20), padx=30)

    # Buttons
    tk.Button(
        frame,
        text="BOOKS",
        width=20,
        height=2,
        bg="black",
        fg="gold",
        font=("Arial", 12, "bold"),
        command=lambda: book_screen(root)
    ).grid(row=1, column=0, pady=10)

    tk.Button(
        frame,
        text="MEMBERS",
        width=20,
        height=2,
        bg="black",
        fg="gold",
        font=("Arial", 12, "bold"),
        command=lambda: member_screen(root)
    ).grid(row=2, column=0, pady=10)

    tk.Button(
        frame,
        text="LOANS",
        width=20,
        height=2,
        bg="black",
        fg="gold",
        font=("Arial", 12, "bold"),
        command=lambda: loan_screen(root)
    ).grid(row=3, column=0, pady=10)

    tk.Button(
        frame,
        text="EXIT",
        width=20,
        height=2,
        bg="darkred",
        fg="white",
        font=("Arial", 12, "bold"),
        command=root.destroy
    ).grid(row=4, column=0, pady=(10, 20))

    root.mainloop()