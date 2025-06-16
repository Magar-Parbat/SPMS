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

        self.clear_window()
        self.root.geometry("800x600")

        tk.Label(self.root, text="Your Grades", font=("Arial", 14)).pack(pady=20)

        found = False # flag to check if marks found

        try:
            with open("data/marks.csv","r") as file:
                headers = file.readline().strip().split(",")
                subjects = headers[1:]

                for line in file:
                    data = line.strip().split(",")
                    if data[0] == self.username:
                        marks = [int(mark) if mark.isdigit() else 0 for mark in data [1:]]
                        found = True # marks found
                        break

            if not found:
                messagebox.showerror("Error", "No marks found")
                return

            # Create display frame
            report_frame = tk.Frame(self.root)
            report_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

            # Dispaly sutdent name
            tk.Label(report_frame, text=f"Student: {self.username}", font=("Arial", 12)).pack(anchor="center", pady=5)

            # Display each subject marks
            for subject, mark in zip(subjects, marks):
                tk.Label(report_frame, text=f" {subject}: {mark}/100", font=("Arial", 11)).pack(anchor="center", pady=5)
                    
            # Calcualte marks
            total = sum(marks)
            percentage = total / (len(marks) * 100) * 100

            # simpel gpa calculation 
            gpa = round((percentage / 100) * 4.0, 2)

            # grade calculation
            def get_grade(pct):
                if pct >= 90: return 'A+'
                elif pct >= 80: return 'A'
                elif pct >= 70: return 'B+'
                elif pct >= 60: return 'B'
                elif pct >= 50: return 'C+'
                elif pct >= 40: return 'C'
                elif pct >= 30: return 'D'
                else: return 'NG' 
            
            grade = get_grade(percentage)

            # Separator line
            tk.Frame(report_frame, height=5, bg="gray").pack(fill=tk.X, pady=10)

            # Dispaly calcuations
            tk.Label(report_frame, text=f"Total Marks: {total}", font=("Arial", 11)).pack(anchor="center", pady=5)
            tk.Label(report_frame, text=f"Percentage: {percentage:.2f}%", font=("Arial", 11)).pack(anchor="center", pady=5)
            tk.Label(report_frame, text=f"GPA: {gpa}", font=("Arial", 11)).pack(anchor="center", pady=5)
            tk.Label(report_frame, text=f"Grade: {grade}", font=("Arial", 11)).pack(anchor="center", pady=5)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

        tk.Button(self.root, text="Back to Dashboard", command=self.show_student_dashboard).pack(pady=20)




if __name__ == "__main__":
    root = tk.Tk()
    app = StudentDashboard(root)
    root.mainloop()