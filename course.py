import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk 
import os

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

        tk.Label(self.root, text="Course Dashboard", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="View Course", command=self.view_course).pack(pady=10)
        tk.Button(self.root, text="Edit Course", command=self.edit_course).pack(pady=10)

        tk.Button(self.root, text="Back", command=self.return_to_dashboard).pack(pady=10)

    def view_course(self):

        messagebox.showinfo("View Course", "This feature is under development.")
    
    def edit_course(self):

        self.clear_window()
        self.root.geometry("800x600")
        tk.Label(self.root, text="Edit Course", font=("Arial", 14)).pack(pady=10)

        students = []

        with open("data/users.txt", "r") as file:
            for line in file:
                data = line.strip().aplit(",")
                if len(data) == 3 and data[2] == "Student":
                    students.append(data[0])

        # Create a treeview to editable cells

        columns = ["Username", "Physics", "Chemistry", "Maths", "English", "Nepali"]
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)

        # set headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        # load existing marks if availabel
        marks_data = self.load_existing_marks()

        # Add Students to the treeview
        for student in students:
            if student in marks_data:
                values = [
                    student,
                    marks_data[student].get("Physics", ""), 
                    marks_data[student].get("Chemistry", ""),
                    marks_data[student].get("Maths", ""),
                    marks_data[student].get("English", ""),
                    marks_data[student].get("Nepali", "")
                ]
            else:
                values = [student] = [""] * 5 # empty values for new students

            self.tree.insert("", tk.END, vlues = values) 
        
        # Pack the treeview
        self.tree.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

        # save button
        tk.Button(self.root, text="Save", command=self.save_marks_to_csv).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_course_dashboard).pack(pady=10)

        # Bind double-check to edit cells
        self.tree.bind("<Double-1>", self.on_double_click)

    def load_existing_marks(self):
        
        marks_data = {}
        try:
            if not os.path.exists("data/marks.csv"):
                return marks_data
            
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

            # Get cell position and value:
            col_index = int(column[1:]) - 1
            x, y, width, height = self.tree.bbox(item, column)
            abs_x = self.tree.winfo_rootx() + x - self.root.winfo_rootx()
            abs_y = self.tree.winfo_rooty() + y - self.root.winfo_rooty()
            current_value = self.tree.item(item, "values")[col_index]

            # create entry widget
            entry = tk.Entry(self.root)
            entry.place(x=abs_x, y=abs_y, width=width, height=height)
            entry.insert(0, current_value)
            entry.focus_set()
            
    

        

        

        

            
                

        
            



        

