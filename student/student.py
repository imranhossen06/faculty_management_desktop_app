import tkinter as tk
from tkinter import messagebox, ttk
from db import get_db_connection
from utils.utils import create_login_card, create_hover_btn
from student.components.student_dashboard import open_student_dashboard
from student.components.registration import open_registration


def student_login(root, main_menu):
    create_login_card(
        root,
        "Student Login",
        student_login_action(root, main_menu),
        back_action=lambda: main_menu(root),
        extra_btn={
            "text": "Registration",
            "bg": "#079A5F",
            "hover": "#046c43",
            "command": lambda: student_registration(root, main_menu)
        }
    )

def student_login_action(root, main_menu):
    def action(email, password):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM student WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            messagebox.showinfo("Login Successful", f"Welcome {user['name']}")
            open_student_dashboard(root, user, lambda: main_menu(root))
     
        else:
            messagebox.showerror("Login Failed", "Invalid email or password")
    return action

def student_registration(root, main_menu):

    open_registration(root, main_menu, student_login_callback=student_login)
