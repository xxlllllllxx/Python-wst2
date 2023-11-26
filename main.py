import tkinter as tk
from tkinter import messagebox as mb, ttk
import database as db

# MAIN FILE


def __main__():
    # login = Login(tk.Tk())
    # login.root.mainloop()
    # bypass -> for testing purposes
    main = Main(tk.Tk(), db.login("admin", "admin"))
    # for faster debugging
    main.root.bind("<FocusOut>", lambda event: event.widget.destroy())
    main.root.mainloop()


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
        # init the login attributes
        self.root = root
        self.root.title("Main")
        self.root.geometry("600x500")
        self.username = employee[1]
        self.position = employee[3]

        # label for position
        tk.Label(self.root, text=f"USER:   {self.username}  ( {self.position} )").grid(
            column=0, row=0, sticky=tk.W)

        # innergrid -> Franchise Module
        grid_franchise = ttk.LabelFrame(self.root, text="Franchise Table")

        table_franchise = ttk.Treeview(grid_franchise, style="Treeview")

        # list franchise
        table_franchise["columns"] = db.cols_franchise

        self.column_design(table_franchise,
                           "#0", "", width=5)
        self.column_design(table_franchise,
                           db.cols_franchise[0], "ID", width=5)
        self.column_design(table_franchise,
                           db.cols_franchise[1], "OPERATOR", width=50)
        self.column_design(table_franchise,
                           db.cols_franchise[2], "DRIVER", width=50)
        self.column_design(table_franchise,
                           db.cols_franchise[3], "BODY #", width=30)
        self.column_design(table_franchise,
                           db.cols_franchise[4], "PLATE #", width=30)
        self.column_design(table_franchise,
                           db.cols_franchise[5], "LICENSE #", width=50)
        self.column_design(table_franchise,
                           db.cols_franchise[6], "SHARES", width=30)

        self.populate_list(table_franchise, db.list_franchise())

        # Franchise Buttons
        tk.Button(grid_franchise, text="INSERT", width=10).grid(
            column=0, row=1, sticky=tk.NSEW, padx=5, pady=[0, 10])
        tk.Button(grid_franchise, text="UPDATE", width=10).grid(
            column=1, row=1, sticky=tk.NSEW, padx=5, pady=[0, 10])
        tk.Button(grid_franchise, text="DELETE", width=10).grid(
            column=2, row=1, sticky=tk.NSEW, padx=5, pady=[0, 10])

        # grid connections
        table_franchise.grid(column=0, row=0, sticky=tk.NSEW,
                             padx=5, pady=5, columnspan=3)

        grid_franchise.grid(column=0, row=1, padx=10, pady=10, sticky="NEW")
        grid_franchise.columnconfigure(0, weight=1)
        grid_franchise.columnconfigure(1, weight=1)
        grid_franchise.columnconfigure(2, weight=1)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # styles
        style = ttk.Style()
        style.configure("Treeview", rowheight=14, font=('Arial', 8))
        style.configure("Treeview.Heading", font=('Arial', 8, 'bold'))

    # populate the selected tree with the list
    def populate_list(self, tree: ttk.Treeview, list: tuple):
        for row in list:
            tree.insert("", tk.END, values=row)

    # column designing for treeviews
    def column_design(self, tree: ttk.Treeview, header: str, title: str, width=30, **kwargs):
        tree.heading(header, text=title)
        tree.column(header, width=width, **kwargs)


# to initialize all the above code before execution
if __name__ == "__main__":
    __main__()
