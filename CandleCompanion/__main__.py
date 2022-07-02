import sqlite3
import tkinter as tk
from datetime import *
from tkinter import ttk
from PIL import ImageTk, Image
import Database as Database

db = sqlite3.connect("db.sqlite")
cur = db.cursor()
datab = Database.Database(db, cur)



# ==== Functions ========================================================================
def tree(frame, selection, table, column, *args):
    try:
        columns = (args)
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        tree.pack(side=tk.LEFT)
        for i in args:
            for j in range(0, len(i)):
                if '_' in i[j]:
                    i[j].replace('_', ' ')
                    tree.heading(i, text='{}'.format(i))
                    tree.column(i, minwidth=5, width=100)
                else:
                    tree.heading(i, text='{}'.format(i))
                    tree.column(i, minwidth=5, width=100)

        for value in datab.db.execute("SELECT * FROM {} ORDER BY {}".format(table, column)):
            tree.insert('', tk.END, values=value)
        tree.bind('<<TreeviewSelect>>', selection, )

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        return tree
    except Exception as TreeViewError:
        error(TreeViewError)
        print("TreeView failed to initialise {}".format(TreeViewError))


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
    p_size_entry.delete(0, tk.END)
    p_scent_entry.delete(0, tk.END)
    p_decorator_1_entry.delete(0, tk.END)
    p_decorator_2_entry.delete(0, tk.END)
    p_quantity_entry.delete(0, tk.END)
    p_price_entry.delete(0, tk.END)
    p_product_entry.insert(0, selecteddetails[0])
    p_size_entry.insert(0, selecteddetails[1])
    p_scent_entry.insert(0, selecteddetails[2])
    p_decorator_1_entry.insert(0, selecteddetails[3])
    p_decorator_2_entry.insert(0, selecteddetails[4])
    p_quantity_entry.insert(0, selecteddetails[5])
    p_price_entry.insert(0, selecteddetails[6])
    return


def get_recipes_selection(event):
    try:
        curItem = rec_tree.focus()
        contents = (rec_tree.item(curItem))
        selecteddetails = contents['values']
        r_product_entry.delete(0, tk.END)
        r_wax_entry.delete(0, tk.END)
        r_scent_amount_entry.delete(0, tk.END)
        r_product_entry.insert(0, selecteddetails[0])
        r_wax_entry.insert(0, selecteddetails[1])
        r_scent_amount_entry.insert(0, selecteddetails[2])
    except Exception as GetSelectionError:
        print("Failed to get_selection {}".format(GetSelectionError))
    return


def change_frame(lWin, nWin):
    lWin.pack_forget()
    nWin.pack(fill='both', expand=True)


def button(frame, text, command, side):
    but = tk.Button(frame, text=text, command=command)
    but.pack(side=side)
    return but


def label(frame, text, side):
    lab = tk.Label(frame, text=text)
    lab.pack(side=side)
    return lab


def entry(frame, side):
    ent = tk.Entry(frame)
    ent.pack(side=side)
    return ent


def dtime():
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")
    return date


def error(error_msg):
    try:
        with open('error.txt', 'w') as e:
            e.write("{} {}".format(dtime(), error_msg))
    except Exception as ErrorError:
        print("Error file failed to write {}".format(ErrorError))


def frame(frame, side):
    fram = tk.Frame(frame)
    fram.pack(side=side)
    return fram


# ==== Main Window ========================================================================
root = tk.Tk()
root.title('Candle Companion')
root.geometry('800x500')
rootWin = tk.Frame(root)
rootWin.pack(fill='both', expand=True)
mWin = tk.Frame(root)
pWin = tk.Frame(root)
sWin = tk.Frame(root)
rWin = tk.Frame(root)

# ==== Frames =============================================================================
# ==== Main ====
rootFrame = frame(rootWin, None)
root_top_frame = frame(rootFrame, tk.TOP)
root_top_top_frame = frame(root_top_frame, tk.TOP)
root_top_bottom_frame = frame(root_top_top_frame, tk.BOTTOM)

root_middle_frame = frame(rootFrame, tk.TOP)
root_middle_top_frame = frame(root_middle_frame, tk.TOP)
root_middle_bottom_frame = frame(root_middle_frame, tk.BOTTOM)

root_bottom_frame = frame(rootFrame, tk.BOTTOM)
root_bottom_top_frame = frame(root_bottom_frame, tk.TOP)
root_bottom_bottom_frame = frame(root_bottom_frame, tk.BOTTOM)

root_left_frame = frame(root_top_bottom_frame, tk.LEFT)
root_right_frame = frame(root_top_bottom_frame, tk.RIGHT)

# ==== Materials ====
mFrame = frame(mWin, None)
m_top_frame = frame(mFrame, tk.TOP)
m_top_top_frame = frame(m_top_frame, tk.TOP)
m_top_bottom_frame = frame(m_top_top_frame, tk.BOTTOM)

m_middle_frame = frame(mFrame, tk.TOP)
m_middle_top_frame = frame(m_middle_frame, tk.TOP)
m_middle_bottom_frame = frame(m_middle_frame, tk.BOTTOM)

