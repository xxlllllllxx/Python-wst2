# PYTHON PROJECT
# WST 2: Web And Mobile Developmnent 2
# Python CRUD
# Masallo, Calim, Estrella

import tkinter as tk
import mysql.connector as mc
from tkinter import messagebox as mb, ttk

# CONFIGURATIONS
host = "localhost"
port = "3306"
database = "db_wst_project"
dbuser = "root"
dbpass = ""

# Tables
# "tbl_employee", ["id", "username", "password", "position", "isDeleted"]
tbl_f = "tbl_franchise"
f_arr = ["id", "driver_name", "body_number", "plate_number", "license_number", "isDeleted"]

# Display Tkinbters
root = tk.Tk()


def login_ui():
    root.title("Login")
    root.geometry("250x110")
    root.columnconfigure(1, weight=1)

    tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

    # init variables for inputs
    username = tk.StringVar()
    password = tk.StringVar()

    tk.Entry(root, textvariable=username).grid(row=0, column=1, padx=5, pady=5, sticky="WE")
    tk.Entry(root, textvariable=password, show="*").grid(row=1, column=1, padx=5, pady=5, sticky="WE")

    tk.Button(root, text="Login", command=lambda: login(username.get(), password.get()), width=20).grid(row=2, column=0, columnspan=2, pady=[10, 20])


