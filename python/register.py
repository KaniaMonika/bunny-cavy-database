import tkinter as tk
from tkinter import messagebox
import sqlite3
import re
import bcrypt
from utils import apply_theme


conn = sqlite3.connect("../database/assessment.db")
cursor = conn.cursor()

class RegistrationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Register")
        self.city_id = None
        self.postcode_id = None
        self.pet_id = None
        self.start_city_input()

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def start_city_input(self):
        self.clear_window()
        tk.Label(self.master, text="Enter City Name", font=("Helvetica", 14)).pack(pady=10)
        self.city_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.city_entry.pack(pady=10)
        tk.Button(self.master, text="Next", command=self.handle_city, font=("Helvetica", 10)).pack()
        apply_theme(self.master, bg="#e6f2ff", fg="#003366")
        root.geometry("400x150")


    def handle_city(self):
        city_name = self.city_entry.get().strip()
        if not city_name:
            messagebox.showerror("Error", "City name is required")
            return

        country_id = 1  #UK

        #insert city if not exists
        cursor.execute("SELECT CityID FROM City WHERE City_name = ?", (city_name,))
        result = cursor.fetchone()
        if result:
            self.city_id = result[0]
        else:
            cursor.execute("INSERT INTO City (City_name, CountryID) VALUES (?, ?)", (city_name, country_id))
            conn.commit()
            self.city_id = cursor.lastrowid

        self.start_postcode_input()

    def start_postcode_input(self):
        self.clear_window()
        tk.Label(self.master, text="Enter Postcode", font=("Helvetica", 14)).pack(pady=10)
        self.postcode_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.postcode_entry.pack(pady=10)
        tk.Button(self.master, text="Next", command=self.handle_postcode, font=("Helvetica", 10)).pack()
        apply_theme(self.master, bg="#e6f2ff", fg="#003366")
        root.geometry("400x150")


    def handle_postcode(self):
        postcode = self.postcode_entry.get().strip()
        if not postcode:
            messagebox.showerror("Error", "Postcode is required")
            return

        #insert postcode if not exists
        cursor.execute("SELECT PostcodeID FROM Postcode WHERE Postcode = ? AND CityID = ?", (postcode, self.city_id))
        result = cursor.fetchone()
        if result:
            self.postcode_id = result[0]
        else:
            cursor.execute("INSERT INTO Postcode (Postcode, CityID) VALUES (?, ?)", (postcode, self.city_id))
            conn.commit()
            self.postcode_id = cursor.lastrowid

        self.start_pet_selection()

    def start_pet_selection(self):
        self.clear_window()
        tk.Label(self.master, text="Select Pet Type", font=("Helvetica", 14)).pack(pady=10)

        self.pet_var = tk.StringVar()
        tk.Radiobutton(self.master, text="Guinea Pig", variable=self.pet_var, value="1", font=("Helvetica", 12)).pack(pady=5)
        tk.Radiobutton(self.master, text="Bunny", variable=self.pet_var, value="2", font=("Helvetica", 12)).pack(pady=10)

        tk.Button(self.master, text="Next", command=self.handle_pet_selection, font=("Helvetica", 10)).pack()
        apply_theme(self.master, bg="#e6f2ff", fg="#003366")
        root.geometry("400x200")


    def handle_pet_selection(self):
        if not self.pet_var.get():
            messagebox.showerror("Error", "Please select a pet type")
            return

        self.pet_id = int(self.pet_var.get())
        self.start_final_details()

    def start_final_details(self):
        self.clear_window()
        self.fields = {}
        entries = [
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("Email", "email"),
            ("Phone", "phone"),
            ("Address Line", "address"),
            ("Password", "password", "*"),
            ("Confirm Password", "confirm_password", "*")
        ]

        for label, name, *args in entries:
            tk.Label(self.master, text=label, font=("Helvetica", 12)).pack(pady=5)
            entry = tk.Entry(self.master, show=args[0], font=("Helvetica", 12)) if args else tk.Entry(self.master, font=("Helvetica", 12))
            entry.pack(pady=5)
            self.fields[name] = entry

        tk.Button(self.master, text="Register", command=self.register_user, font=("Helvetica", 10)).pack()
        apply_theme(self.master, bg="#e6f2ff", fg="#003366")
        root.geometry("400x500")


    def register_user(self):
        data = {k: v.get().strip() for k, v in self.fields.items()}

        if any(not v for v in data.values()):
            messagebox.showerror("Error", "All fields are required.")
            return

        if data['password'] != data['confirm_password']:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        login = data['email'].split('@')[0]

        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, data['email']):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        try:
            cursor.execute("""
                INSERT INTO Customers (
                    first_name, last_name, email, phone, address_first_line, postcode, petID, subscriber
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['first_name'], data['last_name'], data['email'], data['phone'],
                data['address'], self.postcode_id, self.pet_id, "no"
            ))
            conn.commit()
            customer_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO login_credentials (customer_id, login, password)
                VALUES (?, ?, ?)
            """, (customer_id, login, hashed_password))
            conn.commit()

            messagebox.showinfo("Success", "Account created successfully!")
            self.master.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.geometry("400x300")
app = RegistrationApp(root)
root.mainloop()
conn.close()
