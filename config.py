import mysql.connector as mc
from mysql.connector import errorcode
import tkinter as tk

# CONFIGURATIONS FILE

host = "localhost"
port = "3306"
database = "db_wst_project"
user = "root"
password = ""

# database tables
table_employee = "tbl_employee"
employee_columns = ["id",
                    "username",
                    "password",
                    "position",
                    "isDeleted"]
table_franchise = "tbl_franchise"
franchise_columns = ["id",
                     "operator_name",
                     "driver_name",
                     "body_number",
                     "plate_number",
                     "license_number",
                     "share_capital",
                     "isDeleted"]


# Test database connection
if __name__ == "__main__":
    try:
        conn = mc.connect(host=host, port=port,
                          database=database, user=user,
                          password=password)
        print("Database Connected")
    except mc.Error as err:  # Error Handling
        print("Database failed: ", err)
