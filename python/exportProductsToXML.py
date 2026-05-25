import sqlite3
import xml.etree.ElementTree as ET

db_path = r"c:\Users\kania\OneDrive\Desktop\Bunny&CavyBotanicals\database\assessment db"

try:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Product")
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()

    root_elem = ET.Element('Product')
    for row in rows:
        prod_elem = ET.SubElement(root_elem, 'Product')
        for col, val in zip(columns, row):
            ET.SubElement(prod_elem, col).text = str(val)

    tree = ET.ElementTree(root_elem)
    tree.write('products.xml', encoding='utf-8', xml_declaration=True)
    print(f"Exported data to products.xml by admin")

except Exception as e:
    print(f"Error exporting data: {e}")
