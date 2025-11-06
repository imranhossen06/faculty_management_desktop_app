import tkinter as tk
from tkinter import ttk, messagebox
from db import get_db_connection


def open_registration(root, main_menu, student_login_callback=None):
    root.title("Student Registration")
    root.geometry("600x700")
    
    # Clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Fetch active departments
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM department WHERE status=1")
    departmentList = cursor.fetchall()
    cursor.close()
    conn.close()

    main_frame = tk.Frame(root, bg="#f0f4f7", padx=30, pady=30)
    main_frame.pack(expand=True, fill=tk.BOTH)

    tk.Label(main_frame, text="Student Registration",
             font=("Helvetica", 24, "bold"), bg="#f0f4f7").pack(pady=(0, 20))

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

    # Fields
    name_entry = add_field("Full Name:", True)
    email_entry = add_field("Email:", True)
    student_id_entry = add_field("Student ID:", True)

    # Department Combobox
    dept_frame = tk.Frame(form_frame, bg="#f0f4f7")
    dept_frame.pack(fill=tk.X, pady=5)
    tk.Label(dept_frame, text="Department: *", width=15, anchor='w', fg="red", bg="#f0f4f7").pack(side=tk.LEFT)
    department_var = tk.StringVar()
    department_dict = {dept['name']: dept['id'] for dept in departmentList}
    department_combo = ttk.Combobox(dept_frame, textvariable=department_var,
                                    values=list(department_dict.keys()), state="readonly")
    department_combo.set("Select Department")
    department_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)

    intake_entry = add_field("Intake:", True)
    section_entry = add_field("Section:", True)
    contact_entry = add_field("Contact No:", True)
    password_entry1 = add_field("Password:", True, show="*")
    password_entry2 = add_field("Confirm Password:", True, show="*")

    # Date of Birth
    tk.Label(form_frame, text="Date of Birth: *", bg="#f0f4f7").pack(pady=(10, 0))
    day_var = tk.StringVar(value="Day")
    month_var = tk.StringVar(value="Month")
    year_var = tk.StringVar(value="Year")
    days = [str(i) for i in range(1, 32)]
    months = [str(i) for i in range(1, 13)]
    years = [str(i) for i in range(1950, 2025)]
    dob_frame = tk.Frame(form_frame, bg="#f0f4f7")
    dob_frame.pack(pady=5)
    tk.OptionMenu(dob_frame, day_var, *days).pack(side=tk.LEFT, padx=5)
    tk.OptionMenu(dob_frame, month_var, *months).pack(side=tk.LEFT, padx=5)
    tk.OptionMenu(dob_frame, year_var, *years).pack(side=tk.LEFT, padx=5)

    def validate_and_register():
        # Validate required fields
        required_fields = {
            "Full Name": name_entry.get(),
            "Email": email_entry.get(),
            "Student ID": student_id_entry.get(),
            "Department": department_var.get(),
            "Intake": intake_entry.get(),
            "Section": section_entry.get(),
            "Password": password_entry1.get(),
            "Confirm Password": password_entry2.get(),
            "Day": day_var.get(),
            "Month": month_var.get(),
            "Year": year_var.get()
        }

        for field_name, value in required_fields.items():
            if not value or value in ["Select Department", "Day", "Month", "Year"]:
                messagebox.showerror("Required Field Missing", f"Please enter/select {field_name}")
                return

        if password_entry1.get() != password_entry2.get():
            messagebox.showerror("Password Mismatch", "Password and Confirm Password do not match")
            return

        dob = f"{year_var.get()}-{month_var.get().zfill(2)}-{day_var.get().zfill(2)}"

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO student
                   (name,email,student_id,password,department_id,intake,section,phone,photo,dob,created_by)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                    name_entry.get(), email_entry.get(), student_id_entry.get(), password_entry1.get(),
                    department_dict.get(department_var.get()), intake_entry.get(), section_entry.get(),
                    contact_entry.get(), None, dob, None
                )
            )
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", f"Student {name_entry.get()} registered successfully!")
            # Return to login page
            if student_login_callback:
                student_login_callback(root, main_menu)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # Buttons
    btn_frame = tk.Frame(main_frame, bg="#f0f4f7")
    btn_frame.pack(pady=20)
    tk.Button(btn_frame, text="Register", bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"),
              width=15, command=validate_and_register).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Back", bg="#f44336", fg="white", font=("Helvetica", 12, "bold"),
              width=15, command=lambda: student_login_callback(root, main_menu) if student_login_callback else None).pack(side=tk.LEFT, padx=10)
