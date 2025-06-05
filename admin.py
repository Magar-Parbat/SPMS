import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 
import os 

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.geometry("600x400")
        self.root.configure() # for background color

        self.show_dashboard() # call this to show the main screen
    
    def show_dashboard(self):

        self.clear_window()

        title = tk.Label(self.root, text="Admin Dashboard", font=("Arial", 14))
        title.pack(pady=20)

        tk.Button(self.root, text="Manage Users", command=self.manage_users).pack(pady=10)
        tk.Button(self.root, text="Manage Courses", command=self.manage_courses).pack(pady=10)
        tk.Button(self.root, text="Exit", command = self.root.quit).pack(pady=10)
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def manage_users(self):

        self.clear_window()

        self.root.geometry("600x400")

        tk.Label(self.root, text="Manage Users", font=("Arial", 14)).pack(pady=20)
        tk.Button(self.root, text="View Users", command=self.view_users).pack(pady=10)
        tk.Button(self.root, text="Add User", command=self.add_users).pack(pady=10)
        tk.Button(self.root, text="Update / Delete User", command=self.update_users).pack(pady=10)

        tk.Button(self.root, text="Back", command=self.show_dashboard).pack(pady=10)
    
    def view_users(self):

        self.clear_window()
        self.root.geometry("800x600")
        tk.Label(self.root, text="Users List", font=("Arial", 14)).pack(pady=20)

        # Read and seprate data from users.txt

        admins = []
        students = []

        try:
            with open("data/users.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if len(data) == 3:
                        if data[2] == "Admin":
                            admins.append(data)
                        else:
                            students.append(data)
        
        except FileNotFoundError:
            messagebox.showerror("Error", "Users file not found.")
            return
        
        # create admin table

        tk.Label(self.root, text="Admins", font=("Arial", 12)).pack(pady=5)

        admin_columns = ("sn", "username", "fullname", "role")
        admin_tree = ttk.Treeview(self.root, columns=admin_columns, show="headings", height=5)

        # headings
        admin_tree.heading("sn", text="SN")
        admin_tree.heading("username", text="Username")
        admin_tree.heading("fullname", text="Full Name")
        admin_tree.heading("role", text="Role")

        # column size
        admin_tree.column("sn", width=40, anchor="center")
        admin_tree.column("username", width=120, anchor="w")
        admin_tree.column("fullname", width=180, anchor="w")
        admin_tree.column("role", width=80, anchor="center")

        for idx, admin in enumerate(admins, start=1):
            admin_tree.insert("", tk.END, values=(idx, *admin))
        
        admin_tree.pack(pady=5, padx=20, fill=tk.BOTH)
    
        # Add a scrollbar for admin table

        # create a student table
        tk.Label(self.root, text="Students", font=("Arial", 12)).pack(pady=5)

        student_columns = ("sn", "username", "fullname", "role")
        student_tree = ttk.Treeview(self.root, columns=student_columns, show="headings", height=5)

        # set headings
        student_tree.heading("sn", text="SN")
        student_tree.heading("username", text="Username")
        student_tree.heading("fullname", text="Full Name")
        student_tree.heading("role", text="Role")

        # set column size
        student_tree.column("sn", width=40, anchor="center")
        student_tree.column("username", width=120, anchor="w")
        student_tree.column("fullname", width=180, anchor="w")
        student_tree.column("role", width=80, anchor="center")

        for idx, student in enumerate(students, start=1):
            student_tree.insert("", tk.END, value=(idx, *student))
        
        student_tree.pack(pady=5, padx=20, fill=tk.BOTH)

        # Add a scrollbar for student table
    
        tk.Button(self.root, text="Back", command=self.manage_users).pack(pady=10)

    def add_users(self):

        self.clear_window()
        self.root.geometry("600x500")

        tk.Label(self.root, text="Create Account", font=("Arial", 14)).pack(pady=20)

        tk.Label(self.root, text="Username:").pack(pady=5)
        username_entry = tk.Entry(self.root)
        username_entry.pack(pady=5)

        tk.Label(self.root, text="Full Name:").pack(pady=5)
        fullname_entry = tk.Entry(self.root)
        fullname_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack(pady=5)

        tk.Label(self.root, text="Confirm Password:").pack(pady=5)
        confirm_password_entry = tk.Entry(self.root, show="*")
        confirm_password_entry.pack(pady=5)

        tk.Label(self.root, text="Role:").pack(pady=5)
        self.role_var = tk.StringVar(value="Student") # default role
        tk.Radiobutton(self.root, text="Admin", variable=self.role_var, value="Admin").pack(pady=5)
        tk.Radiobutton(self.root, text="Student", variable=self.role_var, value="Student").pack(pady=5)

        def create_account():

            username = username_entry.get().strip()
            fullname = fullname_entry.get().strip()
            password = password_entry.get().strip()
            confirm_password = confirm_password_entry.get().strip()
            role = self.role_var.get()

            # if any field is empty
            if not username or not fullname or not password or not confirm_password:
                messagebox.showerror("Error", "All fields are required.")
                return
            
            # if password and confirm password do not match
            if password != confirm_password:
                messagebox.showerror("Error", "Password do not match.")
                return
            
            # if usename already exists
            try:
                with open("data/users.txt", "r") as file:
                    for line in file:
                        data = line.strip().split(",")
                        if data[0] == username:
                            messagebox.showerror("Error", "Username already exists.")
                            return
            except FileNotFoundError:
                messagebox.showerror("Error", "Users file not found.")
                return
            
            # if all checks pass, create account
            try: 
                with open("data/users.txt", "a") as file:
                    file.write(f"{username},{fullname},{role}\n")
                with open("data/passwords.txt", "a") as file:
                    file.write(f"{username},{password}\n")
                
                messagebox.showinfo("Success", "Account created successfully.")
                self.manage_users() # go back to manage users screen
            
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        tk.Button(self.root, text="Create Account", command=create_account).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.manage_users).pack(pady=10)
    
    def update_users(self):

        messagebox.showinfo("Info", "This feature is under development.")

    def manage_courses(self):

        messagebox.showinfo("Info", "This feature is under development.")


if __name__ == "__main__":
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()
    