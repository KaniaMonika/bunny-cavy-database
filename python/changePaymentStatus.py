import tkinter as tk
from tkinter import ttk
import sqlite3
import sys

# Get admin_id from arguments
admin_id = int(sys.argv[1])

# DB connection
conn = sqlite3.connect(r"c:\Users\kania\OneDrive\Desktop\Bunny&CavyBotanicals\database\assessment db")
cursor = conn.cursor()

root = tk.Tk()
root.title("Change Payment Status")
root.geometry("1000x500")

# Create a main frame
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Treeview (left side)
tree_frame = tk.Frame(main_frame)
tree_frame.pack(side="left", fill="both", expand=True)

columns = ("order_id", "customer_id", "order_date", "total_price", "payment_status", "order_status")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(fill="both", expand=True)

# Function to refresh orders
def refresh_orders():
    tree.delete(*tree.get_children())
    cursor.execute("SELECT order_id, customer_id, order_date, total_price, payment_status, order_status FROM Orders")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

refresh_orders()

# Buttons (right side)
button_frame = tk.Frame(main_frame)
button_frame.pack(side="right", fill="y")

def change_status(order_id):
    cursor.execute("UPDATE Orders SET payment_status = 'Completed' WHERE order_id = ?", (order_id,))
    conn.commit()
    refresh_orders()

# Create buttons for pending orders
cursor.execute("SELECT order_id FROM Orders WHERE payment_status = 'Pending'")
for (order_id,) in cursor.fetchall():
    btn = tk.Button(button_frame, text=f"Complete Payment {order_id}", width=20, command=lambda oid=order_id: change_status(oid))
    btn.pack(padx=5, pady=5)

root.mainloop()
conn.close()
