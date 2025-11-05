import tkinter as tk
from tkinter import messagebox, ttk

from db import get_db_connection
from utils.utils import create_login_card, create_hover_btn


def student_login(root, main_menu):
    create_login_card(
        root,
        "Student Login",
        student_login_action(root, main_menu),
        main_menu,
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
            open_student_dashboard(root, user, main_menu)
        else:
            messagebox.showerror("Login Failed", "Invalid email or password")
    return action

def student_registration(root, main_menu):
    root.title("Student Registration")
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM department WHERE status=1")
    departmentList = cursor.fetchall()
    cursor.close()
    conn.close()

    for widget in root.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(root, bg="#f0f4f7", padx=30, pady=30)
    main_frame.pack(expand=True, fill=tk.BOTH)

    tk.Label(main_frame, text="Student Registration", font=("Helvetica", 24, "bold"), bg="#f0f4f7").pack(pady=(0,20))

    form_frame = tk.Frame(main_frame, bg="#f0f4f7")
    form_frame.pack()

    def add_field(label_text, required=False, show=None):
        frame = tk.Frame(form_frame, bg="#f0f4f7")
        frame.pack(fill=tk.X, pady=5)
        if required:
            tk.Label(frame, text=label_text + " *", width=15, anchor='w', fg="red", bg="#f0f4f7").pack(side=tk.LEFT)
        else:
            tk.Label(frame, text=label_text, width=15, anchor='w', bg="#f0f4f7").pack(side=tk.LEFT)
        entry = tk.Entry(frame, show=show)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        return entry

    name_entry = add_field("Full Name:", True)
    email_entry = add_field("Email:", True)
    student_id_entry = add_field("Student ID:", True)

    # Department
    dept_frame = tk.Frame(form_frame, bg="#f0f4f7")
    dept_frame.pack(fill=tk.X, pady=5)
    tk.Label(dept_frame, text="Department: *", width=15, anchor='w', fg="red", bg="#f0f4f7").pack(side=tk.LEFT)
    department_var = tk.StringVar()
    department_dict = {dept['name']: dept['id'] for dept in departmentList}
    department_combo = ttk.Combobox(dept_frame, textvariable=department_var, values=list(department_dict.keys()), state="readonly")
    department_combo.set("Select Department")
    department_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)

    intake_entry = add_field("Intake:", True)
    section_entry = add_field("Section:", True)
    contact_entry = add_field("Contact No:", True)
    password_entry1 = add_field("Password:", True, show="*")
    password_entry2 = add_field("Confirm Password:", True, show="*")

    def validate_and_register():
        required_fields = {
            "Full Name": name_entry.get(),
            "Email": email_entry.get(),
            "Student ID": student_id_entry.get(),
            "Department": department_var.get(),
            "Intake": intake_entry.get(),
            "Section": section_entry.get(),
            "Password": password_entry1.get(),
            "Confirm Password": password_entry2.get()
        }
        for field_name, value in required_fields.items():
            if not value or value in ["Select Department"]:
                messagebox.showerror("Required Field Missing", f"Please enter/select {field_name}")
                return
        if password_entry1.get() != password_entry2.get():
            messagebox.showerror("Password Mismatch", "Password and Confirm Password do not match")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO student (name,email,student_id,password,department_id,intake,section,phone) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (name_entry.get(), email_entry.get(), student_id_entry.get(), password_entry1.get(),
                 department_dict.get(department_var.get()), intake_entry.get(), section_entry.get(), contact_entry.get(), "N/A")
            )
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", f"Student {name_entry.get()} registered successfully!")
            student_login(root, main_menu)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    btn_frame = tk.Frame(main_frame, bg="#f0f4f7")
    btn_frame.pack(pady=20)
    tk.Button(btn_frame, text="Register", bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), width=15, command=validate_and_register).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Back", bg="#f44336", fg="white", font=("Helvetica", 12, "bold"), width=15, command=lambda: student_login(root, main_menu)).pack(side=tk.LEFT, padx=10)

def open_student_dashboard(root, user, main_menu):
    for widget in root.winfo_children():
        widget.destroy()
    tk.Label(root, text=f"Student Dashboard - {user['name']}", font=("Helvetica", 20, "bold")).pack(pady=50)
    tk.Button(root, text="Back to Main Menu", command=lambda: main_menu(root)).pack()
