import tkinter as tk
from tkinter import font
from student.components.appointments import show_student_appointments
from student.components.classrooms import show_classrooms
from student.components.join_counselling import show_join_counselling
from db import get_db_connection

def open_student_dashboard(root, user, main_menu_callback):
    root.title(f"Student Dashboard - {user['name']}")

    for widget in root.winfo_children():
        widget.destroy()

    heading_font = font.Font(family="Helvetica", size=12, weight="bold")
    big_font = font.Font(family="Helvetica", size=14, weight="bold")
    small_font = font.Font(family="Helvetica", size=10)

    # ========== Sidebar ==========
    sidebar = tk.Frame(root, bg="#004aad", width=240)
    sidebar.pack(side="left", fill="y")

    tk.Label(sidebar, text="BUBT STUDENT", bg="#004aad", fg="white",
             font=("Helvetica", 18, "bold")).pack(pady=30)

    # ========== Main Area ==========
    main_area = tk.Frame(root, bg="#f0f2f5")
    main_area.pack(side="left", fill="both", expand=True)

    content_frame = tk.Frame(main_area, bg="#f0f2f5")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def show_dashboard():
        for widget in content_frame.winfo_children():
            widget.destroy()

        # Fetch Stats
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS total FROM appointments WHERE student_id=%s", (user['id'],))
        total = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) AS c FROM appointments WHERE status='pending' AND student_id=%s", (user['id'],))
        pending = cursor.fetchone()['c']

        cursor.execute("SELECT COUNT(*) AS c FROM appointments WHERE status='approved' AND student_id=%s", (user['id'],))
        approved = cursor.fetchone()['c']

        cursor.execute("SELECT COUNT(*) AS c FROM appointments WHERE status='rejected' AND student_id=%s", (user['id'],))
        rejected = cursor.fetchone()['c']

        cursor.execute("SELECT COUNT(*) AS c FROM appointments WHERE status='cancelled' AND student_id=%s", (user['id'],))
        cancelled = cursor.fetchone()['c']

        conn.close()

        stats = [
            ("Total Appointments", total),
            ("Pending", pending),
            ("Approved", approved),
            ("Rejected", rejected),
            ("Cancelled", cancelled),
        ]

        for title, value in stats:
            card = tk.Frame(content_frame, bg="white", width=180, height=90, relief="ridge", bd=1)
            card.pack(side="left", padx=8)
            card.pack_propagate(False)

            tk.Label(card, text=title, bg="white", font=small_font).pack(pady=5)
            tk.Label(card, text=value, bg="white", font=("Helvetica", 18, "bold")).pack()

    def show_appointment():
        show_student_appointments(content_frame, user)

    def show_classroom():
        show_classrooms(content_frame, user)

    def join_counselling():
        show_join_counselling(content_frame, user)
    
    def go_back_to_main_menu():
        for widget in root.winfo_children():
            widget.destroy()
        main_menu_callback()  # takes back to main.py menu


    menu_items = [
        ("Dashboard", show_dashboard),
        ("Appointments", show_appointment),
        ("Classrooms", show_classroom),
        ("Join Counselling Hours", join_counselling),
    ]

    for text, cmd in menu_items:
        tk.Button(sidebar, text=text, anchor="w", command=cmd,
                  bg="#004aad", fg="white", relief="flat", bd=0,
                  activebackground="#00337b", padx=15).pack(fill="x", pady=6)

    # Logout Button
    # tk.Button(sidebar, text="Logout / Main Menu", bg="#d32f2f", fg="white",
    #           relief="flat", command=main_menu_callback).pack(fill="x", pady=40)
    logout_btn = tk.Button(sidebar, text="Logout / Main Menu", anchor="w",
                       bg="#f44336", fg="white", relief="flat", bd=0,
                       font=small_font,
                       command=lambda: go_back_to_main_menu())
    logout_btn.pack(fill="x", pady=20, padx=12, side="bottom")


    show_dashboard()
