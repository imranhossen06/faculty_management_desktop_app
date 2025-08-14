import tkinter as tk
import subprocess

# Faculty login
def faculty_login():
    subprocess.Popen(["python", "login.py"])

# Student menu
def student_menu():
    # প্রথম স্ক্রিন ক্লিয়ার
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Student Panel", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="Login", width=20, command=lambda: subprocess.Popen(["python", "login.py"])).pack(pady=5)
    tk.Button(root, text="Registration", width=20, command=lambda: subprocess.Popen(["python", "registration.py"])).pack(pady=5)

    tk.Button(root, text="Back", width=20, command=main_menu).pack(pady=20)

# Main menu
def main_menu():
    # প্রথম স্ক্রিন ক্লিয়ার
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Select which panel you want to access", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="Faculty", width=20, command=faculty_login).pack(pady=5)
    tk.Button(root, text="Student", width=20, command=student_menu).pack(pady=5)

# Tkinter window
root = tk.Tk()
root.title("Main Panel")
root.state('zoomed')

main_menu()

root.mainloop()
