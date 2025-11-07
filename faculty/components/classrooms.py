import tkinter as tk
from tkinter import messagebox, filedialog
from db import get_db_connection
import random, string, os
from tkinter import simpledialog

def show_faculty_classrooms(content_frame, faculty):
    for widget in content_frame.winfo_children():
        widget.destroy()

    def generate_code():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    header = tk.Label(content_frame, text="Your Classrooms", font=("Helvetica", 16, "bold"), bg="#f0f2f5")
    header.pack(pady=10)

    # ---------- CREATE CLASSROOM SECTION ----------
    form = tk.Frame(content_frame, bg="white", padx=15, pady=15, relief="groove", bd=1)
    form.pack(pady=10)

    tk.Label(form, text="Classroom Name:", bg="white").grid(row=0, column=0, sticky="w")
    name_entry = tk.Entry(form, width=35)
    name_entry.grid(row=0, column=1, pady=5)

    tk.Label(form, text="Subject:", bg="white").grid(row=1, column=0, sticky="w")
    subject_entry = tk.Entry(form, width=35)
    subject_entry.grid(row=1, column=1, pady=5)

    def save_classroom():
        name = name_entry.get()
        subject = subject_entry.get()
        code = generate_code()

        if name == "":
            messagebox.showwarning("Warning", "Classroom name required.")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO classrooms (name, subject, join_code, faculty_id) VALUES (%s, %s, %s, %s)",
                       (name, subject, code, faculty['id']))
        conn.commit()
        conn.close()

        name_entry.delete(0, tk.END)
        subject_entry.delete(0, tk.END)
        load_classrooms()

    tk.Button(form, text="Create Classroom", bg="#004aad", fg="white", command=save_classroom).grid(columnspan=2, pady=8)

    # ---------- LIST EXISTING CLASSROOMS ----------
    list_frame = tk.Frame(content_frame, bg="#f0f2f5")
    list_frame.pack(fill="both", expand=True, pady=15)

    def load_classrooms():
        for widget in list_frame.winfo_children():
            widget.destroy()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM classrooms WHERE faculty_id=%s", (faculty['id'],))
        classes = cursor.fetchall()
        conn.close()

        for c in classes:
            box = tk.Frame(list_frame, bg="white", relief="ridge", bd=1, padx=10, pady=10)
            box.pack(fill="x", pady=5)

            tk.Label(box, text=f"{c['name']}  |  {c['subject']}", font=("Helvetica", 12, "bold"), bg="white").pack(anchor="w")
            tk.Label(box, text=f"Join Code: {c['join_code']}", bg="white", fg="#444").pack(anchor="w")

            tk.Button(box, text="Open Classroom", bg="#004aad", fg="white",
                      command=lambda c=c: open_classroom_resources(content_frame, c)).pack(anchor="e", pady=5)

    load_classrooms()


