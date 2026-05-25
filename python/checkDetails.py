import tkinter as tk
from tkinter import ttk
import sqlite3
import sys

admin_id = int(sys.argv[1])

# DB connection
conn = sqlite3.connect(r"c:\Users\kania\OneDrive\Desktop\Bunny&CavyBotanicals\database\assessment db")
cursor = conn.cursor()

root = tk.Tk()
root.title("Customer Contact Details")
root.geometry("1000x500")

#treeview setup
columns = ("customer_id", "first_name", "last_name", "email", "phone", "address", "postcode", "city")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(fill="both", expand=True)

#SQL JOIN query to fetch contact details
query = """
SELECT c.customer_id, c.first_name, c.last_name, c.email, c.phone, c.address_first_line,
       IFNULL(p.Postcode, 'N/A') AS Postcode, IFNULL(ci.City_name, 'N/A') AS City
FROM Customers c
LEFT JOIN Postcode p ON c.postcode = p.PostcodeID
LEFT JOIN City ci ON p.CityID = ci.CityID
"""

cursor.execute(query)
rows = cursor.fetchall()

#insert data into treeview
for row in rows:
    tree.insert("", "end", values=row)

root.mainloop()
conn.close()
