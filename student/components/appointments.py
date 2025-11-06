import tkinter as tk
from tkinter import ttk
from db import get_db_connection

def show_student_appointments(content_frame, user):
    # Clear previous UI
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="My Appointments", font=("Helvetica", 14, "bold"),
            bg="#f0f2f5").pack(pady=10)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT a.id, w.name AS day, c.start_time, c.end_time, a.status
        FROM appointments a
        JOIN counselling_slots c ON a.slot_id = c.id
        JOIN weekly_days w ON c.weekly_days_id = w.id
        WHERE a.student_id=%s
        ORDER BY a.id DESC
    """
    cursor.execute(query, (user['id'],))
    rows = cursor.fetchall()
    conn.close()

    table = ttk.Treeview(content_frame, columns=("Day","Start","End","Status"), show="headings", height=12)
    table.pack(expand=True, fill="both", padx=20, pady=10)

    # ===== Table Headings =====
    table.heading("Day", text="Day")
    table.heading("Start", text="Start Time")
    table.heading("End", text="End Time")
    table.heading("Status", text="Status")

    # ===== Column Width & Alignment Fix =====
    table.column("Day", width=120, anchor="center")
    table.column("Start", width=120, anchor="center")
    table.column("End", width=120, anchor="center")
    table.column("Status", width=140, anchor="center")


    for row in rows:
        table.insert("", tk.END, values=(row['day'], row['start_time'], row['end_time'], row['status']))