def main_ui(position: str):
    root.title("Main")
    root.geometry("600x430")
    tk.Label(root, text=f"LoggedIn as: {position}").grid(row=0, column=0, sticky=tk.W)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=5)
    root.columnconfigure(2, weight=1)

    # init variables for inputs
    f_id = tk.StringVar()
    f_driver_name = tk.StringVar()
    f_body_number = tk.StringVar()
    f_plate_number = tk.StringVar()
    f_license_number = tk.StringVar()

    data_tuple = (f_id, f_driver_name, f_body_number, f_plate_number, f_license_number)

    # tree
    main_tree = ttk.Treeview(root)
    main_tree.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)
    main_tree["columns"] = ["id", "driver_name", "body_number", "plate_number", "license_number"]

    column_header_bind(main_tree, "#0", "#", width=5)
    column_header_bind(main_tree, "id", "ID", width=10, anchor=tk.CENTER)
    column_header_bind(main_tree, "driver_name", "DRIVER NAME", width=100)
    column_header_bind(main_tree, "body_number", "BODY #", width=50, anchor=tk.CENTER)
    column_header_bind(main_tree, "plate_number", "PLATE NUMBER", width=80, anchor=tk.CENTER)
    column_header_bind(main_tree, "license_number", "LICENSE NUMBER", width=80, anchor=tk.CENTER)

    # populate the tree
    retrieve(main_tree, data_tuple)

    # binding for tree
    main_tree.bind("<<TreeviewSelect>>", lambda event:  main_tree_select(main_tree, data_tuple))

    # input labels
    tk.Label(root, text="Selected id:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
    tk.Label(root, text="Driver name:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
    tk.Label(root, text="Body Number:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
    tk.Label(root, text="Plate Number:").grid(row=5, column=0, padx=10, pady=5, sticky=tk.E)
    tk.Label(root, text="License Number:").grid(row=6, column=0, padx=10, pady=5, sticky=tk.E)

    # input widget
    tk.Entry(root, textvariable=f_id, state="readonly").grid(row=2, column=1, padx=5, pady=5, sticky="W")
    tk.Entry(root, textvariable=f_driver_name).grid(row=3, column=1, padx=5, pady=5, sticky="WE")
    tk.Entry(root, textvariable=f_body_number).grid(row=4, column=1, padx=5, pady=5, sticky="WE")
    tk.Entry(root, textvariable=f_plate_number).grid(row=5, column=1, padx=5, pady=5, sticky="WE")
    tk.Entry(root, textvariable=f_license_number).grid(row=6, column=1, padx=5, pady=5, sticky="WE")

    # buttons
    tk.Button(root, text="REFRESH", command=lambda: retrieve(main_tree, data_tuple)).grid(row=1, column=2, sticky="NEW")
    tk.Button(root, text="CLEAR", command=lambda: clear(data_tuple)).grid(row=2, column=2, sticky="WE")
    tk.Button(root, text="INSERT", command=lambda: create(main_tree, data_tuple)).grid(row=3, column=2, sticky="WE")
    tk.Button(root, text="UPDATE", command=lambda: update(main_tree, data_tuple)).grid(row=4, column=2, sticky="WE")
    tk.Button(root, text="DELETE", command=lambda: delete(main_tree, data_tuple)).grid(row=5, column=2, sticky="WE")


def get_connection() -> mc.MySQLConnection:
    # Make connection to database
    try:
        conn = mc.connect(host=host, port=port, database=database, user=dbuser, password=dbpass)
        return conn
    except mc.Error as err:  # Error Handling
        mb.showerror("Error", err)


def create(tree: ttk.Treeview, data: tuple):
    if check(data):
        try:
            # Create entries using INSERT INTO with parameterized query
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"""INSERT INTO {tbl_f} VALUES (NULL, %s, %s, %s, %s, 0)""", (data[1].get(), data[2].get(), data[3].get(), data[4].get()))
            conn.commit()

            mb.showinfo("Insert Success", f"Franchise body number: {data[2].get()} added.")
            clear(data)
            retrieve(tree, data)
        except Exception as e:
            mb.showerror("Insert Failed", f"Failed to add body number: {data[2].get()}\nError: {str(e)}")
        finally:
            conn.close()


def retrieve(tree: ttk.Treeview, data: tuple):
    try:
        # Retrieve table using SELECT
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {tbl_f} WHERE {f_arr[5]} = 0")
        result = cursor.fetchall()
        conn.commit()

        # clean the tree
        tree.delete(*tree.get_children())
        clear(data)
        # insert the fresh rows
        for row in result:
            tree.insert("", tk.END, values=row)
    except Exception as e:
        mb.showerror("Retieve Failed", f"Failed to retrieve table")
    finally:
        conn.close()


def update(tree: ttk.Treeview, data: tuple):
    if check(data):
        try:
            # Update entries using UPDATE with parameterized query
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"""UPDATE {tbl_f} SET {f_arr[1]}=%s, {f_arr[2]}=%s, {f_arr[3]}=%s, {f_arr[4]}=%s WHERE {f_arr[0]}=%s;""",
                           (data[1].get(), data[2].get(), data[3].get(), data[4].get(), int(data[0].get())))
            conn.commit()
            mb.showinfo("Update Success", f"Franchise ID {int(data[0].get())} updated.")
            clear(data)
            retrieve(tree, data)
        except Exception as e:
            # Handle exceptions
            mb.showerror("Update Failed", f"Failed to update Franchise ID {data[0].get()}\nError: {str(e)}")
        finally:
            conn.close()


def delete(tree: ttk.Treeview, data: tuple):
    if check(data):
        try:
            # Delete selected id using soft deletion UPDATE set isDeleted to 1
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {tbl_f} SET {f_arr[5]} = 1 WHERE {f_arr[0]}={data[0].get()};")
            conn.commit()

            mb.showinfo("Delete Success", f"Franchise bodynumber: {data[2].get()} deleted.")
            clear(data)
            retrieve(tree, data)
        except Exception as e:
            mb.showerror("Update Failed", f"Failed to delete Franchise ID {data[0].get()}\nError: {str(e)}")
        finally:
            conn.close()


def login(username_val: str, password_val: str):
    try:
        # login functionality -> returns the position of the user if logged in
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT position, username FROM tbl_employee WHERE username=%s AND password=%s AND isDeleted=0", (username_val, password_val))
        result = cursor.fetchone()
        conn.commit()
        if result is not None:
            mb.showinfo("Login Success", f"Welcome {str.capitalize(result[0])} {str.capitalize(result[1])}!")
            # clean the root of login ui
            for widget in root.winfo_children():
                widget.grid_forget()
            # repopultate root with new ui
            main_ui(result[0])
        else:
            mb.showwarning("Login Failed", "Username and Password not found!")
    except Exception as e:
        mb.showerror("Login Failed", "Database error")
    finally:
        conn.close()


def main_tree_select(tree: ttk.Treeview, data: tuple):
    # This is the selecton event of tree
    selection = tree.selection()
    if selection:
        values = tree.item(selection[0], "value")
        data[0].set(values[0])
        data[1].set(values[1])
        data[2].set(values[2])
        data[3].set(values[3])
        data[4].set(values[4])


def column_header_bind(tree: ttk.Treeview, header: str, title: str, **kwargs):
    # designing the columns with heading
    tree.heading(header, text=title)
    tree.column(header, **kwargs)


def clear(data: tuple):
    # clearing the input fields
    for res in data:
        res.set("")


def check(data: tuple) -> bool:
    # Checking the input for None values
    sub = data[1:]
    for value in sub:
        if value is None or value.get() == "":
            mb.showwarning("Incomplete fields", "Some input fields are empty\nSelect from the list then continue")
            return False

    return True


# open login UI
login_ui()
root.mainloop()
