import tkinter as tk
from tkinter import ttk, font

def open_faculty_dashboard(root, user, main_menu_callback):
    root.title(f"Faculty Dashboard - {user['name']}")

    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    # ================= Styles & Fonts =================
    heading_font = font.Font(family="Helvetica", size=12, weight="bold")
    big_font = font.Font(family="Helvetica", size=14, weight="bold")
    small_font = font.Font(family="Helvetica", size=10)

    # ================= Sidebar =================
    sidebar = tk.Frame(root, bg="#0b4d2e", width=240)
    sidebar.pack(side="left", fill="y")

    logo_frame = tk.Frame(sidebar, bg="#0b4d2e")
    logo_frame.pack(fill="x", pady=20)
    logo_label = tk.Label(logo_frame, text="BUBT", bg="#0b4d2e", fg="white", font=("Helvetica", 20, "bold"))
    logo_label.pack(padx=20, anchor="w")
    sub_label = tk.Label(logo_frame, text="FACULTY PANEL", bg="#0b4d2e", fg="#cfead7", font=("Helvetica", 9))
    sub_label.pack(padx=20, anchor="w")

    # ================= Content Area =================
    main_area = tk.Frame(root, bg="#f0f2f5")
    main_area.pack(side="left", fill="both", expand=True)

    topbar = tk.Frame(main_area, bg="white", height=70)
    topbar.pack(fill="x")
    topbar.pack_propagate(False)

    greeting = tk.Label(topbar, text=f"Hello, {user['name']}!", bg="white", font=heading_font, anchor="w")
    greeting.pack(side="left", padx=20)

    profile_frame = tk.Frame(topbar, bg="white")
    profile_frame.pack(side="right", padx=20)
    profile_name = tk.Label(profile_frame, text=user['name'], bg="white", font=big_font)
    profile_role = tk.Label(profile_frame, text=user.get('designation','LECTURER'), bg="white", font=small_font, fg="#6c757d")
    profile_name.pack(anchor="e")
    profile_role.pack(anchor="e")

    content_frame = tk.Frame(main_area, bg="#f0f2f5")
    content_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # ================= Functional Menu Buttons =================
    def show_dashboard():
        for widget in content_frame.winfo_children():
            widget.destroy()
        
        # Dashboard cards
        stats_frame = tk.Frame(content_frame, bg="#f0f2f5")
        stats_frame.pack(fill="x", padx=10, pady=10)

        stats = [
            ("In Total", "30", "#ffffff", "📊"),
            ("Approved", "25", "#e7f9ef", "✅"),
            ("Pending", "2", "#fff7e6", "⏳"),
            ("Rejected", "2", "#ffecec", "❌"),
            ("Cancelled", "1", "#f0f0f0", "🚫")
        ]

        def make_card(parent, title, value, bg, icon="📊"):
            card = tk.Frame(parent, bg=bg, bd=0, relief="ridge", width=170, height=90)
            card.pack_propagate(False)
            icon_lbl = tk.Label(card, text=icon, bg=bg, font=("Helvetica", 14))
            icon_lbl.pack(anchor="w", padx=10, pady=(10,0))
            title_lbl = tk.Label(card, text=title, bg=bg, font=small_font)
            title_lbl.pack(anchor="w", padx=10)
            value_lbl = tk.Label(card, text=value, bg=bg, font=("Helvetica", 18, "bold"))
            value_lbl.pack(anchor="w", padx=10, pady=(0,10))
            return card

        for t, v, c, i in stats:
            ccard = make_card(stats_frame, t, v, c, i)
            ccard.pack(side="left", padx=8)

        # Placeholder label under cards
        tk.Label(content_frame, text="Additional Dashboard Info Here", bg="#f0f2f5", font=big_font).pack(pady=20)

    def show_appointment():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(content_frame, text="Appointment Content", font=big_font, bg="#f0f2f5").pack(pady=20)

    def show_classroom():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(content_frame, text="Classroom Content", font=big_font, bg="#f0f2f5").pack(pady=20)

    def show_counselling():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(content_frame, text="Counselling Hours Content", font=big_font, bg="#f0f2f5").pack(pady=20)

    def show_support():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(content_frame, text="Support Content", font=big_font, bg="#f0f2f5").pack(pady=20)

    def show_configuration():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(content_frame, text="Configuration Content", font=big_font, bg="#f0f2f5").pack(pady=20)

    menu_items = [
        ("Dashboard", show_dashboard),
        ("Appointment", show_appointment),
        ("Classroom", show_classroom),
        ("Counselling Hours", show_counselling),
        ("Support", show_support),
        ("Configuration", show_configuration)
    ]

    for text, cmd in menu_items:
        b = tk.Button(sidebar, text=text, anchor="w", command=cmd,
                      bg="#0b4d2e", fg="white", relief="flat", bd=0,
                      activebackground="#0a3f24", padx=12)
        b.pack(fill="x", pady=6)

    # Logout button below menu
    logout_btn = tk.Button(sidebar, text="Logout / Main Menu", anchor="w",
                           bg="#f44336", fg="white", relief="flat", bd=0,
                           font=small_font, command=main_menu_callback)
    logout_btn.pack(fill="x", pady=20, padx=12, side="bottom")

    # Initially show dashboard content
    show_dashboard()
