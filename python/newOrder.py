import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime
import sys

conn = sqlite3.connect(r"c:\Users\kania\OneDrive\Desktop\Bunny&CavyBotanicals\database\assessment db")
cursor = conn.cursor()

class OrderWindow:
    def __init__(self, master, customer_id):
        self.master = master
        self.customer_id = customer_id
        self.master.title("Make an Order")
        self.master.geometry("420x500")
        self.category_var = tk.StringVar()
        self.category_dict = {}
        self.qty_vars = {}
        self.basket = []

        self.build_ui()

    def build_ui(self):
        tk.Label(self.master, text="Select a Category:", font=("Helvetica", 12)).pack(pady=5)
        self.category_dropdown = ttk.Combobox(self.master, textvariable=self.category_var, state="readonly")
        self.category_dropdown.pack()

        self.category_dropdown['values'] = self.load_categories()
        tk.Button(self.master, text="Show Products", command=self.show_products).pack(pady=10)
        tk.Button(self.master, text="Go to Basket", command=self.open_basket, bg="#FFA500", fg="white").pack(pady=10)

        self.products_frame = tk.Frame(self.master)
        self.products_frame.pack(fill="both", expand=True)


    def load_categories(self):
        cursor.execute("SELECT CategoryID, Category_name FROM Category")
        results = cursor.fetchall()
        self.category_dict = {name: cid for cid, name in results}
        return list(self.category_dict.keys())

    def show_products(self):
        for widget in self.products_frame.winfo_children():
            widget.destroy()
        self.qty_vars.clear()

        selected_category = self.category_var.get()
        if not selected_category:
            return

        cat_id = self.category_dict[selected_category]
        cursor.execute("""
            SELECT ProdID, prod_name, selling_price, product_weight_grams 
            FROM Product 
            WHERE category_id = ? AND sellable = 'YES'
        """, (cat_id,))
        products = cursor.fetchall()

        headers = ["Product", "Price (£)", "Weight (g)", "Quantity", "Add"]
        for i, h in enumerate(headers):
            tk.Label(self.products_frame, text=h, font=("Helvetica", 10, "bold")).grid(row=0, column=i, padx=5, pady=5)

        for idx, (prod_id, name, price, weight) in enumerate(products, start=1):
            tk.Label(self.products_frame, text=name).grid(row=idx, column=0)
            tk.Label(self.products_frame, text=price).grid(row=idx, column=1)
            tk.Label(self.products_frame, text=weight).grid(row=idx, column=2)

            qty_var = tk.IntVar(value=0)
            self.qty_vars[prod_id] = qty_var

            tk.Button(self.products_frame, text="-", command=lambda v=qty_var: self.adjust_qty(v, -1)).grid(row=idx, column=3, sticky="w")
            tk.Label(self.products_frame, textvariable=qty_var, width=3).grid(row=idx, column=3)
            tk.Button(self.products_frame, text="+", command=lambda v=qty_var: self.adjust_qty(v, 1)).grid(row=idx, column=3, sticky="e")

            tk.Button(self.products_frame, text="Add", command=lambda pid=prod_id: self.add_to_basket(pid)).grid(row=idx, column=4)

    def adjust_qty(self, var, delta):
        value = var.get() + delta
        var.set(max(value, 0))

    def add_to_basket(self, product_id):
        qty = self.qty_vars[product_id].get()
        if qty < 1:
            messagebox.showwarning("Quantity Needed", "Select at least 1 item.")
            return

        #check if already in basket
        for item in self.basket:
            if item["product_id"] == product_id:
                item["qty"] += qty
                break
        else:
            self.basket.append({"product_id": product_id, "qty": qty})

        messagebox.showinfo("Added", f"Added to basket.\nItems in basket: {len(self.basket)}")
        self.qty_vars[product_id].set(0)

    def open_basket(self):
        if not self.basket:
            messagebox.showinfo("Empty Basket", "No items added yet.")
            return
        BasketWindow(self.master, self.customer_id, self.basket)

class BasketWindow:
    def __init__(self, master, customer_id, basket):
        self.top = tk.Toplevel(master)
        self.top.geometry("400x400")
        self.top.title("Your Basket")
        self.customer_id = customer_id
        self.basket = basket
        tk.Label(self.top, text="Items in Your Basket", font=("Helvetica", 12)).pack(pady=10)

        self.frame = tk.Frame(self.top)
        self.frame.pack()
        self.total_label = tk.Label(self.top, text="", font=("Helvetica", 10, "bold"))
        self.total_label.pack(pady=5)
        self.update_total()


        self.refresh_view()

        tk.Button(self.top, text="Checkout", command=self.checkout, bg="#4CAF50", fg="white").pack(pady=10)

    def refresh_view(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        for idx, item in enumerate(self.basket):
            product_id = item["product_id"]
            cursor.execute("SELECT prod_name FROM Product WHERE ProdID = ?", (product_id,))
            name = cursor.fetchone()[0]

            tk.Label(self.frame, text=name).grid(row=idx, column=0)
            tk.Label(self.frame, text=f"Qty: {item['qty']}").grid(row=idx, column=1)
            tk.Button(self.frame, text="Remove", command=lambda i=idx: self.remove_item(i)).grid(row=idx, column=2)

    def remove_item(self, index):
        del self.basket[index]
        self.refresh_view()
        self.update_total()


    def update_total(self):
        total = 0.0
        for item in self.basket:
            cursor.execute("SELECT selling_price FROM Product WHERE ProdID = ?", (item["product_id"],))
            price = cursor.fetchone()[0]
            total += price * item["qty"]
        self.total_label.config(text=f"Total: £{round(total, 2)}")


    def checkout(self):
        if not self.basket:
            messagebox.showwarning("Basket Empty", "Add products first.")
            return

        order_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Calculate total price
        total_price = 0.0
        for item in self.basket:
            cursor.execute("SELECT selling_price FROM Product WHERE ProdID = ?", (item["product_id"],))
            price = cursor.fetchone()[0]
            total_price += price * item["qty"]

        try:
            cursor.execute("""
                INSERT INTO Orders (
                    customer_id, order_date, total_price, payment_status, order_status
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                self.customer_id,
                order_date,
                round(total_price, 2),
                "Pending",
                "processing"
            ))

            order_id = cursor.lastrowid

            for item in self.basket:
                cursor.execute("""
                    INSERT INTO Ordered_items (order_id, product_id, qty)
                    VALUES (?, ?, ?)
                """, (order_id, item["product_id"], item["qty"]))

            conn.commit()
            messagebox.showinfo("Success", f"Order placed! Total: £{round(total_price, 2)}")
            self.top.destroy()

        except Exception as e:
            messagebox.showerror("Checkout failed", f"{e}")


if __name__ == "__main__":
    root = tk.Tk()
    customer_id = int(sys.argv[1])
    OrderWindow(root, customer_id)
    root.mainloop()
