import tkinter as tk
from tkinter import messagebox, ttk

# Student Record Management System with GUI

class StudentRecordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Record Management System")
        self.root.geometry("800x600")
        
        # File to store student records
        self.FILENAME = "students.txt"
        
        # Create main container
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create widgets
        self.create_widgets()
        
        # Load initial data
        self.load_data()
    
    def create_widgets(self):
        # Title
        title_label = ttk.Label(
            self.main_frame, 
            text="Student Record Management System",
            font=('Helvetica', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=4, pady=10)
        
        # Buttons frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=1, column=0, columnspan=4, pady=10)
        
        # Buttons
        self.add_btn = ttk.Button(button_frame, text="Add Student", command=self.show_add_dialog)
        self.add_btn.pack(side=tk.LEFT, padx=5)
        
        self.search_btn = ttk.Button(button_frame, text="Search Student", command=self.show_search_dialog)
        self.search_btn.pack(side=tk.LEFT, padx=5)
        
        self.update_btn = ttk.Button(button_frame, text="Update Student", command=self.show_update_dialog)
        self.update_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_btn = ttk.Button(button_frame, text="Delete Student", command=self.show_delete_dialog)
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Treeview for displaying records
        self.tree = ttk.Treeview(
            self.main_frame, 
            columns=("Roll No", "Name", "Marks"), 
            show="headings",
            selectmode="browse"
        )
        
        # Configure columns
        self.tree.heading("Roll No", text="Roll No", anchor=tk.W)
        self.tree.heading("Name", text="Name", anchor=tk.W)
        self.tree.heading("Marks", text="Marks", anchor=tk.W)
        
        self.tree.column("Roll No", width=150, anchor=tk.W)
        self.tree.column("Name", width=250, anchor=tk.W)
        self.tree.column("Marks", width=150, anchor=tk.W)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=10)
        scrollbar.grid(row=2, column=3, sticky="ns")
        
        # Configure grid weights
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, columnspan=4, sticky="ew", pady=10)
    
    def load_data(self):
        # Clear current data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load from file
        try:
            with open(self.FILENAME, "r") as file:
                records = file.readlines()
                for record in records:
                    roll_no, name, marks = record.strip().split(",")
                    self.tree.insert("", tk.END, values=(roll_no, name, marks))
        except FileNotFoundError:
            pass  # File doesn't exist yet
    
    def show_add_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Student")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        # Form fields
        ttk.Label(dialog, text="Roll Number:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
        roll_no_entry = ttk.Entry(dialog)
        roll_no_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        
        ttk.Label(dialog, text="Name:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        name_entry = ttk.Entry(dialog)
        name_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        
        ttk.Label(dialog, text="Marks:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
        marks_entry = ttk.Entry(dialog)
        marks_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        def save():
            roll_no = roll_no_entry.get()
            name = name_entry.get()
            marks = marks_entry.get()
            
            if not roll_no or not name or not marks:
                messagebox.showerror("Error", "All fields are required!")
                return
            
            with open(self.FILENAME, "a") as file:
                file.write(f"{roll_no},{name},{marks}\n")
            
            self.load_data()
            self.status_var.set("Student record added successfully!")
            dialog.destroy()
        
        ttk.Button(button_frame, text="Save", command=save).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
        
        # Focus on first field
        roll_no_entry.focus_set()
    
    def show_search_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Search Student")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        
        ttk.Label(dialog, text="Enter Roll Number to Search:").pack(pady=20)
        
        roll_no_entry = ttk.Entry(dialog)
        roll_no_entry.pack(pady=10)
        
        result_label = ttk.Label(dialog, text="")
        result_label.pack(pady=10)
        
        def search():
            roll_no = roll_no_entry.get()
            if not roll_no:
                messagebox.showerror("Error", "Please enter a roll number!")
                return
            
            found = False
            try:
                with open(self.FILENAME, "r") as file:
                    for record in file:
                        r_no, name, marks = record.strip().split(",")
                        if r_no == roll_no:
                            result_label.config(text=f"Found: {name}, Marks: {marks}")
                            found = True
                            break
                
                if not found:
                    result_label.config(text="Student record not found.")
            except FileNotFoundError:
                result_label.config(text="No records found.")
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Search", command=search).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Close", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
        
        roll_no_entry.focus_set()
    
    def show_update_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a student to update!")
            return
        
        # Get selected record
        item = self.tree.item(selected[0])
        roll_no, name, marks = item['values']
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Student Record")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        # Form fields with current values
        ttk.Label(dialog, text="Roll Number:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
        roll_no_label = ttk.Label(dialog, text=roll_no)
        roll_no_label.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        
        ttk.Label(dialog, text="Name:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        name_entry = ttk.Entry(dialog)
        name_entry.insert(0, name)
        name_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        
        ttk.Label(dialog, text="Marks:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
        marks_entry = ttk.Entry(dialog)
        marks_entry.insert(0, marks)
        marks_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
        
        def update():
            new_name = name_entry.get()
            new_marks = marks_entry.get()
            
            if not new_name or not new_marks:
                messagebox.showerror("Error", "All fields are required!")
                return
            
            # Read all records
            try:
                with open(self.FILENAME, "r") as file:
                    records = file.readlines()
                
                # Write back all records with updated one
                with open(self.FILENAME, "w") as file:
                    for record in records:
                        r_no, n, m = record.strip().split(",")
                        if r_no == roll_no:
                            file.write(f"{roll_no},{new_name},{new_marks}\n")
                        else:
                            file.write(record)
                
                self.load_data()
                self.status_var.set("Student record updated successfully!")
                dialog.destroy()
            except FileNotFoundError:
                messagebox.showerror("Error", "No records found!")
                dialog.destroy()
        
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Update", command=update).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
        
        name_entry.focus_set()
    
    def show_delete_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a student to delete!")
            return
        
        # Get selected record
        item = self.tree.item(selected[0])
        roll_no, name, marks = item['values']
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm", f"Delete record for {name} (Roll No: {roll_no})?"):
            return
        
        # Read all records except the one to delete
        try:
            with open(self.FILENAME, "r") as file:
                records = file.readlines()
            
            with open(self.FILENAME, "w") as file:
                for record in records:
                    r_no, n, m = record.strip().split(",")
                    if r_no != roll_no:
                        file.write(record)
            
            self.load_data()
            self.status_var.set("Student record deleted successfully!")
        except FileNotFoundError:
            messagebox.showerror("Error", "No records found!")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentRecordApp(root)
    root.mainloop()
