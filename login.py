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

        # check if the username and password fields are empty
        if not username or not password:
            messagebox.showerror("Error", "Please fill in both fields.")
            return

        try:
            with open("data/passwords.txt", "r") as file:
                credentials = {}
                for line in file:
                    saved_username, saved_password = line.strip().split(",")
                    credentials[saved_username.strip()] = saved_password.strip()

            # check if username exists
            if username not in credentials:
                messagebox.showerror("Login failed", "Username doesn't exist.")
                return
            
            # check if the password matches
            if credentials[username] != password:
                messagebox.showerror("Login failed", "Incorrect password.")
                return

            try:
                with open("data/users.txt", "r") as user_file:
                    for user_line in user_file:
                        user_data = user_line.strip().split(",")
                        if len(user_data) == 3:
                            saved_username, fullname, role = [item.strip() for item in user_data]
                            if saved_username == username:
                                if role == "Student":
                                    messagebox.showinfo("Login Successful", f"Student dashboard is under development.")
                                else:
                                    messagebox.showinfo("Login Successful", f"Admin dashboard is under development.")
                                return
                # if username found i npasswords.txt but not in users.txt
                messagebox.showerror("Login failed", "User data not found.")

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while reading user data: {str(e)}")
                return

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

        # check if all fields are filled
        if not username or not fullname or not password or not confirm_password or not role:
            messagebox.showerror("Error", "Fill all the fields.")
            return
        
        # check if the password and confirm password match
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # check if the username already exists
        try:
            with open("data/users.txt", "r") as user_file:
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

            with open("data/passwords.txt", "a") as password_file:
                password_file.write(f"{username},{password}\n")

            messagebox.showinfo("Success",f"Accound Created for {fullname} as {role}.")

            '''
            # redirect to respective dashboard
            if role == "Student":
                open_admin_dashboard()
            else:
                open_student_dashboard()
            '''

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