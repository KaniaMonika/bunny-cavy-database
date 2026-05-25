import tkinter as tk
import bcrypt
import sqlite3
from tkinter import messagebox
import sys


customer_id = int(sys.argv[1])
# DB connection
conn = sqlite3.connect("../database/assessment.db")
cursor = conn.cursor()

def on_window_close():
    sys.exit(1)

def delete_account(customer_id):
    entered_password = delete_password_entry.get().strip()

    cursor.execute("SELECT password FROM login_credentials WHERE customer_id = ?", (customer_id,))
    result = cursor.fetchone()

    if result:
        db_hashed_password = result[0]
        #ensure db_hashed_password is bytes (if stored as TEXT, it might be string)
        if isinstance(db_hashed_password, str):
            db_hashed_password = db_hashed_password.encode('utf-8')
        #compare the entered password with the stored hash
        if bcrypt.checkpw(entered_password.encode('utf-8'), db_hashed_password):
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete your account?")
            if confirm:
                try:
                    cursor.execute("DELETE FROM login_credentials WHERE customer_id = ?", (customer_id,))
                    cursor.execute("DELETE FROM Customers WHERE customer_id = ?", (customer_id,))
                    conn.commit()
                    messagebox.showinfo("Deleted", "Your account has been deleted.")
                    root.destroy()
                    sys.exit(0)
                except Exception as e:
                    messagebox.showerror("Error", f"Account cannot be deleted.\n{e}")
        else:
            messagebox.showerror("Error", "Incorrect password.")
            sys.exit(1)
    else:
        messagebox.showerror("Error", "User not found.")
        sys.exit(1)


root = tk.Tk()
root.title("Delete Account")
root.geometry("300x200")

tk.Label(root, text="Confirm password to delete account").pack(pady=10)
delete_password_entry = tk.Entry(root, show="*")
delete_password_entry.pack()
tk.Button(root, text="Delete account", width = 20, command=lambda: delete_account(customer_id)).pack(pady=10)
root.protocol("WM_DELETE_WINDOW", on_window_close)
root.mainloop()