m_bottom_frame = frame(mFrame, tk.TOP)
m_bottom_top_frame = frame(m_bottom_frame, tk.TOP)
m_bottom_bottom_frame = frame(m_bottom_frame, tk.BOTTOM)

m_left_frame = frame(m_top_bottom_frame, tk.LEFT)
m_right_frame = frame(m_top_bottom_frame, tk.RIGHT)

# ==== Products ====
pFrame = frame(pWin, None)
p_top_frame = frame(pFrame, tk.TOP)
p_top_top_frame = frame(p_top_frame, tk.TOP)
p_top_bottom_frame = frame(p_top_top_frame, tk.BOTTOM)

p_middle_frame = frame(pFrame, tk.TOP)
p_middle_top_frame = frame(p_middle_frame, tk.TOP)
p_middle_bottom_frame = frame(p_middle_frame, tk.BOTTOM)

p_bottom_frame = frame(pFrame, tk.TOP)
p_bottom_top_frame = frame(p_bottom_frame, tk.TOP)
p_bottom_bottom_frame = frame(p_bottom_frame, tk.BOTTOM)

p_left_frame = frame(p_top_bottom_frame, tk.LEFT)
p_right_frame = frame(p_top_bottom_frame, tk.RIGHT)

# ==== Sales ====
sFrame = frame(sWin, None)
s_top_frame = frame(sFrame, tk.TOP)
s_top_top_frame = frame(s_top_frame, tk.TOP)
s_top_bottom_frame = frame(s_top_top_frame, tk.BOTTOM)

s_middle_frame = frame(sFrame, tk.TOP)
s_middle_top_frame = frame(s_middle_frame, tk.TOP)
s_middle_bottom_frame = frame(s_middle_frame, tk.BOTTOM)

s_bottom_frame = frame(sFrame, tk.TOP)
s_bottom_top_frame = frame(s_bottom_frame, tk.TOP)
s_bottom_bottom_frame = frame(s_bottom_frame, tk.BOTTOM)

s_left_frame = frame(s_top_bottom_frame, tk.LEFT)
s_right_frame = frame(s_top_bottom_frame, tk.RIGHT)

# ==== Recipes ====
rFrame = frame(rWin, None)
r_top_frame = frame(rFrame, tk.TOP)
r_top_top_frame = frame(r_top_frame, tk.TOP)
r_top_bottom_frame = frame(r_top_top_frame, tk.BOTTOM)

r_middle_frame = frame(rFrame, tk.TOP)
r_middle_top_frame = frame(r_middle_frame, tk.TOP)
r_middle_bottom_frame = frame(r_middle_frame, tk.BOTTOM)

r_bottom_frame = frame(rFrame, tk.BOTTOM)
r_bottom_top_frame = frame(r_bottom_frame, tk.TOP)
r_bottom_bottom_frame = frame(r_bottom_frame, tk.BOTTOM)

r_left_frame = frame(r_top_bottom_frame, tk.LEFT)
r_right_frame = frame(r_top_bottom_frame, tk.RIGHT)

# ==== Create Treeviews ==================================================================
materials_tree = tree(m_bottom_top_frame, get_materials_selection, 'materials', 'materials.ingredient', 'ingredients',
                      'quantity', 'cost')
product_tree = tree(p_bottom_top_frame, get_products_selection, 'products', 'products.product', 'products', 'size',
                    'scent', 'decoration_1', 'decoration_2', 'quantity', 'price')
rec_tree = tree(r_bottom_top_frame, get_recipes_selection, 'recipes', 'recipes.product', 'product', 'wax_amount', 'scent_amount')

# ==== Main Screen =======================================================================
# ==== Labels ====
img = ImageTk.PhotoImage(Image.open('img/RoarinLogo300.png'))
canvas = tk.Canvas(rootWin, width=305, height=305)
canvas.pack()
canvas.create_image(5, 5, anchor='nw', image=img)

# ==== Buttons ===========================================================================
# materials_button = tk.Button(r_top_top_frame, text="Materials", command=lambda: change_frame(rWin, mWin))
root_materials_button = button(root_top_top_frame, "Materials", lambda: change_frame(rootWin, mWin), tk.LEFT)
root_products_button = button(root_top_top_frame, "Products", lambda: change_frame(rootWin, pWin), tk.LEFT)
root_sales_button = button(root_top_top_frame, "Sales", lambda: change_frame(rootWin, sWin), tk.LEFT)
root_recipes_button = button(root_top_top_frame, "Recipes", lambda: change_frame(rootWin, rWin), tk.LEFT)

# ==== Materials Screen ==================================================================
# ==== Labels ============================================================================
m_materials_label = label(m_right_frame, "Ingredient", tk.TOP)
m_quantity_label = label(m_right_frame, "Quantity", tk.TOP)
m_cost_label = label(m_right_frame, "cost", tk.TOP)
m_message_label = label(m_bottom_bottom_frame, 'Candle Companion', tk.BOTTOM)

