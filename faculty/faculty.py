import tkinter as tk
from tkinter import messagebox
from db import get_db_connection
from utils.utils import create_login_card
from faculty.components.faculty_dashboard import open_faculty_dashboard
def faculty_login(root, main_menu):
    # Prepare the login callback
    login_callback = faculty_login_action(root, main_menu)  # this returns the 'action' function
    create_login_card(
        root,
        "Faculty Login",
        login_callback,  # pass the returned function
        main_menu
    )




def faculty_login_action(root, main_menu):
    def action(email, password):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM faculty WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            messagebox.showinfo("Login Successful", f"Welcome {user['name']}")
            open_faculty_dashboard(root, user, lambda: main_menu(root))
        else:
            messagebox.showerror("Login Failed", "Invalid email or password")
    return action
