import tkinter as tk
from tkinter import messagebox

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def login_window():

    clear_window()

    title_label = tk.Label(root, text="Student Profile Managements System", font=("Arial", 14))
    title_label.pack(pady=20)

    tk.Label(root, text="Username:", font=("Arial", 10)).pack(pady=10)
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Password:", font=("Arial", 10)).pack(pady=10)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    def login():
        username = username_entry.get()
        password = password_entry.get()

        try:
            with open("data/passwords.txt", "r") as file:
                for line in file:
                    saved_username, saved_password = line.strip().split(",")

                    if username == saved_username and password == saved_password:

                        try: # check if the user is admin or student
                            with open("data/users.txt", "r") as user_file:
                                for user_line in user_file:
                                    user_data = user_line.strip().split(",")

                                    if len(user_data) == 3:
                                        file_username, fullname, role = [item.strip() for item in user_data]

                                        if username == file_username:
                                            if role == "Admin":
                                                clear_window()
                                                messagebox.showinfo("Success", "Admin Dashboard is under development.")

                                            else:
                                                messagebox.showinfo("Sucess", "Student Dashboard is under development.")
                        except FileNotFoundError:
                            messagebox.showerror("Error", "User data file not found.")
                            return
                        
                messagebox.showerror("Login failed", "Invalid username or password")
        
        except FileNotFoundError:
            messagebox.showerror("Error", "Password file not found.")

    tk.Button(root, text="Login", command=login).pack(pady=10)
    tk.Button(root, text="Create Account", command=create_account_window).pack(pady=10)
    tk.Button(root, text="Exit", command=create_account_window).pack(pady=10)

def create_account_window():

    clear_window()
    tk.Label(root, text="Create Account", font=("Arial", 14)).pack(pady = 14)

    tk.Label(root, text="Username").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Full Name").pack(pady=5)
    fullname_entry = tk.Entry(root)
    fullname_entry.pack()

    tk.Label(root, text="Password").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    tk.Label(root, text="Confirm Password").pack(pady=5)
    confirm_password_entry = tk.Entry(root, show="*")
    confirm_password_entry.pack()

    role_var = tk.StringVar(value="Student") # default role is Student
    tk.Label(root, text="Select Role").pack(pady=5)
    tk.Radiobutton(root, text="Student", value="Student", variable=role_var).pack()

    def create_account():
        username = username_entry.get()
        fullname = fullname_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get().strip()
        role = role_var.get()

        if not username or not fullname or not password or not confirm_password or not role:
            messagebox.showerror("Error", "Fill all the fields.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # check if the username already exists
        try:
            with opne("data/users.txt", "r") as user_file:
                for line in user_file:
                    saved_username = line.strip().split(",")[0]
                    if username == saved_username:
                        messagebox.showerror("Error", "Username already exists.")
                        return

        except FileNotFoundError:
            pass 
        
        try:
            with open("data/users.txt", "a") as user_file:
                user_file.write(f"{username},{fullname},{role}\n")

            with opne("data/passwords.txt", "a") as password_file:
                password_file.write(f"{username},{password}\n")

            messagebox.showinfo("Success",f"Accound Created for {fullname} as {role}.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating the account: {str(e)}")
            return
    
    tk.Button(root, text="Create Account", command=create_account).pack(pady=10)
    tk.Button(root, text="Back to Login", command=login_window).pack(pady=10)

# creating login window
root = tk.Tk()
root.title("Login")
root.geometry("400x500")
root.configure() # for background color

login_window() # calls the funtion to create and display the login window

root.mainloop() # start the Tkinter event loop to keep the window open and responsive 