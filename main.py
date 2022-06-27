import sqlite3
import tkinter as tk
from datetime import *
from tkinter import ttk


def error(error_msg):
    # noinspection PyBroadException
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")
    try:
        with open('error.txt', 'w') as e:
            e.write("{} {}".format(date, error_msg))
    except Exception as ErrorError:
        print("Error file failed to write {}".format(ErrorError))


# ==== Main Window ========================================================================
root = tk.Tk()
root.title('Candle Companion')
root.geometry('800x400')
rWin = tk.Frame(root)
rWin.pack(fill='both', expand=True)
mWin = tk.Frame(root)
pWin = tk.Frame(root)

# ==== Frames =============================================================================
# ==== Main Init ====
rFrame = tk.Frame(rWin)
r_top_frame = tk.Frame(rFrame)
r_top_top_frame = tk.Frame(r_top_frame)
r_top_bottom_frame = tk.Frame(r_top_top_frame)
r_middle_frame = tk.Frame(rFrame)
r_middle_top_frame = tk.Frame(r_middle_frame)
r_middle_bottom_frame = tk.Frame(r_middle_frame)
r_bottom_frame = tk.Frame(rFrame)
r_bottom_top_frame = tk.Frame(r_bottom_frame)
r_bottom_bottom_frame = tk.Frame(r_bottom_frame)
r_left_frame = tk.Frame(r_top_bottom_frame)
r_right_frame = tk.Frame(r_top_bottom_frame)
# ==== Main Pack ====
rFrame.pack()
r_top_frame.pack(side=tk.TOP)
r_top_top_frame.pack(side=tk.TOP)
r_top_bottom_frame.pack(side=tk.BOTTOM)
r_middle_frame.pack(side=tk.TOP)
r_middle_top_frame.pack(side=tk.TOP)
r_middle_bottom_frame.pack(side=tk.BOTTOM)
r_bottom_frame.pack(side=tk.BOTTOM)
r_bottom_top_frame.pack(side=tk.TOP)
r_bottom_bottom_frame.pack(side=tk.BOTTOM)
r_left_frame.pack(side=tk.LEFT)
r_right_frame.pack(side=tk.RIGHT)

# ==== Materials Init ====
mFrame = tk.Frame(mWin)
m_top_frame = tk.Frame(mFrame)
m_top_top_frame = tk.Frame(m_top_frame)
m_top_bottom_frame = tk.Frame(m_top_top_frame)
m_middle_frame = tk.Frame(mFrame)
m_middle_top_frame = tk.Frame(m_middle_frame)
m_middle_bottom_frame = tk.Frame(m_middle_frame)
m_bottom_frame = tk.Frame(mFrame)
m_bottom_top_frame = tk.Frame(m_bottom_frame)
m_bottom_bottom_frame = tk.Frame(m_bottom_frame)
m_left_frame = tk.Frame(m_top_bottom_frame)
m_right_frame = tk.Frame(m_top_bottom_frame)
# ==== Materials Pack ====
mFrame.pack()
m_top_frame.pack(side=tk.TOP)
m_top_top_frame.pack(side=tk.TOP)
m_top_bottom_frame.pack(side=tk.BOTTOM)
m_middle_frame.pack(side=tk.TOP)
m_middle_top_frame.pack(side=tk.TOP)
m_middle_bottom_frame.pack(side=tk.BOTTOM)
m_bottom_frame.pack(side=tk.TOP)
m_bottom_top_frame.pack(side=tk.TOP)
m_bottom_bottom_frame.pack(side=tk.BOTTOM)
m_left_frame.pack(side=tk.LEFT)
m_right_frame.pack(side=tk.RIGHT)

