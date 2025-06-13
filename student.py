import tkinter as tk
from tkinter import messagebox

class StudentDashboard:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Student Dashboard")
        self.root.geometry("600x400")
        self.root.configure # for background color

        self.show_student_dashboard() 

    def show_student_dashboard(self):

        self.clear_window()

        title = tk.Label(self.root, text="Student Dashboard", font=("Arial", 14))
        title.pack(pady=20)

        tk.Button(self.root, text="Edit Your Account", command=self.edit_account).pack(pady=10)
        tk.Button(self.root, text="View Grades", command=self.view_grades).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def edit_account(self):

        self.clear_window()
        self.root.geometry("500x400")

        tk.Label(self.root, text="Edit Your Account", font=("Arial", 14)).pack(pady=20)

        # Get current user details
        fullname = ""
        try:
            with open("data/users.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if data[0] == self.username:
                        fullname = data[1]
                        break
        except FileNotFoundError:
            messagebox.showerror("Error", "User data not found")
            self.show_student_dashboard()
            return

        tk.Label(self.root, text="Username:").pack()
        tk.Label(self.root, text=self.username).pack(pady=5)

        tk.Label(self.root, text="Full Name:").pack()
        fullname_entry = tk.Entry(self.root)
        fullname_entry.insert(0, fullname)
        fullname_entry.pack(pady=5)

        tk.Label(self.root, text="New Password (Leave blank to keep current):").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack(pady=5)

        tk.Label(self.root, text="Confirm Password:").pack()
        confirm_entry = tk.Entry(self.root, show="*")
        confirm_entry.pack(pady=5)

        def update_account():
            new_fullname = fullname_entry.get().strip()
            new_password = password_entry.get().strip()
            confirm_password = confirm_entry.get().strip()

            if not new_fullname:
                messagebox.showerror("Error", "Full name cannot be empty")
                return

            if new_password and new_password != confirm_password:
                messagebox.showerror("Error", "Passwords don't match")
                return

            # update user details
            try:
                updated_user=[]
                with open("data/users.txt", "r") as file:
                    for line in file:
                        data = line.strip().split(",")
                        if data[0] == self.username:
                            updated_user.append(f"{self.username},{new_fullname},Student\n")
                        else:
                            updated_user.append(line)

                with open("data/users.txt", "w") as file:
                    file.writelines(updated_user)

                if new_password:
                    updated_passwords = []
                    with open("data/passwords.txt", "r") as file:
                        for line in file:
                            data = line.strip().split(",")
                            if data[0] == self.username:
                                updated_passwords.append(f"{self.username},{new_password}\n")
                            else:
                                updated_passwords.append(line)

                    with open("data/passwords.txt","w") as file:
                        file.writelines(updated_passwords)

                messagebox.showinfo("Success", "Account updated successfully")
                self.show_student_dashboard()
            
            except Exception as e:
                messagebox.showerror("Error", f"failed to update account: {str(e)}")

        tk.Button(self.root, text="Update Account", command=update_account).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_student_dashboard).pack(pady=5)

    def view_grades(self):

        messagebox.showinfo("View Grades", "This feature is devleoping.")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentDashboard(root)
    root.mainloop()