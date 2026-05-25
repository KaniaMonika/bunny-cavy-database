import tkinter as tk
import sqlite3
import sys

customer_id = int(sys.argv[1])

# DB connection
conn = sqlite3.connect("../database/assessment.db")
cursor = conn.cursor()

class OrderSummaryWindow:
    def __init__(self, master, customer_id):
        self.master = master
        self.master.title("Your Orders")
        self.master.geometry("600x400")
        self.customer_id = customer_id

        tk.Label(master, text="Your Orders", font=("Helvetica", 14, "bold")).pack(pady=5)

        self.tree = tk.Listbox(master, width=80)
        self.tree.pack(pady=10)

        self.orders = self.get_orders()

        for order in self.orders:
            summary = f"Order #{order['order_id']} | {order['order_date']} | £{order['total_price']} | Status: {order['order_status']}"
            self.tree.insert(tk.END, summary)

        self.tree.bind("<<ListboxSelect>>", self.show_items)

        self.details_label = tk.Label(master, text="", font=("Helvetica", 10))
        self.details_label.pack(pady=10)

    def get_orders(self):
        cursor.execute("""
            SELECT order_id, order_date, total_price, order_status
            FROM Orders
            WHERE customer_id = ?
            ORDER BY order_date DESC
        """, (self.customer_id,))
        rows = cursor.fetchall()
        return [
            {
                "order_id": row[0],
                "order_date": row[1],
                "total_price": round(row[2], 2),
                "order_status": row[3]
            } for row in rows
        ]

    def show_items(self, event):
        selection = self.tree.curselection()
        if not selection:
            return
        index = selection[0]
        order_id = self.orders[index]['order_id']

        cursor.execute("""
            SELECT P.prod_name, O.qty
            FROM Ordered_items O
            JOIN Product P ON O.product_id = P.ProdID
            WHERE O.order_id = ?
        """, (order_id,))
        items = cursor.fetchall()

        detail_text = f"Items in Order #{order_id}:\n"
        for name, qty in items:
            detail_text += f" {name} - Qty: {qty}\n"

        self.details_label.config(text=detail_text)

# Launch window
if __name__ == "__main__":
    root = tk.Tk()
    app = OrderSummaryWindow(root, customer_id)
    root.mainloop()
    conn.close()
