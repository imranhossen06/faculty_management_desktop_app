import tkinter as tk
from tkinter import messagebox

# Function for login check
def login():
    username = username_entry.get()
    password = password_entry.get()
    dob = f"{day_var.get()}-{month_var.get()}-{year_var.get()}"
    gender = gender_var.get()

    if username == "admin" and password == "1234":
        messagebox.showinfo("Registration Successful", f"Welcome, Admin!\nGender: {gender}\nDOB: {dob}")
    else:
        messagebox.showerror("Registration Failed", "Invalid username or password")

# Create main window
root = tk.Tk()
root.title("Registration Page")
root.geometry("500x400")

# Username label and entry
tk.Label(root, text="Username").pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack()

# Password label and entry
tk.Label(root, text="Password").pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# Gender selection
tk.Label(root, text="Gender").pack(pady=5)
gender_var = tk.StringVar(value="")
tk.Radiobutton(root, text="Male", variable=gender_var, value="Male").pack()
tk.Radiobutton(root, text="Female", variable=gender_var, value="Female").pack()

# Date of Birth
tk.Label(root, text="Date of Birth").pack(pady=5)

day_var = tk.StringVar(value="Day")
month_var = tk.StringVar(value="Month")
year_var = tk.StringVar(value="Year")

days = [str(i) for i in range(1, 32)]
months = [str(i) for i in range(1, 13)]
years = [str(i) for i in range(1950, 2025)]

dob_frame = tk.Frame(root)
dob_frame.pack(pady=5)

tk.OptionMenu(dob_frame, day_var, *days).pack(side=tk.LEFT, padx=5)
tk.OptionMenu(dob_frame, month_var, *months).pack(side=tk.LEFT, padx=5)
tk.OptionMenu(dob_frame, year_var, *years).pack(side=tk.LEFT, padx=5)

# Login button
tk.Button(root, text="Sign Up", command=login).pack(pady=15)

root.mainloop()

