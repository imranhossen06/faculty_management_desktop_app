import tkinter as tk
from tkinter import ttk, messagebox
from db import get_db_connection
from datetime import datetime

def show_join_counselling(content_frame, user):
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="Join Counselling Hours",
             font=("Helvetica", 16, "bold"), bg="#f0f2f5").pack(pady=10)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch faculty list
    cursor.execute("SELECT id, name FROM faculty")
    faculty_list = cursor.fetchall()

    conn.close()

    filter_frame = tk.Frame(content_frame, bg="#f0f2f5")
    filter_frame.pack(pady=5)

    tk.Label(filter_frame, text="Select Faculty:", bg="#f0f2f5",
             font=("Helvetica", 11)).grid(row=0, column=0, padx=5)

    faculty_var = tk.StringVar()
    faculty_dropdown = ttk.Combobox(filter_frame, textvariable=faculty_var, width=30, state="readonly")
    faculty_dropdown['values'] = [f"{f['id']} - {f['name']}" for f in faculty_list]
    faculty_dropdown.grid(row=0, column=1, padx=5)

    # Table for slots
    table = ttk.Treeview(content_frame, columns=("Day","Start","End"), show="headings", height=12)
    table.heading("Day", text="Day")
    table.heading("Start", text="Start Time")
    table.heading("End", text="End Time")
    table.pack(expand=True, fill="both", padx=20, pady=10)

    def load_slots():
        selected = faculty_var.get()
        if not selected:
            return

        faculty_id = selected.split(" - ")[0]  # Extract ID

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT c.id, w.name AS day, c.start_time, c.end_time
            FROM counselling_slots c
            JOIN weekly_days w ON c.weekly_days_id = w.id
            WHERE c.faculty_id=%s AND c.is_active=1
            ORDER BY w.id
        """, (faculty_id,))
        slots = cursor.fetchall()
        conn.close()

        # Clear previous rows
        table.delete(*table.get_children())

        for s in slots:
            table.insert("", tk.END, iid=s['id'], values=(s['day'], s['start_time'], s['end_time']))

    faculty_dropdown.bind("<<ComboboxSelected>>", lambda e: load_slots())

    # Notes input
    tk.Label(content_frame, text="Notes (optional):", bg="#f0f2f5").pack(pady=5)
    notes = tk.Entry(content_frame, width=40)
    notes.pack()

    # Book slot
    def book():
        selected = table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a slot first.")
            return

        slot_id = selected
        txt = notes.get()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO appointments (slot_id, student_id, notes, status, booked_at)
            VALUES (%s, %s, %s, 'pending', %s)
        """, (slot_id, user['id'], txt, datetime.now()))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Appointment request sent!")
        load_slots()

    tk.Button(content_frame, text="Book Appointment", bg="#004aad", fg="white",
              font=("Helvetica", 11, "bold"), width=18, command=book).pack(pady=12)