# ==== Entry Boxes =======================================================================
m_ingredient_entry = entry(m_left_frame, tk.TOP)
m_quantity_entry = entry(m_left_frame, tk.TOP)
m_cost_entry = entry(m_left_frame, tk.TOP)

# ==== Buttons ===========================================================================
m_main_button = button(m_top_top_frame, "Main", lambda: change_frame(mWin, rootWin), tk.LEFT)
m_products_button = button(m_top_top_frame, "Products", lambda: change_frame(mWin, pWin), tk.LEFT)
m_sales_button = button(m_top_top_frame, "Sales", lambda: change_frame(mWin, sWin), tk.LEFT)
m_recipes_button = button(m_top_top_frame, "Recipes", lambda: change_frame(mWin, rWin), tk.LEFT)

m_enter_button = button(m_middle_top_frame, "Enter", datab.add_material, tk.LEFT)
m_delete_button = button(m_middle_top_frame, "Delete", datab.delete_ingredient, tk.LEFT)

# ==== Products Screen ===================================================================
# ==== Labels ============================================================================
p_products_label = label(p_right_frame, "Products", tk.TOP)
p_size_label = label(p_right_frame, "Size", tk.TOP)
p_scents_label = label(p_right_frame, "Scent", tk.TOP)
p_decoration_1_label = label(p_right_frame, "Decoration 1", tk.TOP)
p_decoration_2_label = label(p_right_frame, "Decoration 2", tk.TOP)
p_quantity_label = label(p_right_frame, "Quantity", tk.TOP)

p_price_label = label(p_right_frame, "Price", tk.TOP)
p_message_label = label(p_bottom_bottom_frame, 'Candle Companion', tk.BOTTOM)

# ==== Entry Boxes =======================================================================
p_product_entry = entry(p_left_frame, tk.TOP)
p_size_entry = entry(p_left_frame, tk.TOP)
p_scent_entry = entry(p_left_frame, tk.TOP)
p_decorator_1_entry = entry(p_left_frame, tk.TOP)
p_decorator_2_entry = entry(p_left_frame, tk.TOP)
p_quantity_entry = entry(p_left_frame, tk.TOP)
p_price_entry = entry(p_left_frame, tk.TOP)

# ==== Buttons ===========================================================================
p_main_button = button(p_top_top_frame, "Main", lambda: change_frame(pWin, rootWin), tk.LEFT)
p_materials_button = button(p_top_top_frame, "Materials", lambda: change_frame(pWin, mWin), tk.LEFT)
p_sales_button = button(p_top_top_frame, "Sales", lambda: change_frame(pWin, sWin), tk.LEFT)
p_recipes_button = button(p_top_top_frame, "Recipes", lambda: change_frame(pWin, rWin), tk.LEFT)
p_enter_button = button(p_middle_top_frame, "Enter", datab.add_product, tk.LEFT)
p_delete_button = button(p_middle_top_frame, "Delete", datab.delete_product, tk.LEFT)

# ==== Sales Screen
# ==== Buttons ====
s_main_button = button(s_top_top_frame, "Main", lambda: change_frame(sWin, rootWin), tk.LEFT)
s_materials_button = button(s_top_top_frame, "Materials", lambda: change_frame(sWin, mWin), tk.LEFT)
s_products_button = button(s_top_top_frame, "Products", lambda: change_frame(sWin, pWin), tk.LEFT)
s_recipes_button = button(s_top_top_frame, "Recipes", lambda: change_frame(sWin, rWin), tk.LEFT)

# ==== Recipes Screen
# ==== Labels ====
r_product_label = label(r_right_frame, "Product", tk.TOP)
r_wax_label = label(r_right_frame, "Wax Amount", tk.TOP)
r_scent_amount_label = label(r_right_frame, "Scent Amount", tk.TOP)
r_message_label = label(r_bottom_bottom_frame, 'Candle Companion', tk.BOTTOM)
# ==== Entry Boxes ====
r_product_entry = entry(r_left_frame, tk.TOP)
r_wax_entry = entry(r_left_frame, tk.TOP)
r_scent_amount_entry = entry(r_left_frame, tk.TOP)

# ==== Buttons ====
r_main_button = button(r_top_top_frame, "Main", lambda: change_frame(rWin, rootWin), tk.LEFT)
r_materials_button = button(r_top_top_frame, "Materials", lambda: change_frame(rWin, mWin), tk.LEFT)
r_products_button = button(r_top_top_frame, "Products", lambda: change_frame(rWin, pWin), tk.LEFT)
r_sales_button = button(r_top_top_frame, "Sales", lambda: change_frame(rWin, sWin), tk.LEFT)
r_enter_button = button(r_middle_top_frame, "Enter", datab.add_recipe, tk.LEFT)
r_delete_button = button(r_middle_top_frame, "Delete", datab.delete_recipe, tk.LEFT)

# ==== Main Loop ========================================================================

root.bind('<Return>', datab.add_material)
root.mainloop()
print("Closing database connection")
datab.db.close()