# ---------- RESOURCES PAGE ----------
def open_classroom_resources(content_frame, classroom):
   

    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text=f"{classroom['name']} - Resources", font=("Helvetica", 15, "bold")).pack(pady=10)

    # ---------- UPLOAD FORM ----------
    upload_frame = tk.Frame(content_frame, bg="white", padx=10, pady=10, relief="ridge", bd=1)
    upload_frame.pack(pady=10, fill="x")

    title_entry = tk.Entry(upload_frame, width=50)
    desc_entry = tk.Text(upload_frame, width=50, height=3)

    tk.Label(upload_frame, text="Title:", bg="white").grid(row=0, column=0, sticky="w")
    title_entry.grid(row=0, column=1, pady=5, sticky="w")

    tk.Label(upload_frame, text="Description:", bg="white").grid(row=1, column=0, sticky="nw")
    desc_entry.grid(row=1, column=1, pady=5, sticky="w")

    selected_files = []

    def choose_files():
        files = filedialog.askopenfilenames()
        selected_files.extend(files)
        messagebox.showinfo("Files Added", f"{len(files)} file(s) selected.")

    def upload_resource():
        title = title_entry.get().strip()
        desc = desc_entry.get("1.0", tk.END).strip()

        if title == "":
            messagebox.showwarning("Warning", "Title is required.")
            return

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO classroom_resources (classroom_id, title, description) VALUES (%s, %s, %s)",
                       (classroom['id'], title, desc))
        resource_id = cursor.lastrowid

        for f in selected_files:
            cursor.execute("INSERT INTO classroom_resource_files (resource_id, file_path, file_name) VALUES (%s, %s, %s)",
                           (resource_id, f, os.path.basename(f)))

        conn.commit()
        conn.close()
        open_classroom_resources(content_frame, classroom)

    tk.Button(upload_frame, text="Select Files", bg="#00897b", fg="white", command=choose_files).grid(row=2, column=1, sticky="w", pady=5)
    tk.Button(upload_frame, text="Save", bg="#004aad", fg="white", command=upload_resource).grid(row=3, column=1, sticky="w", pady=5)

    # ---------- RESOURCES LIST ----------
    list_area = tk.Frame(content_frame, bg="#f0f2f5")
    list_area.pack(fill="both", expand=True, pady=10)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM classroom_resources WHERE classroom_id=%s ORDER BY uploaded_at DESC", (classroom['id'],))
    resources = cursor.fetchall()

    for r in resources:
        card = tk.Frame(list_area, bg="white", padx=10, pady=10, relief="ridge", bd=1)
        card.pack(fill="x", pady=8)

        tk.Label(card, text=r['title'], font=("Helvetica", 13, "bold"), bg="white").pack(anchor="w")
        if r['description']:
            tk.Label(card, text=r['description'], bg="white", fg="#444").pack(anchor="w", pady=3)

        # FETCH FILES
        cursor.execute("SELECT * FROM classroom_resource_files WHERE resource_id=%s", (r['id'],))
        files = cursor.fetchall()

        for f in files:
            tk.Button(card, text=f"📄 {f['file_name']}", bg="white", bd=0, anchor="w",
                      command=lambda p=f['file_path']: os.startfile(p)).pack(fill="x", padx=12, pady=1)

        # EDIT + DELETE BUTTONS ROW
        btn_row = tk.Frame(card, bg="white")
        btn_row.pack(anchor="e", pady=5)

        def delete_resource(res_id):
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("DELETE FROM classroom_resource_files WHERE resource_id=%s", (res_id,))
            c.execute("DELETE FROM classroom_resources WHERE id=%s", (res_id,))
            conn.commit()
            conn.close()
            open_classroom_resources(content_frame, classroom)

        def edit_resource(res):
            new_title = simpledialog.askstring("Edit Title", "New Title:", initialvalue=res['title'])
            new_desc = simpledialog.askstring("Edit Description", "New Description:", initialvalue=res['description'])

            if new_title:
                conn2 = get_db_connection()
                c2 = conn2.cursor()
                c2.execute("UPDATE classroom_resources SET title=%s, description=%s WHERE id=%s",
                           (new_title, new_desc, res['id']))
                conn2.commit()
                conn2.close()
                open_classroom_resources(content_frame, classroom)

        # tk.Button(btn_row, text="Edit", bg="#1976d2", fg="white", command=lambda r=r: edit_resource(r)).pack(side="left", padx=5)
        tk.Button(btn_row, text="Edit", bg="#1976d2", fg="white",
          command=lambda r=r: edit_resource_dialog(content_frame, r)).pack(side="left", padx=5)

        tk.Button(btn_row, text="Delete", bg="#d32f2f", fg="white", command=lambda rid=r['id']: delete_resource(rid)).pack(side="left", padx=5)

    conn.close()
    show_joined_students(content_frame, classroom)


