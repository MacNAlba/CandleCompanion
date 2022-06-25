import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

# ==== Database Connection ====
db = sqlite3.connect("db.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
db.execute("CREATE TABLE IF NOT EXISTS materials (ingredient TEXT NOT NULL, quantity REAL NOT NULL, cost REAL)")
db.execute("CREATE TABLE IF NOT EXISTS products (product TEXT NOT NULL, scent TEXT NOT NULL, decoration TEXT, "
           "quantity REAL NOT NULL, price REAL NOT NULL)")


# ==== Functions ====
def item_selected():
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        record = item['values']
        return record


def refresh():
    for item in tree.get_children():
        tree.delete(item)
    for product in db.execute("SELECT * FROM products ORDER BY products.product"):
        tree.insert('', tk.END, values=product)


def add_product():
    try:
        db.execute("INSERT INTO products VALUES(?, ?, ?, ?, ?)", (product_entry.get(), scent_entry.get(),
                                                                  decorator_entry.get(), quantity_entry.get(),
                                                                  price_entry.get()))
        db.commit()
        refresh()
    except Exception as e:
        message_label.config(text="Data entry failed {}".format(e))
        db.rollback()
        refresh()
    finally:
        pass


def delete_product():
    try:

        db.execute("DELETE FROM products WHERE products.product=?", (item_selected,))
        message_label.config(text="Entry deleted")
        db.commit()
        refresh()
    except Exception as e:
        message_label.config(text="Failed to remove field {}".format(e))
        db.rollback()
        refresh()


# ==== Main Window ====
mWin = tk.Tk()
mWin.title('Candle Companion')
# mWin.geometry('1024x768')

mWin.columnconfigure(0, weight=2)
mWin.columnconfigure(1, weight=2)
mWin.columnconfigure(2, weight=2)
mWin.columnconfigure(3, weight=2)
mWin.columnconfigure(4, weight=2)
mWin.columnconfigure(5, weight=2)
mWin.columnconfigure(6, weight=2)
mWin.columnconfigure(7, weight=2)
mWin.columnconfigure(8, weight=1)

mWin.rowconfigure(0, weight=1)
mWin.rowconfigure(1, weight=5)
mWin.rowconfigure(2, weight=5)
mWin.rowconfigure(3, weight=5)
mWin.rowconfigure(4, weight=5)
mWin.rowconfigure(5, weight=5)
mWin.rowconfigure(6, weight=5)
mWin.rowconfigure(7, weight=1)

# ==== TreeView ====
prod_columns = ('product', 'scent', 'decoration', 'quantity', 'price')
tree = ttk.Treeview(mWin, columns=prod_columns, show='headings')

tree.heading('product', text='Products')
tree.heading('scent', text='Scent')
tree.heading('decoration', text='Decoration')
tree.heading('quantity', text='Quantity')
tree.heading('price', text='Price')

for product in db.execute("SELECT * FROM products ORDER BY products.product"):
    tree.insert('', tk.END, values=product)

# TODO data validation on entry fields
# TODO data validation on database entry
# TODO add data remove button and feature


tree.bind('<<TreeviewSelect>>', item_selected)

tree.grid(row=5, column=0, sticky='nsew', rowspan=2, columnspan=4, padx=(30, 0))

scrollbar = ttk.Scrollbar(mWin, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=5, column=3, sticky='nse')

# ==== Frames ====
frame = tk.Frame(mWin)
frame.grid(row=1, column=1, sticky='nsew')
left_frame = tk.Frame(frame)
right_frame = tk.Frame(frame)
left_frame.pack(side=LEFT)
right_frame.pack(side=RIGHT)

# ==== Labels ====
products_label = tk.Label(right_frame, text="Products")
scents_label = tk.Label(right_frame, text="Scent")
decoration_label = tk.Label(right_frame, text="Decoration")
quantity_label = tk.Label(right_frame, text="Quantity")
price_label = tk.Label(right_frame, text="Price")
message_label = tk.Label(mWin, text='Candle Companion')
message_label.grid(row=7, column=1)

products_label.pack(side=TOP)
scents_label.pack(side=TOP)
decoration_label.pack(side=TOP)
quantity_label.pack(side=TOP)
price_label.pack(side=TOP)

# ==== Buttons ====
enter_button = tk.Button(mWin, text="Enter", command=add_product)
enter_button.grid(row=3, column=1)
delete_button = tk.Button(mWin, text="Delete", command=delete_product)
delete_button.grid(row=3, column=2)

# ==== Entry Boxes ====
product_entry = tk.Entry(left_frame)
product_entry.pack(side=TOP)

scent_entry = tk.Entry(left_frame)
scent_entry.pack(side=TOP)

decorator_entry = tk.Entry(left_frame)
decorator_entry.pack(side=TOP)

quantity_entry = tk.Entry(left_frame)
quantity_entry.pack(side=TOP)

price_entry = tk.Entry(left_frame)
price_entry.pack(side=TOP)

# ==== Main Loop ====
mWin.mainloop()
print("Closing database connection")
db.close()
