# student/components/classrooms.py

import tkinter as tk
from tkinter import font
from db import get_db_connection

def show_classrooms(content_frame, user):
    for widget in content_frame.winfo_children():
        widget.destroy()

    heading_font = font.Font(family="Helvetica", size=14, weight="bold")
    tk.Label(content_frame, text="Your Classrooms", font=heading_font, bg="#f0f2f5").pack(pady=10)

    container = tk.Frame(content_frame, bg="#f0f2f5")
    container.pack(padx=10, pady=10)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.course_name, c.room, c.schedule
        FROM classroom_enrollment ce
        JOIN classrooms c ON ce.classroom_id = c.id
        WHERE ce.student_id=%s
    """, (user['id'],))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        tk.Label(container, text="No classrooms assigned.", bg="#f0f2f5", font=("Helvetica", 12)).pack()
        return
    
    for row in rows:
        card = tk.Frame(container, bg="white", bd=1, relief="solid")
        card.pack(fill="x", pady=5)

        tk.Label(card, text=row['course_name'], bg="white", font=("Helvetica", 12, "bold")).pack(anchor="w", padx=10, pady=3)
        tk.Label(card, text=f"Room: {row['room']} | Schedule: {row['schedule']}", bg="white").pack(anchor="w", padx=10, pady=2)
