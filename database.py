import config
from tkinter import messagebox as mb
import mysql.connector as mc
from mysql.connector import errorcode

# DATABASE CONNECTIONS
cols_employee = tuple(config.employee_columns[:-1])
cols_franchise = tuple(config.franchise_columns[:-1])


def get_connection() -> mc.MySQLConnection:
    try:
        conn = mc.connect(host=config.host, port=config.port,
                          database=config.database, user=config.user,
                          password=config.password)
        return conn
    except mc.Error as err:  # Error Handling
        mb.showerror("Error", err)


# simple login function -> return the tuple of employee or None
def login(username: str, password: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = f"SELECT * FROM {
            config.table_employee} WHERE username = %s AND password = %s AND isDeleted = 0;"
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

        query = f"SELECT * FROM {config.table_franchise} WHERE isDeleted = 0"
        cursor.execute(query)

        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return result

    except mc.Error as err:
        mb.showerror("Error", err)


if __name__ == "__main__":
    get_connection()
