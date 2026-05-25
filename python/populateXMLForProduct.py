import sqlite3
import xml.etree.ElementTree as ET
from tkinter import simpledialog, Tk

db_path = r"c:\Users\kania\OneDrive\Desktop\Bunny&CavyBotanicals\database\assessment db"

def populate_xml_for_product():
    root = Tk()
    root.withdraw()
    
    prod_id = simpledialog.askinteger("Input", "Enter ProductID to populate XML:")
    
    if prod_id:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT prod_name, usage_guidelines, product_weight_grams FROM Product WHERE ProdID = ?", (prod_id,))
            row = cursor.fetchone()
            
            if row:
                prod_name, usage, weight = row
                root_elem = ET.Element("ProductDetails")
                ET.SubElement(root_elem, "ProductName").text = prod_name if prod_name else "Unknown"
                ET.SubElement(root_elem, "UsageGuidelines").text = usage if usage else "No guidelines"
                ET.SubElement(root_elem, "WeightGrams").text = str(weight) if weight else "N/A"
                
                xml_str = ET.tostring(root_elem, encoding='unicode')
                cursor.execute("UPDATE Product SET xml_details = ? WHERE ProdID = ?", (xml_str, prod_id))
                conn.commit()
                print(f"Updated xml_details for ProductID {prod_id}")
            else:
                print("Product not found.")
    else:
        print("No ProductID provided.")

populate_xml_for_product()
