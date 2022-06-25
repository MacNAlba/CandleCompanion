import sqlite3
from sqlite3 import Connection
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
# TODO create an error function to handle all error messages and output them to a separate error log file
# ==== Database Connection ====
try:
    db: Connection = sqlite3.connect("db.sqlite")
    db.execute("CREATE TABLE IF NOT EXISTS materials (ingredient TEXT NOT NULL, quantity REAL NOT NULL, cost REAL)")
    db.execute("CREATE TABLE IF NOT EXISTS products (product TEXT NOT NULL, scent TEXT NOT NULL, decoration TEXT, "
               "quantity INTEGER NOT NULL, price REAL NOT NULL)")
except Exception as e:
    print("Database failed to initialise {}".format(e))
    exit()

# ==== Functions ====
def refresh():
    for item in tree.get_children():
        tree.delete(item)
    for product in db.execute("SELECT * FROM products ORDER BY products.product"):
        tree.insert('', tk.END, values=product)


def add_product():
    c = db.cursor()
    try:
        if str(product_entry.get()).isalpha() and len(product_entry.get()) > 0:
            if str(scent_entry.get()).isalpha() and len(scent_entry.get()) > 0:
                if int(quantity_entry.get()) and len(quantity_entry.get()) > 0:
                    if float(price_entry.get()) and len(quantity_entry.get()) > 0:

                        exists = c.execute(
                            "SELECT product FROM products WHERE (product=? and scent=? and decoration=? and price=?)",
                            (product_entry.get(), scent_entry.get(), decorator_entry.get(),
                             price_entry.get())).fetchall()
                        if not exists:
                            db.execute("INSERT INTO products VALUES(?, ?, ?, ?, ?)",
                                       (str(product_entry.get()), str(scent_entry.get()),
                                        str(decorator_entry.get()), float(quantity_entry.get()),
                                        float(price_entry.get())))
                            db.commit()
                            c.close()
                            refresh()
                            message_label.config(
                                text="{} {} {} {} {} added".format(product_entry.get(), scent_entry.get(),
                                                                   decorator_entry.get(), quantity_entry.get(),
                                                                   price_entry.get()))
                        else:
                            fetch = c.execute(
                                "SELECT quantity FROM products WHERE (product=? and scent=? and decoration=? and price=?)",
                                (product_entry.get(), scent_entry.get(), decorator_entry.get(),
                                 price_entry.get())).fetchone()
                            orig_qty = fetch[0]
                            add_qty = float(quantity_entry.get())
                            new_qty = orig_qty + add_qty
                            print(new_qty)
                            print(fetch)
                            update = "UPDATE products SET quantity=? WHERE product=? and scent=? and decoration=? and price=?"

                            c.execute(update, (
                            new_qty, product_entry.get(), scent_entry.get(), decorator_entry.get(), price_entry.get()))
                            c.close()
                            refresh()

                            message_label.config(text="Field updated")
                    else:
                        message_label.config(text="Price must be a decimal number and cannot be empty")
                else:
                    message_label.config(text="Price must be a decimal number and cannot be empty")
            else:
                message_label.config(text="Scent name must be a word and cannot be empty")
        else:
            message_label.config(text="Product name must be a word and cannot be empty")
    except Exception as e:
        message_label.config(text="Data entry failed {}".format(e))
        db.rollback()
        refresh()
    finally:
        pass


def get_selection(event):
    curItem = tree.focus()
    contents = (tree.item(curItem))
    selecteddetails = contents['values']
    product_entry.delete(0, tk.END)
    scent_entry.delete(0, tk.END)
    decorator_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    product_entry.insert(0, selecteddetails[0])
    scent_entry.insert(0, selecteddetails[1])
    decorator_entry.insert(0, selecteddetails[2])
    quantity_entry.insert(0, selecteddetails[3])
    price_entry.insert(0, selecteddetails[4])
    return


def delete_product():
    try:
        c = db.cursor()
        query = "DELETE FROM products WHERE product=? and scent=? and decoration=? and quantity=? and price=?"
        selection = (product_entry.get(), scent_entry.get(), decorator_entry.get(), quantity_entry.get(), price_entry.get())
        c.execute(query, selection)
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
try:
    prod_columns = ('product', 'scent', 'decoration', 'quantity', 'price')
    tree = ttk.Treeview(mWin, columns=prod_columns, show='headings')

    tree.heading('product', text='Products')
    tree.heading('scent', text='Scent')
    tree.heading('decoration', text='Decoration')
    tree.heading('quantity', text='Quantity')
    tree.heading('price', text='Price')

    for product in db.execute("SELECT * FROM products ORDER BY products.product"):
        tree.insert('', tk.END, values=product)
    tree.bind('<<TreeviewSelect>>', get_selection,)
    tree.grid(row=5, column=0, sticky='nsew', rowspan=2, columnspan=4, padx=(30, 0))

    scrollbar = ttk.Scrollbar(mWin, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=5, column=3, sticky='nse')
except Exception as e:
    print("TreeView failed to initialise {}".format(e))

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
