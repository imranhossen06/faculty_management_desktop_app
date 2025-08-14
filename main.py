import tkinter as tk
from tkinter import ttk
from db import get_db_connection
# ---------- Faculty Login ----------
import tkinter as tk
from db import get_db_connection
from tkinter import messagebox

# ---------- Faculty Login ----------
def faculty_login():
    root.configure(bg="#f0f4f7")
    
    root.title("Faculty Login")  # Change title
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Faculty Login", font=("Arial", 20)).pack(pady=20)

    tk.Label(root, text="Email").pack()
    email_entry = tk.Entry(root)
    email_entry.pack()

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    # Login button now calls function with the entry values
    tk.Button(
        root,
        text="Login",
        width=20,
        command=lambda: faculty_login_action(email_entry.get(), password_entry.get())
    ).pack(pady=10)

    tk.Button(root, text="Back", width=20, command=main_menu).pack(pady=20)


def faculty_login_action(email, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM faculty WHERE email=%s AND password=%s",
        (email, password)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("Login Successful", f"Welcome {user['name']}")
        print(user, "user data got")
        
    else:
        messagebox.showerror("Login Failed", "Invalid email or password")





# ---------- Student Registration ----------

def student_registration_action(name, email, student_id, password, department_id, intake, section, phone, dob, confirm_password):
    # Final validation: Password match
    if password != confirm_password:
        messagebox.showerror("Error", "Password and Confirm Password do not match")
        return
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO student (name,email,student_id,password,department_id,intake,section,phone,dob) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (name, email, student_id, password, department_id, intake, section, phone, dob)
        )
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", f"Student {name} registered successfully!")
        student_menu()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))


def student_registration():
    root.title("Student Registration")
    
    # --- Fetch Departments ---
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM department WHERE status=1")
    departmentList = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # --- Clear Old Widgets ---
    for widget in root.winfo_children():
        widget.destroy()
    
    # --- Main Frame ---
    main_frame = tk.Frame(root, bg="#f0f4f7", padx=30, pady=30)
    main_frame.pack(expand=True, fill=tk.BOTH)
    
    tk.Label(main_frame, text="Student Registration", font=("Helvetica", 24, "bold"), bg="#f0f4f7").pack(pady=(0, 20))
    
    form_frame = tk.Frame(main_frame, bg="#f0f4f7")
    form_frame.pack()
    
    # --- Helper to add fields ---
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

    # --- Form Fields ---
    name_entry = add_field("Full Name:", required=True)
    email_entry = add_field("Email:", required=True)
    student_id_entry = add_field("Student ID:", required=True)
    
    # Department Dropdown
    dept_frame = tk.Frame(form_frame, bg="#f0f4f7")
    dept_frame.pack(fill=tk.X, pady=5)
    tk.Label(dept_frame, text="Department: *", width=15, anchor='w', fg="red", bg="#f0f4f7").pack(side=tk.LEFT)
    
    department_var = tk.StringVar()
    department_dict = {dept['name']: dept['id'] for dept in departmentList}  
    department_combo = ttk.Combobox(dept_frame, textvariable=department_var, values=list(department_dict.keys()), state="readonly")
    department_combo.set("Select Department")
    department_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    intake_entry = add_field("Intake:", required=True)
    section_entry = add_field("Section:", required=True)
    
    # DOB Dropdown
    dob_frame_outer = tk.Frame(form_frame, bg="#f0f4f7")
    dob_frame_outer.pack(fill=tk.X, pady=5)
    tk.Label(dob_frame_outer, text="Date of Birth: *", width=15, anchor='w', fg="red", bg="#f0f4f7").pack(side=tk.LEFT)
    
    dob_frame = tk.Frame(dob_frame_outer, bg="#f0f4f7")
    dob_frame.pack(side=tk.LEFT)
    
    day_var = tk.StringVar()
    month_var = tk.StringVar()
    year_var = tk.StringVar()
    
    day_combo = ttk.Combobox(dob_frame, textvariable=day_var, values=[str(i) for i in range(1, 32)], width=4)
    day_combo.set("Day")
    day_combo.pack(side=tk.LEFT, padx=5)
    
    month_combo = ttk.Combobox(dob_frame, textvariable=month_var, values=[str(i) for i in range(1, 13)], width=4)
    month_combo.set("Month")
    month_combo.pack(side=tk.LEFT, padx=5)
    
    year_combo = ttk.Combobox(dob_frame, textvariable=year_var, values=[str(i) for i in range(1950, 2025)], width=6)
    year_combo.set("Year")
    year_combo.pack(side=tk.LEFT, padx=5)
    
    contact_entry = add_field("Contact No:", required=True)
    password_entry1 = add_field("Password:", required=True, show="*")
    password_entry2 = add_field("Confirm Password:", required=True, show="*")
    
    # --- Validation and Register ---
    def validate_and_register():
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
        # Check for empty fields
        for field_name, value in required_fields.items():
            if not value or value in ["Select Department", "Day", "Month", "Year"]:
                messagebox.showerror("Required Field Missing", f"Please enter/select {field_name}")
                return
        
        if password_entry1.get() != password_entry2.get():
            messagebox.showerror("Password Mismatch", "Password and Confirm Password do not match")
            return
        
        dob = f"{year_var.get()}-{month_var.get()}-{day_var.get()}"
        
        student_registration_action(
            name_entry.get(),
            email_entry.get(),
            student_id_entry.get(),
            password_entry1.get(),
            department_dict.get(department_var.get()),
            intake_entry.get(),
            section_entry.get(),
            contact_entry.get(),
            dob,
            password_entry2.get()
        )
    
    # --- Buttons ---
    btn_frame = tk.Frame(main_frame, bg="#f0f4f7")
    btn_frame.pack(pady=20)
    
    tk.Button(btn_frame, text="Register", bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"),
              width=15, command=validate_and_register).pack(side=tk.LEFT, padx=10)
    
    tk.Button(btn_frame, text="Back", bg="#f44336", fg="white", font=("Helvetica", 12, "bold"),
              width=15, command=student_menu).pack(side=tk.LEFT, padx=10)


