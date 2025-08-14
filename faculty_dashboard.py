import tkinter as tk
from tkinter import ttk
from tkinter import font

# ================= Window Setup =================
root = tk.Tk()
root.title("Faculty Panel")
root.geometry("1100x650")
root.configure(bg="#f0f2f5")

def center(win):
    win.update_idletasks()
    w = win.winfo_width()
    h = win.winfo_height()
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# ================= Styles & Fonts =================
heading_font = font.Font(family="Helvetica", size=12, weight="bold")
big_font = font.Font(family="Helvetica", size=14, weight="bold")
small_font = font.Font(family="Helvetica", size=10)

style = ttk.Style()
style.theme_use('default')

# ================= Sidebar =================
sidebar = tk.Frame(root, bg="#0b4d2e", width=240)
sidebar.pack(side="left", fill="y")

# Logo area
logo_frame = tk.Frame(sidebar, bg="#0b4d2e")
logo_frame.pack(fill="x", pady=20)
logo_label = tk.Label(logo_frame, text="BUBT", bg="#0b4d2e", fg="white",
                      font=("Helvetica", 20, "bold"))
logo_label.pack(padx=20, anchor="w")
sub_label = tk.Label(logo_frame, text="FACULTY PANEL", bg="#0b4d2e", fg="#cfead7",
                     font=("Helvetica", 9))
sub_label.pack(padx=20, anchor="w")

# Menu buttons
menu_frame = tk.Frame(sidebar, bg="#0b4d2e")
menu_frame.pack(fill="both", expand=True, padx=10, pady=10)

menu_items = [
    ("Dashboard", lambda: print("Dashboard clicked")),
    ("Appointment", lambda: print("Appointment clicked")),
    ("Classroom", lambda: print("Classroom clicked")),
    ("Support", lambda: print("Support clicked")),
    ("Configuration", lambda: print("Configuration clicked"))
]

for text, cmd in menu_items:
    b = tk.Button(menu_frame, text=text, anchor="w", command=cmd,
                  bg="#0b4d2e", fg="white", relief="flat", bd=0,
                  activebackground="#0a3f24", padx=12)
    b.pack(fill="x", pady=6)

# small footer text
footer = tk.Label(sidebar, text="© 2025 BUBT", bg="#0b4d2e", fg="#a6d1c0", font=small_font)
footer.pack(side="bottom", pady=10)

# ================= Topbar =================
main_area = tk.Frame(root, bg="#f0f2f5")
main_area.pack(side="left", fill="both", expand=True)

topbar = tk.Frame(main_area, bg="white", height=70)
topbar.pack(fill="x")
topbar.pack_propagate(False)

greeting = tk.Label(topbar, text="Hello, Good Afternoon!", bg="white",
                    font=heading_font, anchor="w")
greeting.pack(side="left", padx=20)

# profile compact at top right
profile_frame = tk.Frame(topbar, bg="white")
profile_frame.pack(side="right", padx=20)
profile_name = tk.Label(profile_frame, text="John Doe", bg="white", font=big_font)
profile_role = tk.Label(profile_frame, text="LECTURER", bg="white", font=small_font, fg="#6c757d")
profile_name.pack(anchor="e")
profile_role.pack(anchor="e")

# ================= Content Area =================
content = tk.Frame(main_area, bg="#f0f2f5")
content.pack(fill="both", expand=True, padx=20, pady=10)

# Profile card
profile_card = tk.Frame(content, bg="white", bd=1, relief="solid", height=80)
profile_card.pack(fill="x", padx=10, pady=10)
profile_card.pack_propagate(False)

# inside profile card
left_profile = tk.Frame(profile_card, bg="white")
left_profile.pack(side="left", padx=10, pady=10)

avatar = tk.Canvas(left_profile, width=50, height=50, bg="white", highlightthickness=0)
avatar.create_oval(5, 5, 45, 45, fill="#cfead7", outline="#b6e0c9")
avatar.pack(side="left", padx=(0,10))

text_frame = tk.Frame(left_profile, bg="white")
text_frame.pack(side="left")
name_label = tk.Label(text_frame, text="John Doe", bg="white", font=big_font)
role_label = tk.Label(text_frame, text="LECTURER", bg="white", fg="#6c757d", font=small_font)
name_label.pack(anchor="w")
role_label.pack(anchor="w")

# right side of profile card (placeholder icons)
right_profile = tk.Frame(profile_card, bg="white")
right_profile.pack(side="right", padx=10, pady=10)
for i in range(3):
    dot = tk.Label(right_profile, text="⚙", bg="white", font=("Helvetica", 12))
    dot.pack(side="left", padx=6)

# ================= Stats cards area =================
stats_frame = tk.Frame(content, bg="#f0f2f5")
stats_frame.pack(fill="x", padx=10, pady=10)

# stats data (title, value, bg, icon)
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

# ================= Finalize =================
center(root)
root.mainloop()
