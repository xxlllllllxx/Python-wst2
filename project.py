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
# "tbl_franchise", ["id", "driver_name", "body_number", "plate_number", "license_number", "isDeleted"]

# Display Tkinbters
root = tk.Tk()


def login_ui():
    root.title("Login")
    root.geometry("250x110")
    root.columnconfigure(1, weight=1)

    tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

    username = tk.StringVar()
    password = tk.StringVar()

    tk.Entry(root, textvariable=username).grid(row=0, column=1, padx=5, pady=5, sticky="WE")
    tk.Entry(root, textvariable=password, show="*").grid(row=1, column=1, padx=5, pady=5, sticky="WE")

    tk.Button(root, text="Login", command=lambda: login(username.get(), password.get()), width=20).grid(row=2, column=0, columnspan=2, pady=[10, 20])


def main_ui(position: str):
    root.title("Main")
    root.geometry("500x400")
    tk.Label(root, text=f"LoggedIn as: {position}").grid(row=0, column=0, sticky=tk.W)


def get_connection() -> mc.MySQLConnection:
    # Make connection to database
    try:
        conn = mc.connect(host=host, port=port, database=database, user=dbuser, password=dbpass)
        return conn
    except mc.Error as err:  # Error Handling
        mb.showerror("Error", err)


def create() -> bool:
    # Create entries using INSERT INTO
    pass


def retrieve():
    # Retrieve list using SELECT
    pass


def update(id: int) -> bool:
    # Update selected id using UPDATE
    pass


def delete(id: int) -> bool:
    # Delete selected id using soft deletion UPDATE set isDeleted to 1
    pass


def login(username_val: str, password_val: str):
    # login functionality -> returns the position of the user if logged in
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT position FROM tbl_employee WHERE username=%s AND password=%s AND isDeleted=0", (username_val, password_val))
    result = cursor.fetchone()
    if result is not None:
        # clean the root of login ui
        for widget in root.winfo_children():
            widget.grid_forget()
        # repopultate root with new ui
        main_ui(result[0])
    else:
        mb.showwarning("Login Failed", "Username and Password not found!")


login_ui()
root.mainloop()
