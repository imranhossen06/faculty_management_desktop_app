import tkinter as tk
from faculty import faculty
from student import student

root = tk.Tk()
root.title("Academic Management System")
root.state('zoomed')

def main_menu(root):
    for widget in root.winfo_children():
        widget.destroy()
    
    root.configure(bg="#004225")
    tk.Label(root, text="Academic Management System", font=("Helvetica", 32, "bold"), bg="#004225", fg="white").pack(pady=50)

    def create_button(text, bg_color, hover_color, command):
        btn = tk.Button(root, text=text, font=("Helvetica", 14, "bold"),
                        bg=bg_color, fg="white", width=22, height=2, bd=0, command=command, cursor="hand2")
        btn.pack(pady=20)
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
        return btn

    create_button("Faculty", "#4CAF50", "#45a049", lambda: faculty.faculty_login(root, main_menu))
    
    
    create_button("Student", "#2196F3", "#1e88e5", lambda: student.student_login(root, main_menu))

    tk.Label(root, text="© 2025 Academic Management System", font=("Helvetica", 10), bg="#004225", fg="white").pack(side=tk.BOTTOM, pady=15)

main_menu(root)
root.mainloop()