# ==== Products Init ====
pFrame = tk.Frame(pWin)
p_top_frame = tk.Frame(pFrame)
p_top_top_frame = tk.Frame(p_top_frame)
p_top_bottom_frame = tk.Frame(p_top_top_frame)
p_middle_frame = tk.Frame(pFrame)
p_middle_top_frame = tk.Frame(p_middle_frame)
p_middle_bottom_frame = tk.Frame(p_middle_frame)
p_bottom_frame = tk.Frame(pFrame)
p_bottom_top_frame = tk.Frame(p_bottom_frame)
p_bottom_bottom_frame = tk.Frame(p_bottom_frame)
p_left_frame = tk.Frame(p_top_bottom_frame)
p_right_frame = tk.Frame(p_top_bottom_frame)
# ==== Products Pack ====
pFrame.pack()
p_top_frame.pack(side=tk.TOP)
p_top_top_frame.pack(side=tk.TOP)
p_top_bottom_frame.pack(side=tk.BOTTOM)
p_middle_frame.pack(side=tk.TOP)
p_middle_top_frame.pack(side=tk.TOP)
p_middle_bottom_frame.pack(side=tk.BOTTOM)
p_bottom_frame.pack(side=tk.TOP)
p_bottom_top_frame.pack(side=tk.TOP)
p_bottom_bottom_frame.pack(side=tk.BOTTOM)
p_left_frame.pack(side=tk.LEFT)
p_right_frame.pack(side=tk.RIGHT)

# ==== Database Connection ==============================================================
try:
    db = sqlite3.connect("db.sqlite")
    db.execute(
        "CREATE TABLE IF NOT EXISTS materials (ingredient TEXT NOT NULL, quantity INTEGER NOT NULL, cost REAL NOT NULL)")
    db.execute("CREATE TABLE IF NOT EXISTS products (product TEXT NOT NULL, scent TEXT NOT NULL, decoration TEXT, "
               "quantity INTEGER NOT NULL, price REAL NOT NULL)")
except Exception as DatabaseError:
    print("Database failed to initialise {}".format(DatabaseError))
    exit()


# ==== Functions ========================================================================
def change_to_materials(lWin):
    lWin.pack_forget()
    mWin.pack(fill='both', expand=True)



def change_to_products(lFrame):
    lFrame.pack_forget()
    pWin.pack(fill='both', expand=True)


def change_to_main(lFrame):
    lFrame.pack_forget()
    rWin.pack(fill='both', expand=True)


def refresh_materials():
    for item in materials_tree.get_children():
        materials_tree.delete(item)
    for material in db.execute("SELECT * FROM materials ORDER BY materials.ingredient"):
        materials_tree.insert('', tk.END, values=material)


def refresh_products():
    for item in product_tree.get_children():
        product_tree.delete(item)
    for prod in db.execute("SELECT * FROM products ORDER BY products.product"):
        product_tree.insert('', tk.END, values=prod)


def add_material():
    c = db.cursor()
    try:
        if str(m_ingredient_entry.get()).isalpha() and len(m_ingredient_entry.get()) > 0:
            if int(m_quantity_entry.get()) and len(m_quantity_entry.get()) > 0:
                if float(m_cost_entry.get()) and len(m_cost_entry.get()) > 0:
                    exists = c.execute(
                        "SELECT ingredient FROM materials WHERE (ingredient=? and cost=?)",
                        (m_ingredient_entry.get(), m_cost_entry.get())).fetchall()
                    if not exists:
                        db.execute("INSERT INTO materials VALUES(?, ?, ?)",
                                   (str(m_ingredient_entry.get()),
                                    float(m_quantity_entry.get()),
                                    float(m_cost_entry.get())))
                        db.commit()
                        c.close()
                        refresh_materials()
                        m_message_label.config(
                            text="{} {} {} added".format(m_ingredient_entry.get(),
                                                         m_quantity_entry.get(),
                                                         m_cost_entry.get()))
                    else:
                        fetch = c.execute(
                            "SELECT quantity FROM materials WHERE (ingredient=? and cost=?)",
                            (m_ingredient_entry.get(),
                             m_cost_entry.get())).fetchone()
                        orig_qty = fetch[0]
                        add_qty = float(m_quantity_entry.get())
                        new_qty = orig_qty + add_qty
                        print(new_qty)
                        print(fetch)
                        update = "UPDATE materials SET quantity=? WHERE ingredient=? and cost=?"

                        c.execute(update, (
                            new_qty, m_ingredient_entry.get(), m_cost_entry.get()))
                        c.close()
                        refresh_materials()

                        m_message_label.config(text="Field updated")
                else:
                    m_message_label.config(text="Cost must be a decimal number and cannot be empty")

            else:
                m_message_label.config(text="Scent name must be a word and cannot be empty")
        else:
            m_message_label.config(text="ingredient name must be a word and cannot be empty")
    except Exception as AddError:
        m_message_label.config(text="Data entry failed {}".format(AddError))
        db.rollback()
        refresh_materials()
    finally:
        pass


