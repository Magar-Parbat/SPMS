import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
        tk.Button(self.root, text="View Statistics", command=self.view_statistics).pack(pady=10)

        tk.Button(self.root, text="Back", command=self.return_to_dashboard).pack(pady=10)

    def view_courses(self):

        self.clear_window()
        self.root.geometry("1000x600")

        tk.Label(self.root, text="View Courses", font=("Arial", 14)).pack(pady=10)

        # Columns for the treeview
        columns = [
            "Rank",
            "Username",
            "Maths",
            "Physics",
            "Chemistry",
            "English",
            "Nepali",
            "Total",
            "Percentage",
            "GPA",
            "Grade",
        ]

        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=20)

        # Configure column widths
        col_widths = {
            "Rank": 50,
            "Username": 100,
            "Maths": 70,
            "Physics": 70,
            "Chemistry": 70,
            "English": 70,
            "Nepali": 70,
            "Total": 70,
            "Percentage": 70,
            "GPA": 50,
            "Grade": 50
        }

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths.get(col, 100), anchor="center")

        # Load and process marks data
        marks_data = self.load_existing_marks()
        processed_data = []

        for username, subjects in marks_data.items():
            # Calculate total marks
            total = 0
            valid_subjects = 0
            subject_scores = {}

            for subject in ["Maths", "Physics", "Chemistry", "English", "Nepali"]:
                try:
                    score = float(subjects.get(subject, 0))
                    total += score
                    valid_subjects += 1
                    subject_scores[subject] = score
                except (ValueError, TypeError):
                    subject_scores[subject] = "N/A"

            # Calculate percentage
            percentage = (total/ (valid_subjects * 100)) * 100 if valid_subjects > 0 else 0

            # calculate GPA
            gpa = round((percentage / 100) * 4.0, 2)

            # Determine grades
            grade = self.calculate_grade(percentage)

            processed_data.append({
                "Username": username,
                "Maths": subject_scores.get("Maths", "N/A"),
                "Physics": subject_scores.get("Physics", "N/A"),
                "Chemistry": subject_scores.get("Chemistry", "N/A"),
                "English": subject_scores.get("English", "N/A"),
                "Nepali": subject_scores.get("Nepali", "N/A"),
                "Total": round(total, 2),
                "Percentage": round(percentage, 2),
                "GPA": gpa,
                "Grade": grade
            })

        # sort by percentage for ranks
        processed_data.sort(key=lambda x: x["Percentage"], reverse=True)
        for i, student in enumerate(processed_data, 1):
            student["Rank"] = i 

        # Add data to Treeview
        for student in processed_data:
            self.tree.insert("", tk.END, values=[
                student["Rank"],
                student["Username"],
                student["Maths"],
                student["Physics"],
                student["Chemistry"],
                student["English"],
                student["Nepali"],
                student["Total"],
                f"{student['Percentage']}%",
                student["GPA"],
                student["Grade"]
            ])
        
        # Add scrollbar


        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Button(self.root, text="Back", command=self.show_course_dashboard).pack(pady=10)

    
    def calculate_grade(self, percentage):
        if percentage >= 90:return "A+"
        elif percentage >= 80:return "A"
        elif percentage >= 70:return "B+"
        elif percentage >= 60:return "B"
        elif percentage >= 50:return "C+"
        elif percentage >= 40:return "C"
        elif percentage >= 30:return "D"
        else: return "F"


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
            messagebox.showerror("Error", f"Failed to save marks: {str(e)}")

    def view_statistics(self):
        self.clear_window()
        self.root.geometry("1000x800")
        
        tk.Label(self.root, text="Performance Statistics", font=("Arial", 14)).pack(pady=10)
        
        # Load and process the data
        marks_data = self.load_existing_marks()
        if not marks_data:
            messagebox.showinfo("Info", "No marks data available to display statistics")
            self.show_course_dashboard()
            return
        
        # Convert to DataFrame
        df = pd.DataFrame.from_dict(marks_data, orient='index')
        
        # Convert marks to numeric (ignore non-numeric values)
        subjects = ["Maths", "Physics", "Chemistry", "English", "Nepali"]
        for subject in subjects:
            df[subject] = pd.to_numeric(df[subject], errors='coerce')
        
        # Calculate additional metrics
        df['Total'] = df[subjects].sum(axis=1)
        df['Percentage'] = (df['Total'] / (len(subjects) * 100)) * 100
        df['Grade'] = df['Percentage'].apply(self.calculate_grade)
        
        # Create a frame for the plots
        plot_frame = tk.Frame(self.root)
        plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a notebook for multiple tabs
        notebook = ttk.Notebook(plot_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 1. Subject-wise Average Marks
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Subject Averages")
        
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        subject_means = df[subjects].mean()  # This returns a Series
        subject_means.plot(kind='bar', ax=ax1, color='skyblue')
        ax1.set_title('Average Marks per Subject')
        ax1.set_ylabel('Marks')
        ax1.set_ylim(0, 100)
        
        canvas1 = FigureCanvasTkAgg(fig1, master=tab1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 2. Grade Distribution
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Grade Distribution")
        
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        grade_counts = df['Grade'].value_counts()
        # Sort grades in a meaningful order (A+, A, B+, etc.)
        grade_order = ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'F']
        grade_counts = grade_counts.reindex(grade_order, fill_value=0)
        grade_counts.plot(kind='bar', ax=ax2, color='lightgreen')
        ax2.set_title('Grade Distribution')
        ax2.set_xlabel('Grade')
        ax2.set_ylabel('Number of Students')
        
        canvas2 = FigureCanvasTkAgg(fig2, master=tab2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 3. Subject Comparison (Boxplot)
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="Subject Comparison")
        
        fig3, ax3 = plt.subplots(figsize=(8, 5))
        df[subjects].boxplot(ax=ax3)
        ax3.set_title('Subject-wise Marks Distribution')
        ax3.set_ylabel('Marks')
        ax3.set_ylim(0, 100)
        
        canvas3 = FigureCanvasTkAgg(fig3, master=tab3)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 4. Top Performers
        tab4 = ttk.Frame(notebook)
        notebook.add(tab4, text="Top Performers")
        
        top_students = df.nlargest(5, 'Percentage')
        fig4, ax4 = plt.subplots(figsize=(8, 5))
        top_students.plot(x='Username', y='Percentage', kind='bar', ax=ax4, color='gold')
        ax4.set_title('Top 5 Students by Percentage')
        ax4.set_ylabel('Percentage')
        ax4.set_ylim(0, 100)
        
        canvas4 = FigureCanvasTkAgg(fig4, master=tab4)
        canvas4.draw()
        canvas4.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Back button
        tk.Button(self.root, text="Back", command=self.show_course_dashboard).pack(pady=10)
            
def show_course_screen(root, return_to_dashboard):
    CourseManager(root, return_to_dashboard)
