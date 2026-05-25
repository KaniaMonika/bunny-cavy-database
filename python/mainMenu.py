import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
import sys
import subprocess
import io
from tkinter import filedialog

customer_id = int(sys.argv[1])

def openDelete():
    result = subprocess.run(["python", "deleteAccount.py", str(customer_id)])
    if result.returncode == 0:
        root.destroy() 
def openNewOrder():
    subprocess.run(["python", "newOrder.py", str(customer_id)])
def openMyOrders():
    subprocess.run(["python", "myOrders.py", str(customer_id)])

def upload_photo():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        with open(file_path, 'rb') as f:
            image_data = f.read()
        cursor.execute("UPDATE Customers SET pet_pic = ? WHERE customer_id = ?", (image_data, customer_id))
        conn.commit()
        root.destroy()  #refresh window to display the image
        subprocess.run(["python", sys.argv[0], str(customer_id)])

# DB connection
conn = sqlite3.connect("../database/assessment.db")
cursor = conn.cursor()

cursor.execute("SELECT first_name, email, pet_pic FROM Customers WHERE customer_id = ?", (customer_id,))
customer = cursor.fetchone()

root = tk.Tk()
root.title("Main Menu")
root.geometry("400x500")

if customer:
    firstName, email, pet_pic = customer

    #show pet picture if exists, else show "Add Photo" button
    if pet_pic:
        image = Image.open(io.BytesIO(pet_pic))
        image = image.resize((200, 200))
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(root, image=photo)
        label.image = photo
        label.pack(pady=10)
    else:
        tk.Label(root,text="Add a photo of your pet so he can accompany\n you while you choose his favorite snacks!").pack(pady=10)
        tk.Button(root, text="Add Photo", width=20, command=upload_photo).pack(pady=10)
    
    tk.Label(root, text=f"Welcome, {firstName}!").pack(pady=10)
    tk.Label(root, text=f"Email: {email}").pack(pady=10)
else:
    tk.Label(root, text="Customer not found").pack()

tk.Button(root, text="Make a new order", width=20, command=openNewOrder).pack(pady=10)
tk.Button(root, text="Check your orders", width=20, command=openMyOrders).pack(pady=10)
tk.Button(root, text="Delete account", width=20, command=openDelete).pack(pady=10)
tk.Button(root, text="Logout", width=20, command=root.destroy).pack(pady=10)

root.mainloop()
conn.close()
