import tkinter as tk
from tkinter import ttk, messagebox
from db import get_db_connection

def show_faculty_appointments(content_frame, user):
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="Student Appointment Requests", font=("Helvetica", 14, "bold"),
             bg="#f0f2f5").pack(pady=10)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT a.id AS appointment_id, s.name AS student, s.intake, s.student_id, s.section, w.name AS day, c.start_time, c.end_time, a.status
        FROM appointments a
        JOIN student s ON a.student_id = s.id
        JOIN counselling_slots c ON a.slot_id = c.id
        JOIN weekly_days w ON c.weekly_days_id = w.id
        WHERE c.faculty_id=%s
        ORDER BY a.id DESC
    """
    cursor.execute(query, (user['id'],))
    rows = cursor.fetchall()
    conn.close()

    table = ttk.Treeview(
        content_frame,
        columns=("Student", "Intake", "Section", "Day", "Start", "End", "Status"),
        show="headings",
        height=12
    )
    table.pack(expand=True, fill="both", padx=20, pady=10)

    table.heading("Student", text="Student Name")
    table.heading("Intake", text="Intake")
    table.heading("Section", text="Section")
    table.heading("Day", text="Day")
    table.heading("Start", text="Start Time")
    table.heading("End", text="End Time")
    table.heading("Status", text="Status")

    table.column("Student", width=160, anchor="center")
    table.column("Intake", width=90, anchor="center")
    table.column("Section", width=90, anchor="center")
    table.column("Day", width=90, anchor="center")
    table.column("Start", width=120, anchor="center")
    table.column("End", width=120, anchor="center")
    table.column("Status", width=110, anchor="center")

    for row in rows:
        table.insert("", tk.END, iid=row['appointment_id'], values=(
            row['student'],
            row['intake'],
            row['section'],
            row['day'],
            str(row['start_time'])[:-3],
            str(row['end_time'])[:-3],
            row['status']
        ))

    action_frame = tk.Frame(content_frame, bg="#f0f2f5")
    action_frame.pack(pady=10)

    def approve():
        selected = table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a request")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE appointments SET status='approved' WHERE id=%s", (selected,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Appointment Approved")
        show_faculty_appointments(content_frame, user)

    def reject():
        selected = table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a request")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE appointments SET status='rejected' WHERE id=%s", (selected,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Appointment Rejected")
        show_faculty_appointments(content_frame, user)

    tk.Button(action_frame, text="Approve", bg="#4CAF50", fg="white", width=14, command=approve).pack(side="left", padx=8)
    tk.Button(action_frame, text="Reject", bg="#d32f2f", fg="white", width=14, command=reject).pack(side="left")
