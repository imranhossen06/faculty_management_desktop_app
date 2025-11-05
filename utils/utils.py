import tkinter as tk

def create_hover_btn(parent, text, bg_color, hover_color, command, pady=5):
    btn = tk.Button(parent, text=text, bg=bg_color, fg="white",
                    font=("Helvetica", 12, "bold"), width=25, height=2,
                    bd=0, command=command, cursor="hand2")
    btn.pack(pady=pady)
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
    return btn

def create_login_card(root, title, login_action, back_action, extra_btn=None):
    # Clear previous
    for widget in root.winfo_children():
        widget.destroy()

    # Container
    container = tk.Frame(root, bg="#f0f4f7")
    container.pack(expand=True, fill="both")

    # Shadow effect
    shadow = tk.Frame(container, bg="#d6d6d6")
    shadow.place(relx=0.5, rely=0.5, anchor="center", width=420, height=420)

    # Card
    card = tk.Frame(container, bg="white", bd=0, relief="ridge")
    card.place(relx=0.5, rely=0.5, anchor="center", width=400, height=400)

    # Title
    tk.Label(card, text=title, font=("Helvetica", 20, "bold"),
             bg="white", fg="#004225").pack(pady=(30, 20))

    # Email field
    tk.Label(card, text="Email", bg="white", fg="black", font=("Helvetica", 10)).pack(pady=(0, 5))
    email_entry = tk.Entry(card, width=30, font=("Helvetica", 11), bd=1, relief="solid")
    email_entry.pack(pady=(0, 15))

    # Password field
    tk.Label(card, text="Password", bg="white", fg="black", font=("Helvetica", 10)).pack(pady=(0, 5))
    password_entry = tk.Entry(card, show="*", width=30, font=("Helvetica", 11), bd=1, relief="solid")
    password_entry.pack(pady=(0, 10))

    # Show/Hide password toggle
    def toggle_password():
        if password_entry.cget('show') == '*':
            password_entry.config(show='')
            eye_btn.config(text="Hide")
        else:
            password_entry.config(show='*')
            eye_btn.config(text="Show")

    eye_btn = tk.Button(card, text="Show", command=toggle_password,
                        bg="white", fg="#004225", bd=0, cursor="hand2", font=("Helvetica", 8))
    eye_btn.pack(pady=(0, 15))

    # Buttons
    def create_hover_btn_local(text, bg_color, hover_color, command, pady=5):
        btn = tk.Button(card, text=text, bg=bg_color, fg="white",
                        font=("Helvetica", 12, "bold"), width=25, height=2,
                        bd=0, command=command, cursor="hand2")
        btn.pack(pady=pady)
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
        return btn

    create_hover_btn_local("Login", "#074d51", "#086752", lambda: login_action(email_entry.get(), password_entry.get()), pady=5)

    if extra_btn:
        create_hover_btn_local(extra_btn["text"], extra_btn["bg"], extra_btn["hover"], extra_btn["command"], pady=5)

    create_hover_btn_local("Back", "#757575", "#424242", back_action, pady=5)
