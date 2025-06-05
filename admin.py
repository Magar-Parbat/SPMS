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

    def add_users(self):

        messagebox.showinfo("Info", "This feature is under development.")
    
    def update_users(self):

        messagebox.showinfo("Info", "This feature is under development.")

    def manage_courses(self):

        messagebox.showinfo("Info", "This feature is under development.")


if __name__ == "__main__":
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()
    