def add_product():
    c = db.cursor()
    try:
        if str(p_product_entry.get()).isalpha() and len(p_product_entry.get()) > 0:
            if str(p_scent_entry.get()).isalpha() and len(p_scent_entry.get()) > 0:
                if int(p_quantity_entry.get()) and len(p_quantity_entry.get()) > 0:
                    if float(p_price_entry.get()) and len(p_price_entry.get()) > 0:

                        exists = c.execute(
                            "SELECT product FROM products WHERE (product=? and scent=? and decoration=? and price=?)",
                            (p_product_entry.get(), p_scent_entry.get(), p_decorator_entry.get(),
                             p_price_entry.get())).fetchall()
                        if not exists:
                            db.execute("INSERT INTO products VALUES(?, ?, ?, ?, ?)",
                                       (str(p_product_entry.get()), str(p_scent_entry.get()),
                                        str(p_decorator_entry.get()), float(p_quantity_entry.get()),
                                        float(p_price_entry.get())))
                            db.commit()
                            c.close()
                            refresh_products()
                            p_message_label.config(
                                text="{} {} {} {} {} added".format(p_product_entry.get(), p_scent_entry.get(),
                                                                   p_decorator_entry.get(), p_quantity_entry.get(),
                                                                   p_price_entry.get()))
                        else:
                            fetch = c.execute(
                                "SELECT quantity FROM products WHERE (product=? and scent=? and decoration=? and price=?)",
                                (p_product_entry.get(), p_scent_entry.get(), p_decorator_entry.get(),
                                 p_price_entry.get())).fetchone()
                            orig_qty = fetch[0]
                            add_qty = float(p_quantity_entry.get())
                            new_qty = orig_qty + add_qty
                            print(new_qty)
                            print(fetch)
                            update = "UPDATE products SET quantity=? WHERE product=? and scent=? and decoration=? and price=?"

                            c.execute(update, (
                                new_qty, p_product_entry.get(), p_scent_entry.get(), p_decorator_entry.get(),
                                p_price_entry.get()))
                            c.close()
                            refresh_products()

                            p_message_label.config(text="Field updated")
                    else:
                        p_message_label.config(text="Price must be a decimal number and cannot be empty")
                else:
                    p_message_label.config(text="Price must be a decimal number and cannot be empty")
            else:
                p_message_label.config(text="Scent name must be a word and cannot be empty")
        else:
            p_message_label.config(text="Product name must be a word and cannot be empty")
    except Exception as AddProductError:
        error(AddProductError)
        p_message_label.config(text="Data entry failed {}".format(AddProductError))
        db.rollback()
        refresh_products()
    finally:
        pass


def get_materials_selection(event):
    try:
        curItem = materials_tree.focus()
        contents = (materials_tree.item(curItem))
        selecteddetails = contents['values']
        m_ingredient_entry.delete(0, tk.END)
        m_quantity_entry.delete(0, tk.END)
        m_cost_entry.delete(0, tk.END)
        m_ingredient_entry.insert(0, selecteddetails[0])
        m_quantity_entry.insert(0, selecteddetails[1])
        m_cost_entry.insert(0, selecteddetails[2])
    except Exception as GetSelectionError:
        print("Failed to get_selection {}".format(GetSelectionError))
    return


def get_products_selection(event):
    curItem = product_tree.focus()
    contents = (product_tree.item(curItem))
    selecteddetails = contents['values']
    p_product_entry.delete(0, tk.END)
    p_scent_entry.delete(0, tk.END)
    p_decorator_entry.delete(0, tk.END)
    p_quantity_entry.delete(0, tk.END)
    p_price_entry.delete(0, tk.END)
    p_product_entry.insert(0, selecteddetails[0])
    p_scent_entry.insert(0, selecteddetails[1])
    p_decorator_entry.insert(0, selecteddetails[2])
    p_quantity_entry.insert(0, selecteddetails[3])
    p_price_entry.insert(0, selecteddetails[4])
    return


