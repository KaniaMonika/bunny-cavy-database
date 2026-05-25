import tkinter as tk
import sqlite3
import sys
import subprocess


admin_id = int(sys.argv[1])

def ChangePaymentStatus():
    subprocess.run(["python", "changePaymentStatus.py",str(admin_id)])
def ChangeOrderStatus():
    subprocess.run(["python", "changeOrderStatus.py",str(admin_id)])
def CheckDetails():
    subprocess.run(["python", "checkDetails.py",str(admin_id)])
def ExportTable():
    subprocess.run(["python", "exportProductsToXML.py",str(admin_id)]) 
def Populate():
    subprocess.run(["python", "populateXMLForProduct.py",str(admin_id)])
# DB connection
conn = sqlite3.connect(r"c:\Users\kania\OneDrive\Desktop\Bunny&CavyBotanicals\database\assessment db")
cursor = conn.cursor()

cursor.execute("SELECT login FROM admin_credentials WHERE admin_id = ?", (admin_id,))
admin = cursor.fetchone()

root = tk.Tk()
root.title("Main Menu")
root.geometry("400x500")

if admin:
    tk.Label(root, text=f"Welcome Admin!").pack(pady=10)
else:
    tk.Label(root, text="Admin not found").pack()

tk.Button(root, text="Change Payment Status", width = 25, command=ChangePaymentStatus).pack(pady=10)
tk.Button(root, text="Change Order Status", width = 25, command=ChangeOrderStatus).pack(pady=10)
tk.Button(root, text="Contact Deatils to Customers", width = 25, command=CheckDetails).pack(pady=10)
tk.Button(root, text="Export Products to XML", width=25, command=ExportTable).pack(pady=10)
tk.Button(root, text="Populate XML for Product", width=25, command=Populate).pack(pady=10)
tk.Button(root, text="Logout", width = 25, command=root.destroy).pack(pady=10)

root.mainloop()
conn.close()