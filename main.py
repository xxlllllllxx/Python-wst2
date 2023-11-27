import tkinter as tk
from tkinter import messagebox as mb, ttk
import database as db

# MAIN FILE


def __main__():
    login = Login(tk.Tk())
    login.root.mainloop()
    # bypass -> for testing purposes
    # main = Main(tk.Tk(), db.login("admin", "admin"))
    # for faster debugging
    # root.bind("<FocusOut>", lambda event: event.widget.destroy())
    # main.root.mainloop()


class Login:
    def __init__(self, root: tk.Tk):
        # init the login attributes
        self.root = root
        self.root.title("Login")
        self.username_entry = tk.Entry(self.root)
        self.password_entry = tk.Entry(self.root, show="*")

        # Username label and entry
        username_label = tk.Label(self.root, text="Username:")
        username_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        # Password label and entry
        password_label = tk.Label(self.root, text="Password:")
        password_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Login button -> click event to login()
        login_button = tk.Button(self.root, text="Login", command=self.login)
        login_button.grid(row=2, column=0, columnspan=2, pady=10)

    # LOGIN Functionality

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        result = db.login(username, password)
        if result is not None:
            mb.showinfo("Login Success", f"Welcome {result[3]}")
            employee = tuple(result)
            self.root.destroy()
            Main(tk.Tk(), employee)
        else:
            mb.showwarning("Login Failed", "Username or Password Incorrect!")


