import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import font, messagebox


def open_faculty_pannel(root, faculty_name, faculty_designation, faculty_id):
    # ===== Clear previous widgets (from login page) =====
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Faculty Panel")
    root.geometry("1100x650")
    root.configure(bg="#f0f2f5")

    # Fonts & Styles
    heading_font = font.Font(family="Helvetica", size=12, weight="bold")
    big_font = font.Font(family="Helvetica", size=14, weight="bold")
    small_font = font.Font(family="Helvetica", size=10)

    # ================= Sidebar =================
    sidebar = tk.Frame(root, bg="#0b4d2e", width=240)
    sidebar.pack(side="left", fill="y")

    # ================= Main Area =================
    main_area = tk.Frame(root, bg="#f0f2f5")
    main_area.pack(side="left", fill="both", expand=True)

    # --- Topbar ---
    topbar = tk.Frame(main_area, bg="white", height=70)
    topbar.pack(fill="x")
    topbar.pack_propagate(False)

    greeting = tk.Label(topbar, text="Hello,\nGood Afternoon!", bg="white", anchor="w",
                        font=heading_font)
    greeting.pack(side="left", padx=20)

    profile_frame = tk.Frame(topbar, bg="white")
    profile_frame.pack(side="right", padx=20)
    profile_name = tk.Label(profile_frame, text=faculty_name, bg="white", font=big_font)
    profile_role = tk.Label(profile_frame, text=faculty_designation, bg="white", font=small_font, fg="#6c757d")
    profile_name.pack(anchor="e")
    profile_role.pack(anchor="e")

    # --- Content area (dynamic load হবে) ---
    content = tk.Frame(main_area, bg="#f0f2f5")
    content.pack(fill="both", expand=True, padx=20, pady=10)

    # ================= Helper functions =================
    def clear_content():
        for w in content.winfo_children():
            w.destroy()

    # ---------------- Dashboard ----------------
    def show_dashboard():
        clear_content()

        tk.Label(content, text="📊 Dashboard", font=big_font, bg="#f0f2f5").pack(anchor="w")

        stats = [
            ("👨‍🎓 Total Appointment", "120"),
            ("📅 Appointments", "15"),
            ("🏫 Pending", "8"),
            ("💬 Approved", "23"),
            ("💬 Rejected", "4"),
            ("💬 Canceled", "2"),
        ]

        grid = tk.Frame(content, bg="#f0f2f5")
        grid.pack(fill="both", expand=True, padx=20, pady=20)

        def make_stat_card(parent, title, value):
            card = tk.Frame(parent, bg="white", width=220, height=120, relief="raised", bd=1)
            card.pack_propagate(False)

            tk.Label(card, text=title, font=("Helvetica", 12), bg="white", fg="#555").pack(pady=(15, 5))
            tk.Label(card, text=value, font=("Helvetica", 20, "bold"), bg="white", fg="#0b4d2e").pack()

            return card

        for i, (title, value) in enumerate(stats):
            card = make_stat_card(grid, title, value)
            card.grid(row=0, column=i, padx=12, pady=12, sticky="nsew")

        for i in range(len(stats)):
            grid.grid_columnconfigure(i, weight=1)

    # ---------------- Counselling Hours ----------------
    def show_counselling_hours():
        clear_content()
        tk.Label(content, text="🕒 Counselling Hours", font=big_font, bg="#f0f2f5").pack(anchor="w")

        # Default data
        days = [
            ("Monday", "Open", "9:00 AM - 5:00 PM"),
            ("Tuesday", "Open", "10:00 AM - 4:00 PM"),
            ("Wednesday", "Open", "11:00 AM - 6:00 PM"),
            ("Thursday", "Open", "9:00 AM - 5:00 PM"),
            ("Friday", "Closed", ""),
            ("Saturday", "Open", "12:00 PM - 3:00 PM"),
            ("Sunday", "Closed", ""),
        ]

        grid = tk.Frame(content, bg="#f0f2f5")
        grid.pack(fill="both", expand=True, padx=10, pady=10)

        entries = {}  # store {day: (status_var, entry)}

        for i, (day, status, time) in enumerate(days):
            # --- Card ---
            card = tk.Frame(grid, bg="white", relief="raised", bd=1, width=300, height=100)
            card.grid(row=i // 2, column=i % 2, padx=12, pady=12, sticky="nsew")
            card.pack_propagate(False)

            # Day name
            tk.Label(card, text=day, font=("Helvetica", 12, "bold"), bg="white", fg="#0b4d2e").pack(anchor="w", padx=10, pady=(8, 4))

            inner = tk.Frame(card, bg="white")
            inner.pack(fill="x", padx=10)

            # Status dropdown
            status_var = tk.StringVar(value=status)
            status_menu = tk.OptionMenu(inner, status_var, "Open", "Closed")
            status_menu.config(width=7, bg="#0b4d2e", fg="white", relief="flat")
            status_menu.pack(side="left", padx=(0, 10))

            # Time entry
            time_entry = tk.Entry(inner, width=20)
            time_entry.insert(0, time)
            time_entry.pack(side="left")

            entries[day] = (status_var, time_entry)

    def save_hours():
        updated = {}
        for day, (status_var, entry) in entries.items():
            status = status_var.get()
            time = entry.get() if status == "Open" else "Closed"
            updated[day] = {"status": status, "time": time}

        messagebox.showinfo("Saved", f"Counselling hours updated:\n{updated}")

        tk.Button(content, text="💾 Save Changes", command=save_hours, bg="#0b4d2e", fg="white",
                relief="flat", padx=12, pady=6).pack(pady=15)


    # Default data
    days = [
        ("Monday", "Open", "9:00 AM - 5:00 PM"),
        ("Tuesday", "Open", "10:00 AM - 4:00 PM"),
        ("Wednesday", "Open", "11:00 AM - 6:00 PM"),
        ("Thursday", "Open", "9:00 AM - 5:00 PM"),
        ("Friday", "Closed", ""),
        ("Saturday", "Open", "12:00 PM - 3:00 PM"),
        ("Sunday", "Closed", ""),
    ]

    grid = tk.Frame(content, bg="#f0f2f5")
    grid.pack(fill="both", expand=True, padx=10, pady=10)

    entries = {}  # store {day: (status_var, entry)}

    for i, (day, status, time) in enumerate(days):
        # --- Card ---
        card = tk.Frame(grid, bg="white", relief="raised", bd=1, width=300, height=100)
        card.grid(row=i // 2, column=i % 2, padx=12, pady=12, sticky="nsew")
        card.pack_propagate(False)

        # Day name
        tk.Label(card, text=day, font=("Helvetica", 12, "bold"), bg="white", fg="#0b4d2e").pack(anchor="w", padx=10, pady=(8, 4))

        inner = tk.Frame(card, bg="white")
        inner.pack(fill="x", padx=10)

        # Status dropdown
        status_var = tk.StringVar(value=status)
        status_menu = tk.OptionMenu(inner, status_var, "Open", "Closed")
        status_menu.config(width=7, bg="#0b4d2e", fg="white", relief="flat")
        status_menu.pack(side="left", padx=(0, 10))

        # Time entry
        time_entry = tk.Entry(inner, width=20)
        time_entry.insert(0, time)
        time_entry.pack(side="left")

        entries[day] = (status_var, time_entry)

    def save_hours():
        updated = {}
        for day, (status_var, entry) in entries.items():
            status = status_var.get()
            time = entry.get() if status == "Open" else "Closed"
            updated[day] = {"status": status, "time": time}

        messagebox.showinfo("Saved", f"Counselling hours updated:\n{updated}")

        tk.Button(content, text="💾 Save Changes", command=save_hours, bg="#0b4d2e", fg="white",
              relief="flat", padx=12, pady=6).pack(pady=15)

    # ================= Sidebar Menu =================
    menu_items = [
        ("Dashboard", show_dashboard),
        ("Appointment", lambda: print("Appointment clicked")),
        ("Classroom", lambda: print("Classroom clicked")),
        ("Support", lambda: print("Support clicked")),
        ("Configuration", lambda: print("Configuration clicked")),
        ("Counselling Hours", show_counselling_hours),
    ]

    for text, cmd in menu_items:
        b = tk.Button(sidebar, text=text, anchor="w", command=cmd,
                      bg="#0b4d2e", fg="white", relief="flat", bd=0,
                      activebackground="#0a3f24", padx=12)
        b.pack(fill="x", pady=6)

    # Default view = Dashboard
    show_dashboard()
