import tkinter as tk
from tkinter import ttk, font, messagebox
from db import get_db_connection

def show_counselling_hours(content_frame, faculty_id):
    # Clear previous widgets
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    heading_font = font.Font(family="Helvetica", size=12, weight="bold")
    tk.Label(content_frame, text="Counselling Hours", font=("Helvetica", 16, "bold"), bg="#f0f2f5").pack(pady=10)

    # Fetch weekly_days dynamically
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM weekly_days ORDER BY id")
    weekly_days = cursor.fetchall()
    
    # Fetch existing counselling_slots for faculty
    cursor.execute("""
        SELECT cs.*, wd.id as day_id, wd.name as day_name
        FROM counselling_slots cs
        JOIN weekly_days wd ON cs.weekly_days_id = wd.id
        WHERE cs.faculty_id = %s
    """, (faculty_id,))
    db_rows = cursor.fetchall()
    cursor.close()
    conn.close()

    db_map = {row['weekly_days_id']: row for row in db_rows}

    table_frame = tk.Frame(content_frame, bg="#f0f2f5")
    table_frame.pack(padx=10, pady=10, fill="x")

    # Table headers
    headers = ["Day", "Start Time", "End Time", "Available"]
    for i, h in enumerate(headers):
        tk.Label(table_frame, text=h, font=heading_font, bg="#d9edf7", width=15, relief="ridge").grid(row=0, column=i, sticky="nsew")

    # Create rows dynamically from weekly_days
    row_vars = []
    for idx, day in enumerate(weekly_days, start=1):
        tk.Label(table_frame, text=day['name'], bg="#f0f2f5", width=15, relief="ridge").grid(row=idx, column=0, sticky="nsew")
        
        db_row = db_map.get(day['id'])
        if db_row:
            start_val = db_row['start_time'] if db_row['start_time'] else ""
            end_val = db_row['end_time'] if db_row['end_time'] else ""
            avail_val = bool(db_row['is_active'])
        else:
            start_val = "09:00"
            end_val = "17:00"
            avail_val = True

        start_var = tk.StringVar(value=start_val)
        end_var = tk.StringVar(value=end_val)
        available_var = tk.BooleanVar(value=avail_val)

        start_entry = tk.Entry(table_frame, textvariable=start_var, width=15)
        start_entry.grid(row=idx, column=1, sticky="nsew")
        end_entry = tk.Entry(table_frame, textvariable=end_var, width=15)
        end_entry.grid(row=idx, column=2, sticky="nsew")

        def toggle_time(e_var=available_var, s_entry=start_entry, e_entry=end_entry):
            if e_var.get():
                s_entry.config(state="normal")
                e_entry.config(state="normal")
            else:
                s_entry.delete(0, tk.END)
                e_entry.delete(0, tk.END)
                s_entry.config(state="disabled")
                e_entry.config(state="disabled")

        cb = tk.Checkbutton(table_frame, variable=available_var, command=toggle_time, bg="#f0f2f5")
        cb.grid(row=idx, column=3)
        toggle_time()  # initialize state
        row_vars.append({
            "weekly_days_id": day['id'],
            "start_var": start_var,
            "end_var": end_var,
            "available_var": available_var
        })

    # Save button
    def save_hours():
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            for row in row_vars:
                start_time = row["start_var"].get() if row["available_var"].get() else None
                end_time = row["end_var"].get() if row["available_var"].get() else None
                is_active = 1 if row["available_var"].get() else 0
                weekly_days_id = row["weekly_days_id"]

                cursor.execute("""
                    INSERT INTO counselling_slots
                    (faculty_id, weekly_days_id, start_time, end_time, is_active, created_at)
                    VALUES (%s, %s, %s, %s, %s, NOW())
                    ON DUPLICATE KEY UPDATE
                        start_time = VALUES(start_time),
                        end_time = VALUES(end_time),
                        is_active = VALUES(is_active),
                        created_at = NOW()
                """, (faculty_id, weekly_days_id, start_time, end_time, is_active))
            
            conn.commit()
            messagebox.showinfo("Saved", "Counselling hours saved successfully!")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Error saving counselling hours: {e}")
        finally:
            cursor.close()
            conn.close()

    tk.Button(content_frame, text="Save", bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"),
              command=save_hours).pack(pady=15)
