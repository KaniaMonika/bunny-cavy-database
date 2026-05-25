import tkinter as tk
from utils import apply_theme
import subprocess



def openLogin():
    subprocess.run(["python","login.py"])
    root.destroy()

def openRegister():
    subprocess.run(["python","register.py"])
    root.destroy()

root = tk.Tk()
root.title("Login Menu")
root.geometry("300x200")

tk.Label(root, text="Welcome").pack(pady=10)
tk.Button(root, text="Login", width = 20, command=openLogin).pack(pady=10)
tk.Button(root, text="Register", width = 20, command=openRegister).pack(pady=10)
tk.Button(root, text="Exit", width = 20, command=root.destroy).pack(pady=10)
apply_theme(root, bg="#e6f2ff", fg="#003366")


root.mainloop()