def delete_ingredient():
    try:
        c = db.cursor()
        query = "DELETE FROM materials WHERE ingredient=? and quantity=? and cost=?"
        selection = (m_ingredient_entry.get(), m_quantity_entry.get(), m_cost_entry.get())
        c.execute(query, selection)
        m_message_label.config(text="Entry deleted")
        db.commit()
        refresh_materials()
    except Exception as DeleteError:
        m_message_label.config(text="Failed to remove field {}".format(DeleteError))
        db.rollback()
        refresh_materials()


def delete_product():
    try:
        c = db.cursor()
        query = "DELETE FROM products WHERE product=? and scent=? and decoration=? and quantity=? and price=?"
        selection = (
            p_product_entry.get(), p_scent_entry.get(), p_decorator_entry.get(), p_quantity_entry.get(),
            p_price_entry.get())
        c.execute(query, selection)
        p_message_label.config(text="Entry deleted")
        db.commit()
        refresh_products()
    except Exception as DeleteProductError:
        error(DeleteProductError)
        p_message_label.config(text="Failed to remove field {}".format(DeleteProductError))
        db.rollback()
        refresh_products()


# ==== TreeView ==========================================================================
# ==== Materials ====
try:
    mat_columns = ('ingredient', 'quantity', 'cost')
    materials_tree = ttk.Treeview(m_bottom_top_frame, columns=mat_columns, show='headings')
    materials_tree.pack(side=tk.LEFT)

    materials_tree.heading('ingredient', text='materials')
    materials_tree.column('ingredient', minwidth=5, width=100)
    materials_tree.heading('quantity', text='Quantity')
    materials_tree.column('quantity', minwidth=5, width=100)
    materials_tree.heading('cost', text='cost')
    materials_tree.column('cost', minwidth=5, width=100)

    for ingredient in db.execute("SELECT * FROM materials ORDER BY materials.ingredient"):
        materials_tree.insert('', tk.END, values=ingredient)
    materials_tree.bind('<<TreeviewSelect>>', get_materials_selection, )


    scrollbar = ttk.Scrollbar(m_bottom_top_frame, orient=tk.VERTICAL, command=materials_tree.yview)
    materials_tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill='y')
except Exception as MaterialsTreeViewError:
    error(MaterialsTreeViewError)
    print("Materials TreeView failed to initialise {}".format(MaterialsTreeViewError))
# ==== Products ====
try:
    prod_columns = ('product', 'scent', 'decoration', 'quantity', 'price')
    product_tree = ttk.Treeview(p_bottom_top_frame, columns=prod_columns, show='headings')
    product_tree.pack(side=tk.LEFT)

    product_tree.heading('product', text='Products')
    product_tree.column('product', minwidth=5, width=100)
    product_tree.heading('scent', text='Scent')
    product_tree.column('scent', minwidth=5, width=100)
    product_tree.heading('decoration', text='Decoration')
    product_tree.column('decoration', minwidth=5, width=100)
    product_tree.heading('quantity', text='Quantity')
    product_tree.column('quantity', minwidth=5, width=100)
    product_tree.heading('price', text='Price')
    product_tree.column('price', minwidth=5, width=100)

    # noinspection PyUnboundLocalVariable
    for product in db.execute("SELECT * FROM products ORDER BY products.product"):
        product_tree.insert('', tk.END, values=product)
    product_tree.bind('<<TreeviewSelect>>', get_products_selection, )

    scrollbar = ttk.Scrollbar(p_bottom_top_frame, orient=tk.VERTICAL, command=product_tree.yview)
    product_tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill='y')
except Exception as ProductsTreeViewError:
    error(ProductsTreeViewError)
    print("Product TreeView failed to initialise {}".format(ProductsTreeViewError))

# ==== Main Screen =======================================================================
# ==== Labels ====
#main

# ==== Buttons ===========================================================================
main_button = tk.Button(r_top_top_frame, text="Main", command=lambda: change_to_main(rWin))
materials_button = tk.Button(r_top_top_frame, text="Materials", command=lambda: change_to_materials(rWin))
products_button = tk.Button(r_top_top_frame, text="Products", command=lambda: change_to_products(rWin))

