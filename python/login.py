import tkinter as tk
import sqlite3
import bcrypt
from tkinter import messagebox
import subprocess

#connecting to the database
conn = sqlite3.connect("../database/assessment.db")
cursor = conn.cursor()

#create the main GUI window
root = tk.Tk()
root.title("Login Form")
root.geometry("300x180")

#user name field
tk.Label(root, text="Username").pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack()

#password field
tk.Label(root, text="Password").pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack()

#checkbox to choose Admin login
is_admin = tk.BooleanVar()
tk.Checkbutton(root, text="Login as Admin", variable=is_admin).pack(pady=5)

def signin_click():
    username = username_entry.get()
    password = password_entry.get()
    admin_login = is_admin.get()

    if not username or not password:
        messagebox.showerror("Error", "Please fill both fields")
        return

    if admin_login:
        #query admin_credentials table
        cursor.execute("SELECT admin_id, password FROM admin_credentials WHERE login=?", (username,))
    else:
        # Query login_credentials table
        cursor.execute("SELECT customer_id, password FROM login_credentials WHERE login=?", (username,))

    result = cursor.fetchone()

    if result:
        user_id, db_hashed_password = result
        if bcrypt.checkpw(password.encode('utf-8'), db_hashed_password):
            messagebox.showinfo("Success", "Welcome! Logged in successfully")
            root.destroy()
            #launch different script for admin or customer
            if admin_login:
                subprocess.run(["python", "adminMenu.py", str(user_id)])
            else:
                subprocess.run(["python", "mainMenu.py", str(user_id)])
        else:
            messagebox.showerror("Error", "Wrong password")
    else:
        messagebox.showerror("Error", "Username not found")

#button to trigger login
tk.Button(root, text="Sign In", command=signin_click).pack(pady=10)

#run the application
root.mainloop()

#close the database connection
conn.close()
