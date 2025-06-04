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

    def manage_courses(self):

        messagebox.showinfo("Info", "This feature is under development.")
    
    def view_users(self):

        messagebox.showinfo("Info", "This feature is under development.")

    def add_users(self):

        messagebox.showinfo("Info", "This feature is under development.")
    
    def update_users(self):

        messagebox.showinfo("Info", "This feature is under development.")


if __name__ == "__main__":
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()
    