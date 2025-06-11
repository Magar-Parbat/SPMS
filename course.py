import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 
import os
import csv

class CourseManager:
    def __init__(self, root, return_to_dashboard):
        self.root = root
        self.return_to_dashboard = return_to_dashboard
        self.show_course_dashboard()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_course_dashboard(self):
        self.clear_window()
        self.root.geometry("600x400")

        tk.Label(self.root, text="Manage Courses", font=("Arial", 14)).pack(pady=20)
        tk.Button(self.root, text="View Courses", command=self.view_courses).pack(pady=10)
        tk.Button(self.root, text="Edit Courses", command=self.edit_courses).pack(pady=10)

        tk.Button(self.root, text="Back", command=self.return_to_dashboard).pack(pady=10)

    def view_courses(self):

        messagebox.showinfo("View Courses", "This feature is under development")

    def edit_courses(self):

        self.clear_window()
        self.root.geometry("800x600")

        tk.Label(self.root, text="Edit Course", font=("Arial", 14)).pack(pady=20)

        students = [] # Initialize an empty list to store student marks_data

        with open("data/users.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) == 3 and data[2] == "Student":
                    students.append(data[0]) # adding username form data list ot students list

        # Create the treeview with editable cells 

        columns = ["Username", "Maths", "Physics", "Chemistry", "English", "Nepali"]
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)

        # set headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        # load exiting marks if available
        marks_data = self.load_existing_marks()

        # Add student to the table:
        for student in students:
            if student in marks_data:
                values = [
                    student, 
                    marks_data[student].get("Maths", ""),
                    marks_data[student].get("Physics", ""),
                    marks_data[student].get("Chemistry", ""),
                    marks_data[student].get("English", ""),
                    marks_data[student].get("Nepali", "")
                ]
            else:
                values = [student] + [""] * 5 # empty marks for new student

            self.tree.insert("", tk.END, values=values)
        
        # pack the treeview
        self.tree.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

        # Save Button
        tk.Button(self.root, text="Save", command=self.save_marks_to_csv).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_course_dashboard).pack(pady=10)

        # Bind double-check ot edit cells
        self.tree.bind("<Double-1>", self.on_double_click)
        # <Double-1> = Double left-click event.
        # self.on_double_click = Function that runs when double-clicked.

    def load_existing_marks(self):
        marks_data = {} # creating empty dict 

        try:
            if not os.path.exists("data/marks.csv"):
                return marks_data # If there’s no CSV file, stop and return an empty dictionary.

            with open("data/marks.csv", mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    marks_data[row["Username"]] = row
        
        except Exception as e:
            messagebox.showerror("Error", f"Error reading marks: {str(e)}")

        return marks_data

    def on_double_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)

            # don't allow editing username column
            if column == "#1":
                return

            # Get cell position and values:
            col_index = int(column[1]) -1
            x, y, width, height = self.tree.bbox(item, column)
            abs_x = self.tree.winfo_rootx() + x - self.root.winfo_rootx()
            abs_y = self.tree.winfo_rooty() + y - self.root.winfo_rooty()
            current_value = self.tree.item(item, "values")[col_index]

            # create entry widget
            entry = tk.Entry(self.root)
            entry.place(x=abs_x, y=abs_y, width=width, height=height)
            entry.insert(0, current_value)
            entry.focus_set()

            def save_edit():
                new_value = entry.get()

                # Allow empty value or validate if it's number between 0 and 100
                if new_value: # Only validate if there's actually a values
                    try:
                        value = float(entry.get()) # Convert to float first
                        if value < 0 or value > 100:
                            raise ValueError
                    except ValueError:
                        messagebox.showerror("Error", "Please enter a number between 0 and 100")
                        entry.destroy()
                        return

                values = list(self.tree.item(item, "values"))
                values[col_index] = entry.get()
                self.tree.item(item, values=values)
                entry.destroy()

            entry.bind("<FocusOut>", lambda e: save_edit())
            entry.bind("<Return>", lambda e: save_edit())
    
    def save_marks_to_csv(self):
        fieldnames = ["Username", "Maths", "Physics", "Chemistry", "English", "Nepali"]

        # Prepare data for csv
        data = []
        for child in self.tree.get_children():
            values = self.tree.item(child, "values")
            row = {
                'Username': values[0], 
                'Maths': values[1], 
                'Physics': values[2],
                'Chemistry': values[3],
                'English': values[4],
                'Nepali': values[5]
            }
            data.append(row)

        # save to csv file
        try:
            # Create data directory if it doesn't exists
            os.makedirs("data", exist_ok=True)

            with open("data/marks.csv", mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            messagebox.showinfo("Success", "Marks saved successfully to marks.csv!")
        
        except Exception as e:
            messagebox.showerror("Errr", f"Failed to save marks: {str(e)}")

        

def show_course_screen(root, return_to_dashboard):
    CourseManager(root, return_to_dashboard)