main_button.pack(side=tk.LEFT)
materials_button.pack(side=tk.LEFT)
products_button.pack(side=tk.LEFT)

# ==== Materials Screen ==================================================================
# ==== Labels ============================================================================
m_materials_label = tk.Label(m_right_frame, text="materials")
m_quantity_label = tk.Label(m_right_frame, text="Quantity")
m_cost_label = tk.Label(m_right_frame, text="cost")
m_message_label = tk.Label(m_bottom_bottom_frame, text='Candle Companion')

m_materials_label.pack(side=tk.TOP)
m_quantity_label.pack(side=tk.TOP)
m_cost_label.pack(side=tk.TOP)
m_message_label.pack(side=tk.BOTTOM)

# ==== Entry Boxes =======================================================================
m_ingredient_entry = tk.Entry(m_left_frame)
m_quantity_entry = tk.Entry(m_left_frame)
m_cost_entry = tk.Entry(m_left_frame)

m_ingredient_entry.pack(side=tk.TOP)
m_quantity_entry.pack(side=tk.TOP)
m_cost_entry.pack(side=tk.TOP)

# ==== Buttons ===========================================================================
main_button = tk.Button(m_top_top_frame, text="Main", command=lambda: change_to_main(mWin))
materials_button = tk.Button(m_top_top_frame, text="Materials", command=lambda: change_to_materials(mWin))
products_button = tk.Button(m_top_top_frame, text="Products", command=lambda: change_to_products(mWin))
m_enter_button = tk.Button(m_middle_top_frame, text="Enter", command=add_material)
m_delete_button = tk.Button(m_middle_top_frame, text="Delete", command=delete_ingredient)

main_button.pack(side=tk.LEFT)
materials_button.pack(side=tk.LEFT)
products_button.pack(side=tk.LEFT)
m_enter_button.pack(side=tk.LEFT)
m_delete_button.pack(side=tk.LEFT)

# ==== Products Screen ===================================================================
# ==== Labels ============================================================================
p_products_label = tk.Label(p_right_frame, text="Products")
p_scents_label = tk.Label(p_right_frame, text="Scent")
p_decoration_label = tk.Label(p_right_frame, text="Decoration")
p_quantity_label = tk.Label(p_right_frame, text="Quantity")
p_price_label = tk.Label(p_right_frame, text="Price")
p_message_label = tk.Label(p_bottom_bottom_frame, text='Candle Companion')

p_message_label.pack(side=tk.BOTTOM)
p_products_label.pack(side=tk.TOP)
p_scents_label.pack(side=tk.TOP)
p_decoration_label.pack(side=tk.TOP)
p_quantity_label.pack(side=tk.TOP)
p_price_label.pack(side=tk.TOP)

# ==== Entry Boxes =======================================================================
p_product_entry = tk.Entry(p_left_frame)
p_scent_entry = tk.Entry(p_left_frame)
p_decorator_entry = tk.Entry(p_left_frame)
p_quantity_entry = tk.Entry(p_left_frame)
p_price_entry = tk.Entry(p_left_frame)

p_product_entry.pack(side=tk.TOP)
p_scent_entry.pack(side=tk.TOP)
p_decorator_entry.pack(side=tk.TOP)
p_quantity_entry.pack(side=tk.TOP)
p_price_entry.pack(side=tk.TOP)

# ==== Buttons ===========================================================================
main_button = tk.Button(p_top_top_frame, text="Main", command=lambda: change_to_main(pWin))
materials_button = tk.Button(p_top_top_frame, text="Materials", command=lambda: change_to_materials(pWin))
products_button = tk.Button(p_top_top_frame, text="Products", command=lambda: change_to_materials(pWin))
p_enter_button = tk.Button(p_middle_top_frame, text="Enter", command=add_product)
p_delete_button = tk.Button(p_middle_top_frame, text="Delete", command=delete_product)

main_button.pack(side=tk.LEFT)
materials_button.pack(side=tk.LEFT)
products_button.pack(side=tk.LEFT)
p_enter_button.pack(side=tk.LEFT)
p_delete_button.pack(side=tk.LEFT)
# ==== Main Loop ========================================================================
root.mainloop()
print("Closing database connection")
db.close()