def show_joined_students(content_frame, classroom):
    import tkinter as tk
    from db import get_db_connection

    # Clear previous student section if reloaded
    # (optional but clean)
    # for widget in content_frame.winfo_children():
    #     widget.destroy()

    tk.Label(content_frame, text="Students Joined", font=("Helvetica", 14, "bold")).pack(pady=5)

    student_list_frame = tk.Frame(content_frame, bg="white", padx=10, pady=10)
    student_list_frame.pack(fill="x", pady=5)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT s.name, s.student_id, s.intake, s.section
        FROM classroom_students cs
        JOIN student s ON cs.student_id = s.id
        WHERE cs.classroom_id=%s
        ORDER BY s.name ASC
    """, (classroom['id'],))
    students = cursor.fetchall()
    conn.close()

    if not students:
        tk.Label(student_list_frame, text="No students have joined yet.",
                 bg="white", fg="#777").pack(anchor="w", pady=3)
        return

    for st in students:
        row = tk.Frame(student_list_frame, bg="white")
        row.pack(fill="x", pady=2)

        tk.Label(row, text=f"{st['name']} ({st['student_id']})",
                 bg="white", font=("Arial", 10, "bold")).pack(side="left")

        tk.Label(row, text=f"  |  Intake: {st['intake']}  |  Section: {st['section']}",
                 bg="white", fg="#444").pack(side="left")

def edit_resource_dialog(content_frame, resource):
    import tkinter as tk
    from tkinter import filedialog, messagebox
    from db import get_db_connection
    import os

    # Dialog Window
    dlg = tk.Toplevel()
    dlg.title("Edit Resource")
    dlg.geometry("600x500")
    dlg.grab_set()  # modal

    tk.Label(dlg, text="Edit Resource", font=("Helvetica", 14, "bold")).pack(pady=10)

    # Title
    tk.Label(dlg, text="Title:").pack(anchor="w", padx=10)
    title_entry = tk.Entry(dlg, width=60)
    title_entry.pack(padx=10, pady=5)
    title_entry.insert(0, resource['title'])

    # Description
    tk.Label(dlg, text="Description:").pack(anchor="w", padx=10)
    desc_text = tk.Text(dlg, width=60, height=5)
    desc_text.pack(padx=10, pady=5)
    desc_text.insert("1.0", resource['description'] if resource['description'] else "")

    # Current Files
    tk.Label(dlg, text="Attached Files:").pack(anchor="w", padx=10, pady=(10,0))
    files_frame = tk.Frame(dlg)
    files_frame.pack(fill="both", expand=True, padx=10, pady=5)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM classroom_resource_files WHERE resource_id=%s", (resource['id'],))
    files = cursor.fetchall()
    conn.close()

    file_widgets = []

    def refresh_files():
        for w in file_widgets:
            w.destroy()
        file_widgets.clear()
        for f in files:
            row = tk.Frame(files_frame)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f['file_name']).pack(side="left")
            tk.Button(row, text="Delete", fg="red", command=lambda fid=f['id']: delete_file(fid)).pack(side="right")
            file_widgets.append(row)

    def delete_file(file_id):
        nonlocal files
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM classroom_resource_files WHERE id=%s", (file_id,))
        conn.commit()
        conn.close()
        files = [f for f in files if f['id'] != file_id]
        refresh_files()

    refresh_files()

    # Add New Files
    new_files = []

    def add_files():
        fs = filedialog.askopenfilenames()
        if fs:
            new_files.extend(fs)
            for fpath in fs:
                row = tk.Frame(files_frame)
                row.pack(fill="x", pady=2)
                tk.Label(row, text=os.path.basename(fpath)).pack(side="left")
                file_widgets.append(row)

    tk.Button(dlg, text="Add Files", bg="#00897b", fg="white", command=add_files).pack(pady=5)

    # Save Changes
    def save_changes():
        new_title = title_entry.get().strip()
        new_desc = desc_text.get("1.0", tk.END).strip()

        if not new_title:
            messagebox.showwarning("Warning", "Title is required")
            return

        conn = get_db_connection()
        c = conn.cursor()
        # Update title & description
        c.execute("UPDATE classroom_resources SET title=%s, description=%s WHERE id=%s",
                  (new_title, new_desc, resource['id']))
        # Insert new files
        for fpath in new_files:
            c.execute("INSERT INTO classroom_resource_files (resource_id, file_path, file_name) VALUES (%s, %s, %s)",
                      (resource['id'], fpath, os.path.basename(fpath)))
        conn.commit()
        conn.close()

        dlg.destroy()
        # Refresh main resource page
        open_classroom_resources(content_frame, {'id': resource['classroom_id'], 'name': '', 'subject': ''})

    tk.Button(dlg, text="Save Changes", bg="#004aad", fg="white", command=save_changes).pack(pady=10)