# ---------- Student Login ----------
def student_login():
    root.configure(bg="#f0f4f7")
    root.title("Student Login")  # Change title
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Student Login", font=("Arial", 20)).pack(pady=20)

    tk.Label(root, text="Email").pack()
    email_entry = tk.Entry(root)
    email_entry.pack()

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    tk.Button(root, text="Login", width=20, command=lambda: student_login_action(email_entry.get(), password_entry.get())).pack(pady=10)
    tk.Button(root, text="Back", width=20, command=student_menu).pack(pady=20)

def student_login_action(email, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM student WHERE email=%s AND password=%s",
        (email, password)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("Login Successful", f"Welcome {user['name']}")
        print(user, "user data got")
        
    else:
        messagebox.showerror("Login Failed", "Invalid email or password")


# ---------- Student Menu ----------
def student_menu():
    root.title("Student Panel")  # Change title
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Student Panel", font=("Arial", 20)).pack(pady=20)
    tk.Button(root, text="Login", width=20, command=student_login).pack(pady=10)
    tk.Button(root, text="Registration", width=20, command=student_registration).pack(pady=10)
    tk.Button(root, text="Back", width=20, command=main_menu).pack(pady=20)


# ---------- Main Menu ----------

def main_menu():
    root.title("Main Panel")
    
    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()
    
    # Set main background color
    root.configure(bg="#004225")
    
    # --- Header ---
    header_frame = tk.Frame(root, bg="#004225")
    header_frame.pack(fill=tk.X, pady=(40, 20))
    tk.Label(header_frame, text="Academic Management System", 
             font=("Helvetica", 32, "bold"), bg="#004225", fg="white").pack()
    
    # --- Center Card Panel ---
    card_frame = tk.Frame(root, bg="white", bd=0, relief=tk.RIDGE)
    card_frame.place(relx=0.5, rely=0.55, anchor=tk.CENTER, width=500, height=350)
    
    # Shadow effect
    shadow = tk.Frame(root, bg="#003318")
    shadow.place(relx=0.5, rely=0.55, anchor=tk.CENTER, width=504, height=354)
    shadow.lower(card_frame)
    
    # Card content
    tk.Label(card_frame, text="Select Your Panel", font=("Helvetica", 22, "bold"),
             bg="white", fg="#004225").pack(pady=(40, 30))
    
    # Buttons with cursor pointer and hover effect
    def create_button(text, bg_color, hover_color, command):
        btn = tk.Button(card_frame, text=text, font=("Helvetica", 14, "bold"),
                        bg=bg_color, fg="white", width=22, height=2, bd=0, command=command,
                        cursor="hand2")  # hand2 makes the pointer cursor
        btn.pack(pady=10)
        
        # Hover effect
        def on_enter(e):
            btn.config(bg=hover_color)
        def on_leave(e):
            btn.config(bg=bg_color)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn
    
    create_button("Faculty", "#4CAF50", "#45a049", faculty_login)
    create_button("Student", "#2196F3", "#1e88e5", student_menu)
    
    # Footer
    tk.Label(root, text="© 2025 Academic Management System", font=("Helvetica", 10),
             bg="#004225", fg="white").pack(side=tk.BOTTOM, pady=15)



# ---------- Tkinter Window ----------
root = tk.Tk()
root.title("Main Panel")
root.state('zoomed')
main_menu()
root.mainloop()
