from tkinter import messagebox, filedialog
from BrowserAutomation import BrowserAutomation

class ExcelReaderFrontEndController:
    def __init__(self, excel_reader, frontend_app):
        self.excel_reader = excel_reader  # Reference to ExcelReader instance
        self.frontend_app = frontend_app  # Reference to frontend app
        
    @property
    def raw_data(self):
        return self.excel_reader.raw_data
    
    @property
    def editing(self):
        return self.frontend_app.editing
    
    @property
    def root(self):
        return self.frontend_app.root
    
    @property
    def entries(self):
        return self.frontend_app.entries

    def clear_button_clicked(self):
        """Handle clear button click - clears all form fields"""
        if self.editing:
            messagebox.showwarning(
                "⚠️ Warning",
                "Please save or cancel your current edits before clearing the form.",
                parent=self.root
            )
            return

        # Confirm before clearing
        result = messagebox.askyesno(
            "🗑️ Clear All Fields",
            "Are you sure you want to clear all fields?\n\nThis action cannot be undone.",
            parent=self.root
        )
        
        if result:
            # Clear raw_data in ExcelReader
            for key in self.raw_data:
                self.raw_data[key] = ""

            self.update_ui_with_data()
            
            messagebox.showinfo(
                "✅ Cleared",
                "All fields have been cleared successfully!",
                parent=self.root
            )

            print(self.raw_data)

    def select_file_button_clicked(self):
        """Handle select file button click - opens file picker and loads data"""
        if self.editing:
            messagebox.showwarning(
                "⚠️ Warning",
                "Please save or cancel your current edits before selecting a new file.",
                parent=self.root
            )
            return

        # Open file dialog
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ],
            parent=self.root
        )
        
        if file_path:
            print(f"Selected file: {file_path}")
            
            # Try to load the file using ExcelReader
            success = self.excel_reader.select_file(file_path)
            
            if success:
                # Update the UI with new data
                self.update_ui_with_data()
                
                messagebox.showinfo(
                    "✅ File Loaded",
                    f"File loaded successfully:\n\n{file_path}\n\nData has been populated in the form.",
                    parent=self.root
                )
            else:
                messagebox.showerror(
                    "❌ Error",
                    f"Failed to load file:\n\n{file_path}\n\nPlease check if the file is valid and try again.",
                    parent=self.root
                )

    def update_ui_with_data(self):
        """Update the UI fields with data from ExcelReader"""
        self.frontend_app.set_fields_state(editable=True)
        for key, entry in self.entries.items():
            value = self.raw_data.get(key, "")

            # For a custom date selector widget
            if hasattr(entry, 'date_entry'):  
                # Make sure date_entry is a widget supporting delete/insert
                entry.date_entry.delete(0, "end")
                if value:
                    entry.date_entry.insert(0, str(value))
            
            # For a ComboBox widget
            elif hasattr(entry, 'set'):  
                if value:
                    entry.set(str(value))
                else:
                    # Set default values for dropdowns
                    if key == "sex":
                        entry.set("M")
                    elif key == "marital":
                        entry.set("Single")
                    else:
                        entry.set("")  # Clear if no default
            
            # For a regular Entry widget
            else:  
                entry.delete(0, "end")
                if value:
                    entry.insert(0, str(value))
                else:
                    entry.insert(0, "")  # Clear the entry
        
        self.frontend_app.set_fields_state(editable=False)


    def proceed_button_clicked(self):
        if self.editing:
            messagebox.showerror(
                    "❌ Error",
                    f"Unable to Proceed in Editing Mode Please Save the data and proceed",
                    parent=self.root
                )
        else:
            automation = BrowserAutomation()
            print("Proceed button clicked")
            print("Current data:", self.raw_data)
            
            # Show current data in a message box
            data_summary = "\n".join([f"{key}: {value}" for key, value in self.raw_data.items() if value])
            
            if data_summary:
                messagebox.showinfo(
                    "📋 Current Data",
                    f"Data ready for processing:\n\n{data_summary}",
                    parent=self.root
                )
                data = self.raw_data
                automation.execute_full_flow(data)
            else:
                messagebox.showwarning(
                    "⚠️ No Data",
                    "No data available to process. Please load a file or enter data manually.",
                    parent=self.root
                )

    def save_changes(self):
        """Save changes from UI back to ExcelReader"""
        for key, entry in self.entries.items():
            if hasattr(entry, 'date_entry'):  # Custom date selector
                self.raw_data[key] = entry.date_entry.get()
            else:
                self.raw_data[key] = entry.get()
        
        print("Updated data:", self.raw_data)
        
        # Modern success message
        messagebox.showinfo(
            "✅ Success",
            "Your changes have been saved successfully!\n\nData updated and ready to use.",
            parent=self.root
        )

    def toggle_edit(self):
        if not self.editing:
            self.frontend_app.set_fields_state(editable=True)
            self.frontend_app.action_btn.configure(
                text="💾 Save Changes",
                fg_color=self.frontend_app.colors['success'],
                hover_color='#45a049'
            )
            self.frontend_app.status_label.configure(
                text="✏️ Edit mode - Make your changes",
                text_color=self.frontend_app.colors['success']
            )
            self.frontend_app.editing = True
        else:
            self.save_changes()
            self.frontend_app.set_fields_state(editable=False)
            self.frontend_app.action_btn.configure(
                text="✏️ Edit Data",
                fg_color=self.frontend_app.colors['accent'],
                hover_color=self.frontend_app.colors['primary']
            )
            self.frontend_app.status_label.configure(
                text="🔒 Read-only mode",
                text_color=self.frontend_app.colors['text_secondary']
            )
            self.frontend_app.editing = False