class Main:
    def __init__(self, root: tk.Tk, employee: tuple):
        # init the attributes
        self.root = root
        self.root.title("Main")
        # self.root.geometry("600x500")
        self.username = employee[1]
        self.position = employee[3]

        self.selected_franchise = None

        # label for position
        tk.Label(self.root, text=f"USER:   {self.username}  ( {self.position} )").grid(
            column=0, row=0, sticky=tk.W)

        # innergrid -> Franchise Module
        self.grid_franchise = ttk.LabelFrame(self.root, text="Franchise Table")

        self.table_franchise = ttk.Treeview(self.grid_franchise, style="Treeview", height=5)

        # Add Franchise Buttons
        tk.Button(self.grid_franchise, text="ADD NEW", width=10).grid(column=1, row=0, sticky=tk.NSEW, padx=5, pady=[0, 10])

        # list franchise
        self.table_franchise["columns"] = db.cols_franchise

        self.column_design(self.table_franchise, "#0", "#", width=5)
        self.column_design(self.table_franchise, db.cols_franchise[0], "ID", width=50)
        self.column_design(self.table_franchise, db.cols_franchise[1], "OPERATOR", width=100)
        self.column_design(self.table_franchise, db.cols_franchise[2], "DRIVER", width=100)
        self.column_design(self.table_franchise, db.cols_franchise[3], "BODY #", width=50)
        self.column_design(self.table_franchise, db.cols_franchise[4], "PLATE #", width=80)
        self.column_design(self.table_franchise, db.cols_franchise[5], "LICENSE #", width=80)
        self.column_design(self.table_franchise, db.cols_franchise[6], "SHARES", width=100)

        self.populate_list(self.table_franchise, db.list_franchise())
        self.table_franchise.bind("<<TreeviewSelect>>", self.on_treeview_select)

        # franchise information -> hidden first
        self.franchise_information = tk.Frame(self.grid_franchise)
        self.franchise_information.columnconfigure(0, weight=1)
        self.franchise_information.columnconfigure(1, weight=2)
        self.franchise_information.columnconfigure(2, weight=1)
        self.franchise_information.columnconfigure(3, weight=2)
        self.franchise_information.columnconfigure(4, weight=1)

        self.franchise_information.rowconfigure(0, weight=1)
        self.franchise_information.rowconfigure(1, weight=1)
        self.franchise_information.rowconfigure(2, weight=1)
        self.franchise_information.rowconfigure(3, weight=1)
        self.franchise_information.rowconfigure(4, weight=1)

        # franchise information -> buttons
        tk.Button(self.franchise_information, text="UPDATE", width=10).grid(column=4, row=0, sticky=tk.NSEW, padx=5, pady=[0, 10])
        tk.Button(self.franchise_information, text="DELETE", width=10).grid(column=4, row=1, sticky=tk.NSEW, padx=5, pady=[0, 10])
        tk.Button(self.franchise_information, text="PAYMENT", width=10).grid(column=4, row=2, sticky=tk.NSEW, padx=5, pady=[0, 10])
        tk.Button(self.franchise_information, text="GENERATE ID", width=10).grid(column=4, row=3, sticky=tk.NSEW, padx=5, pady=[0, 10])
        tk.Button(self.franchise_information, text="FOLD", width=10, command=self.fold).grid(column=4, row=4, sticky=tk.NSEW, padx=5, pady=[0, 10])

        # franchise inputs
        tk.Label(self.franchise_information, text="ID: ").grid(column=0, row=0, sticky=tk.E)
        self.E_id = tk.Entry(self.franchise_information, relief=tk.GROOVE, bd=2)
        self.E_id.grid(column=1, row=0, sticky="NWE", padx=10, pady=5, ipadx=2, ipady=2)
        tk.Label(self.franchise_information, text="BODY #: ").grid(column=2, row=0, sticky=tk.E)
        self.E_bodynum = tk.Entry(self.franchise_information, relief=tk.GROOVE, bd=2)
        self.E_bodynum.grid(column=3, row=0, sticky="NWE", padx=10, pady=5, ipadx=2, ipady=2)

        tk.Label(self.franchise_information, text="OPERATOR: ").grid(column=0, row=1, sticky=tk.E)
        self.E_operator = tk.Entry(self.franchise_information, relief=tk.GROOVE, bd=2)
        self.E_operator.grid(column=1, row=1, sticky="NWE", padx=10, pady=5, columnspan=3, ipadx=2, ipady=2)
        tk.Label(self.franchise_information, text="DRIVER: ").grid(column=0, row=2, sticky=tk.E)
        self.E_driver = tk.Entry(self.franchise_information, relief=tk.GROOVE, bd=2)
        self.E_driver.grid(column=1, row=2, sticky="NWE", padx=10, pady=5, columnspan=3, ipadx=2, ipady=2)

        tk.Label(self.franchise_information, text="PLATE #: ").grid(column=0, row=3, sticky=tk.E)
        self.E_platenum = tk.Entry(self.franchise_information, relief=tk.GROOVE, bd=2)
        self.E_platenum.grid(column=1, row=3, sticky="NWE", padx=10, pady=5, ipadx=2, ipady=2)
        tk.Label(self.franchise_information, text="LICENSE #: ").grid(column=2, row=3, sticky=tk.E)
        self.E_license = tk.Entry(self.franchise_information, relief=tk.GROOVE, bd=2)
        self.E_license.grid(column=3, row=3, sticky="NWE", padx=10, pady=5, ipadx=2, ipady=2)

        # grid connections
        self.table_franchise.grid(column=0, row=1, sticky=tk.NSEW, padx=5, pady=5, columnspan=3)

        self.grid_franchise.grid(column=0, row=1, padx=10, pady=10, sticky=tk.NSEW)
        self.grid_franchise.columnconfigure(0, weight=5)
        self.grid_franchise.columnconfigure(1, weight=1)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # styles
        style = ttk.Style()
        style.configure("Treeview", rowheight=14, font=("Arial", 8))
        style.configure("Treeview.Heading", font=("Arial", 8, "bold"))

    # populate the selected tree with the list
    def populate_list(self, tree: ttk.Treeview, list: tuple):
        for row in list:
            tree.insert("", tk.END, values=row)

    # column designing for treeviews
    def column_design(self, tree: ttk.Treeview, header: str, title: str, width=30, **kwargs):
        tree.heading(header, text=title)
        tree.column(header, width=width, **kwargs)

    # selected treeview binding
    def on_treeview_select(self, event):
        self.franchise_information.grid(column=0, row=2, sticky=tk.NSEW, padx=5, pady=5, columnspan=2)
        selected_item = self.table_franchise.selection()[0]
        self.selected_franchise = self.table_franchise.item(selected_item, "values")

        # clear input
        self.E_id.delete(0, tk.END)
        self.E_operator.delete(0, tk.END)
        self.E_driver.delete(0, tk.END)
        self.E_bodynum.delete(0, tk.END)
        self.E_platenum.delete(0, tk.END)
        self.E_license.delete(0, tk.END)

        # populate input
        self.E_id.insert(0, self.selected_franchise[0])
        self.E_operator.insert(0, self.selected_franchise[1])
        self.E_driver.insert(0, self.selected_franchise[2])
        self.E_bodynum.insert(0, self.selected_franchise[3])
        self.E_platenum.insert(0, self.selected_franchise[4])
        self.E_license.insert(0, self.selected_franchise[5])

    def fold(self):
        self.franchise_information.grid_forget()


# to initialize all the above code before execution
if __name__ == "__main__":
    __main__()
