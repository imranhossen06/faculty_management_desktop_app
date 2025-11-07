import tkinter as tk
from tkinter import messagebox
from db import get_db_connection
import  os

def show_classrooms(content_frame, user):
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="Classrooms", font=("Helvetica", 16, "bold")).pack(pady=10)

    join_frame = tk.Frame(content_frame, bg="white", padx=10, pady=10)
    join_frame.pack(pady=10)

    code_entry = tk.Entry(join_frame, width=30)

    tk.Label(join_frame, text="Enter Classroom Code:", bg="white").pack()
    code_entry.pack(pady=5)

    def join_classroom():
        code = code_entry.get()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM classrooms WHERE join_code=%s", (code,))
        classroom = cursor.fetchone()

        if not classroom:
            messagebox.showerror("Error", "Invalid Classroom Code")
            return

        cursor.execute("INSERT IGNORE INTO classroom_students (classroom_id, student_id) VALUES (%s, %s)",
                       (classroom['id'], user['id']))
        conn.commit()
        conn.close()

        load_classes()  # refresh list after joining

    tk.Button(join_frame, text="Join", bg="#004aad", fg="white", command=join_classroom).pack(pady=5)

    list_frame = tk.Frame(content_frame, bg="#f0f2f5")
    list_frame.pack(fill="both", expand=True)

    def load_classes():
        for widget in list_frame.winfo_children():
            widget.destroy()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.id, c.name, c.subject, f.name AS faculty_name
            FROM classrooms c
            JOIN classroom_students s ON c.id = s.classroom_id
            JOIN faculty f ON c.faculty_id = f.id
            WHERE s.student_id = %s
        """, (user['id'],))
        classes = cursor.fetchall()
        conn.close()

        for c in classes:
            class_card = tk.Frame(list_frame, bg="white", bd=1, relief="solid")
            class_card.pack(fill="x", pady=7)

            title = tk.Label(class_card, text=c['name'], font=("Arial", 12, "bold"), bg="white")
            title.grid(row=0, column=0, sticky="w", padx=10, pady=2)

            subject = tk.Label(class_card, text=f"Subject: {c['subject']}", font=("Arial", 10), bg="white", fg="#555")
            subject.grid(row=1, column=0, sticky="w", padx=10)

            faculty = tk.Label(class_card, text=f"Faculty: {c['faculty_name']}", font=("Arial", 10, "italic"), bg="white", fg="#085E79")
            faculty.grid(row=2, column=0, sticky="w", padx=10, pady=2)

            view_btn = tk.Button(class_card, text="View", bg="#007BFF", fg="white", 
                                cursor="hand2", padx=15, pady=3,
                                command=lambda c=c: view_resources(content_frame, c))
            view_btn.grid(row=0, column=1, rowspan=3, padx=15, pady=5)

    load_classes()  # ✅ THIS DOES THE MAGIC


def view_resources(content_frame, classroom):
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text=f"{classroom['name']} - Resources", font=("Helvetica", 15, "bold")).pack(pady=10)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT r.id, r.title, r.description
        FROM classroom_resources r
        WHERE r.classroom_id=%s
        ORDER BY r.uploaded_at DESC
    """, (classroom['id'],))
    resources = cursor.fetchall()

    for r in resources:
        box = tk.Frame(content_frame, bg="white", bd=1, relief="ridge", padx=10, pady=10)
        box.pack(fill="x", pady=5)

        tk.Label(box, text=r['title'], font=("Helvetica", 12, "bold"), bg="white").pack(anchor="w")
        tk.Label(box, text=r['description'], bg="white", fg="#333").pack(anchor="w")

        cursor.execute("SELECT file_name, file_path FROM classroom_resource_files WHERE resource_id=%s", (r['id'],))
        files = cursor.fetchall()

        for f in files:
            tk.Button(box, text=f"📄 {f['file_name']}", anchor="w",
                      command=lambda p=f['file_path']: os.startfile(p)).pack(fill="x", padx=5, pady=2)

    conn.close()
