from tkinter import messagebox as mb
import mysql.connector as mc
from mysql.connector import errorcode

# CONFIGURATIONS

host = "localhost"
port = "3306"
database = "db_wst_project"
user = "root"
password = ""

# database tables
table_employee = "tbl_employee"
employee_columns = ["id", "username", "password", "position", "isDeleted"]
table_franchise = "tbl_franchise"
franchise_columns = ["id", "operator_name", "driver_name", "body_number", "plate_number", "license_number", "share_capital", "isDeleted"]


# DATABASE CONNECTIONS
cols_employee = tuple(employee_columns[:-1])
cols_franchise = tuple(franchise_columns[:-1])


def get_connection() -> mc.MySQLConnection:
    try:
        conn = mc.connect(host=host, port=port, database=database, user=user, password=password)
        return conn
    except mc.Error as err:  # Error Handling
        mb.showerror("Error", err)


# simple login function -> return the tuple of employee or None
def login(username: str, password: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = f"SELECT * FROM {table_employee} WHERE username = %s AND password = %s AND isDeleted = 0;"
        cursor.execute(query, (username, password))

        result = cursor.fetchone()

        conn.commit()
        conn.close()

        return result
    except mc.Error as err:
        mb.showerror("Error", err)


def list_franchise():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = f"SELECT * FROM {table_franchise} WHERE isDeleted = 0"
        cursor.execute(query)

        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return result

    except mc.Error as err:
        mb.showerror("Error", err)


if __name__ == "__main__":
    get_connection()
