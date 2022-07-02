import tkinter as tk

import __main__ as main


class Database(object):
    def __init__(self, db, cur):
        self.db = db
        self.cur = cur

    def create_table(self):
        try:
            self.db.connect("db.sqlite")
            self.db.execute("CREATE TABLE IF NOT EXISTS materials (ingredient TEXT NOT NULL COLLATE NOCASE, quantity "
                            "INTEGER NOT NULL, cost REAL NOT NULL)")
            self.db.execute("CREATE TABLE IF NOT EXISTS products (product TEXT NOT NULL COLLATE NOCASE, size REAL "
                            "NOT NULL, scent TEXT NOT NULL COLLATE NOCASE, decoration_1 TEXT COLLATE NOCASE, "
                            "decoration_2 TEXT COLLATE NOCASE, quantity INTEGER NOT NULL, price REAL NOT NULL)")
            self.db.execute("CREATE TABLE IF NOT EXISTS recipes (product TEXT NOT NULL COLLATE NOCASE, wax_amount "
                            "REAL NOT NULL, scent_amount REAL NOT NULL)")
        except Exception as DatabaseError:
            print("Database failed to initialise {}".format(DatabaseError))
        exit()

    def refresh_materials(self):
        for item in main.materials_tree.get_children():
            main.materials_tree.delete(item)
        for mat in self.db.execute("SELECT * FROM materials ORDER BY materials.ingredient"):
            main.materials_tree.insert('', tk.END, values=mat)

    def refresh_products(self):
        for item in main.product_tree.get_children():
            main.product_tree.delete(item)
        for prod in self.db.execute("SELECT * FROM products ORDER BY products.product"):
            main.product_tree.insert('', tk.END, values=prod)

    def refresh_recipes(self):
        for item in main.rec_tree.get_children():
            main.rec_tree.delete(item)
        for recipe in self.db.execute("SELECT * FROM recipes ORDER BY recipes.product"):
            main.rec_tree.insert('', tk.END, values=recipe)

    def add_material(self):
        try:
            if str(main.m_ingredient_entry.get()).isalpha() and len(main.m_ingredient_entry.get()) > 0:
                if int(main.m_quantity_entry.get()) and len(main.m_quantity_entry.get()) > 0:
                    if float(main.m_cost_entry.get()) and len(main.m_cost_entry.get()) > 0:
                        exists = self.cur.execute(
                            "SELECT ingredient FROM materials WHERE (ingredient=? and cost=?)",
                            (main.m_ingredient_entry.get(), main.m_cost_entry.get())).fetchall()
                        if not exists:
                            self.db.execute("INSERT INTO materials VALUES(?, ?, ?)",
                                            (str(main.m_ingredient_entry.get()),
                                             float(main.m_quantity_entry.get()),
                                             float(main.m_cost_entry.get())))
                            self.db.commit()
                            self.refresh_materials()
                            main.m_message_label.config(
                                text="{} {} {} added".format(main.m_ingredient_entry.get(),
                                                             main.m_quantity_entry.get(),
                                                             main.m_cost_entry.get()))
                        else:
                            fetch = self.cur.execute(
                                "SELECT quantity FROM materials WHERE (ingredient=? and cost=?)",
                                (main.m_ingredient_entry.get(),
                                 main.m_cost_entry.get())).fetchone()
                            orig_qty = fetch[0]
                            add_qty = float(main.m_quantity_entry.get())
                            new_qty = orig_qty + add_qty
                            print(new_qty)
                            print(fetch)
                            update = "UPDATE materials SET quantity=? WHERE ingredient=? and cost=?"

                            self.cur.execute(update, (
                                new_qty, main.m_ingredient_entry.get(), main.m_cost_entry.get()))
                            self.db.commit()
                            self.refresh_materials()
                            main.m_message_label.config(text="Field updated")
                    else:
                        main.m_message_label.config(text="Cost must be a decimal number and cannot be empty")

                else:
                    main.m_message_label.config(text="Scent name must be a word and cannot be empty")
            else:
                main.m_message_label.config(text="ingredient name must be a word and cannot be empty")
        except Exception as AddError:
            main.m_message_label.config(text="Data entry failed {}".format(AddError))
            self.db.rollback()
            self.refresh_materials()
        finally:
            main.m_ingredient_entry.delete(0, tk.END)
            main.m_quantity_entry.delete(0, tk.END)
            main.m_cost_entry.delete(0, tk.END)

    def add_product(self):
        try:
            if str(main.p_product_entry.get()).isalpha() and len(main.p_product_entry.get()) > 0:
                if float(main.p_size_entry.get()):
                    if str(main.p_scent_entry.get()).isalpha() and len(main.p_scent_entry.get()) > 0:
                        if int(main.p_quantity_entry.get()) and len(main.p_quantity_entry.get()) > 0:
                            if float(main.p_price_entry.get()) and len(main.p_price_entry.get()) > 0:

                                exists = self.cur.execute(
                                    "SELECT product FROM products WHERE ("
                                    "product=? and size=? and scent=? and decoration_1=? and decoration_2=? and "
                                    "price=?)",
                                    (main.p_product_entry.get(), main.p_size_entry.get(), main.p_scent_entry.get(),
                                     main.p_decorator_1_entry.get(), main.p_decorator_2_entry.get(),
                                     main.p_price_entry.get())).fetchall()
                                if not exists:
                                    self.db.execute("INSERT INTO products VALUES(?, ?, ?, ?, ?, ?, ?)",
                                                    (str(main.p_product_entry.get()), str(main.p_size_entry.get()),
                                                     str(main.p_scent_entry.get()),
                                                     str(main.p_decorator_1_entry.get()),
                                                     str(main.p_decorator_2_entry.get()),
                                                     float(main.p_quantity_entry.get()),
                                                     float(main.p_price_entry.get())))
                                    self.db.commit()
                                    self.refresh_products()
                                    main.p_message_label.config(
                                        text="{} x {}g {} with {} scent {} and {} for {} added".format(
                                            main.p_quantity_entry.get().lower(), main.p_size_entry.get().lower(),
                                            main.p_product_entry.get().lower(), main.p_scent_entry.get().lower(),
                                            main.p_decorator_1_entry.get().lower(),
                                            main.p_decorator_2_entry.get().lower(),
                                            main.p_price_entry.get().lower()))
                                else:
                                    fetch = self.cur.execute(
                                        "SELECT quantity FROM products WHERE (product=? and size=? and scent=? "
                                        "and decoration_1=? and decoration_2=? and price=?)",
                                        (main.p_product_entry.get(), main.p_size_entry.get(), main.p_scent_entry.get(),
                                         main.p_decorator_1_entry.get(), main.p_decorator_2_entry.get(),
                                         main.p_price_entry.get())).fetchone()
                                    orig_qty = fetch[0]
                                    add_qty = float(main.p_quantity_entry.get())
                                    new_qty = orig_qty + add_qty
                                    update = "UPDATE products SET quantity=? WHERE (product=? and size=? and scent=? " \
                                             "and decoration_1=? and decoration_2=? and price=?) "
                                    self.cur.execute(update, (
                                        new_qty, main.p_product_entry.get(), main.p_size_entry.get(),
                                        main.p_scent_entry.get(),
                                        main.p_decorator_1_entry.get(), main.p_decorator_2_entry.get(),
                                        main.p_price_entry.get()))
                                    self.refresh_products()
                                    main.p_message_label.config(
                                        text="{} quantity increased to {}".format(main.p_product_entry.get(), new_qty))
                            else:
                                main.p_message_label.config(text="Price must be a decimal number and cannot be empty")
                        else:
                            main.p_message_label.config(text="Price must be a decimal number and cannot be empty")
                    else:
                        main.p_message_label.config(text="Scent name must be a word and cannot be empty")
                else:
                    main.p_message_label.config(text="Size must be a number")
            else:
                main.p_message_label.config(text="Product name must be a word and cannot be empty")
        except Exception as AddProductError:
            main.error(AddProductError)
            main.p_message_label.config(text="Data entry failed {}".format(AddProductError))
            self.db.rollback()
            self.refresh_products()
        finally:
            main.p_product_entry.delete(0, tk.END)
            main.p_size_entry.delete(0, tk.END)
            main.p_scent_entry.delete(0, tk.END)
            main.p_decorator_1_entry.delete(0, tk.END)
            main.p_decorator_2_entry.delete(0, tk.END)
            main.p_quantity_entry.delete(0, tk.END)
            main.p_price_entry.delete(0, tk.END)

    def add_recipe(self):
        try:
            if str(main.r_product_entry.get()).isalpha() and len(main.r_product_entry.get()) > 0:
                if float(main.r_wax_entry.get()) and len(main.r_wax_entry.get()) > 0:
                    if float(main.r_scent_amount_entry.get()) and len(main.r_scent_amount_entry.get()) > 0:
                        exists = self.cur.execute(
                            "SELECT product FROM recipes WHERE (product=? and wax_amount=? and scent_amount=?)",
                            (main.r_product_entry.get(), main.r_wax_entry.get(),
                             main.r_scent_amount_entry.get())).fetchall()
                        if not exists:
                            self.db.execute("INSERT INTO recipes VALUES(?, ?, ?)",
                                            (str(main.r_product_entry.get()),
                                             float(main.r_wax_entry.get()),
                                             float(main.r_scent_amount_entry.get())))
                            self.db.commit()
                            self.refresh_recipes()
                            main.m_message_label.config(
                                text="{} {} {} added".format(main.r_product_entry.get(),
                                                             main.r_wax_entry.get(),
                                                             main.r_scent_amount_entry.get()))
                        else:
                            main.r_message_label.config(text="Recipe already exists")
                    else:
                        main.r_message_label.config(text="Scent Amount must be a decimal number and cannot be empty")

                else:
                    main.r_message_label.config(text="Wax amount must be a number and cannot be empty")
            else:
                main.r_message_label.config(text="Product name must be a word and cannot be empty")
        except Exception as AddError:
            main.r_message_label.config(text="Data entry failed {}".format(AddError))
            self.db.rollback()
            self.refresh_recipes()
        finally:
            main.r_product_entry.delete(0, tk.END)
            main.r_wax_entry.delete(0, tk.END)
            main.r_scent_amount_entry.delete(0, tk.END)

    def delete_ingredient(self):
        try:
            query = "DELETE FROM materials WHERE ingredient=? and quantity=? and cost=?"
            selection = (main.m_ingredient_entry.get(), main.m_quantity_entry.get(), main.m_cost_entry.get())
            self.cur.execute(query, selection)
            main.m_message_label.config(text="Entry deleted")
            self.db.commit()
            self.refresh_materials()
        except Exception as DeleteError:
            main.m_message_label.config(text="Failed to remove field {}".format(DeleteError))
            self.db.rollback()
            self.refresh_materials()

    def delete_product(self):
        try:
            query = "DELETE FROM products WHERE product=? and size=? and scent=? and decoration_1=? and " \
                    "decoration_2=? and quantity=? and price=? "
            selection = (
                main.p_product_entry.get(), main.p_size_entry.get(), main.p_scent_entry.get(),
                main.p_decorator_1_entry.get(),
                main.p_decorator_2_entry.get(), main.p_quantity_entry.get(),
                main.p_price_entry.get())
            self.cur.execute(query, selection)
            main.p_message_label.config(text="Entry deleted")
            self.db.commit()
            self.refresh_products()
        except Exception as DeleteProductError:
            main.error(DeleteProductError)
            main.p_message_label.config(text="Failed to remove field {}".format(DeleteProductError))
            self.db.rollback()
            self.refresh_products()

    def delete_recipe(self):
        try:
            query = "DELETE FROM recipes WHERE product=? and wax_amount=? and scent_amount=?"
            selection = (main.r_product_entry.get(), main.r_wax_entry.get(), main.r_scent_amount_entry.get())
            self.cur.execute(query, selection)
            main.m_message_label.config(text="Entry deleted")
            self.db.commit()
            self.refresh_recipes()
        except Exception as DeleteError:
            main.m_message_label.config(text="Failed to remove field {}".format(DeleteError))
            self.db.rollback()
            self.refresh_recipes()
