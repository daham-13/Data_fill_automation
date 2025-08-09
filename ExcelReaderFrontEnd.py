import customtkinter as ctk
import calendar
from datetime import datetime
from ExcelReaderFrontEndController import ExcelReaderFrontEndController

ctk.set_appearance_mode("Dark")  # Modern dark theme
ctk.set_default_color_theme("blue")


class ExcelReaderFrontEnd:
    def __init__(self, excel_reader):
        self.excel_reader = excel_reader  # Store reference to ExcelReader
        
        self.root = ctk.CTk()
        self.root.title("Excel Data Editor")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Modern color scheme
        self.colors = {
            'primary': '#1f538d',
            'secondary': '#14375e',
            'accent': '#36719f',
            'surface': '#212121',
            'surface_variant': '#2d2d2d',
            'text_primary': '#ffffff',
            'text_secondary': '#b3b3b3',
            'success': '#4caf50',
            'warning': '#ff9800',
            'danger': '#f44336'
        }

        self.label_names = [
            "Surname", "Other Name", "Date of birth", "Passport Number", "Passport Expiry",
            "Gender", "Nationality", "Email", "NIC", "Phone 1", "Phone 2",
            "Place of Birth", "Country of Birth", "Marital", "Address",
            "Delegate Name", "Delegate Passport", "Delegate NIC"
        ]

        self.entries = {}
        self.editing = False
        self.date_popup = None
        
        self.controller = ExcelReaderFrontEndController(self.excel_reader, self)

        self.create_widgets()
        self.set_fields_state(editable=False)
        self.bind_mouse_wheel()

    @property
    def raw_data(self):
        """Get raw_data from ExcelReader"""
        return self.excel_reader.raw_data

    def create_date_selector(self, parent, initial_value):
        """Create a modern date selector that handles empty values"""
        container = ctk.CTkFrame(parent, fg_color=self.colors['surface'], corner_radius=10)
        
        # Parse initial date - handle empty/None values
        if initial_value and initial_value.strip():
            try:
                if isinstance(initial_value, str):
                    date_obj = datetime.strptime(initial_value, "%Y-%m-%d")
                else:
                    date_obj = initial_value if initial_value else datetime.now()
            except:
                date_obj = datetime.now()
            date_display = date_obj.strftime("%Y-%m-%d")
        else:
            # Empty value - show placeholder
            date_obj = datetime.now()
            date_display = ""
        
        # Date display entry
        date_entry = ctk.CTkEntry(
            container,
            font=ctk.CTkFont(family="Arial", size=13),
            corner_radius=8,
            border_width=0,
            height=35,
            placeholder_text="YYYY-MM-DD"
        )
        if date_display:
            date_entry.insert(0, date_display)
        date_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        
        # Calendar button
        cal_button = ctk.CTkButton(
            container,
            text="📅",
            width=40,
            height=35,
            corner_radius=8,
            fg_color=self.colors['accent'],
            hover_color=self.colors['primary'],
            command=lambda: self.show_date_picker(date_entry)
        )
        cal_button.pack(side="right", padx=(5, 10), pady=10)
        
        # Store both widgets for state management
        container.date_entry = date_entry
        container.cal_button = cal_button
        
        return container

    def show_date_picker(self, target_entry):
        """Show modern date picker popup with proper sizing"""
        if self.date_popup:
            self.date_popup.destroy()
            
        # Parse current date
        try:
            current_date = datetime.strptime(target_entry.get(), "%Y-%m-%d")
        except:
            current_date = datetime.now()
            
        # Create popup window with larger size
        self.date_popup = ctk.CTkToplevel(self.root)
        self.date_popup.title("Select Date")
        self.date_popup.geometry("380x480")  # Increased from 320x400
        self.date_popup.resizable(False, False)
        
        # Center the popup relative to parent
        self.date_popup.transient(self.root)
        
        # Update window to ensure it's displayed
        self.date_popup.update_idletasks()
        
        # Center the window with new dimensions
        x = (self.root.winfo_x() + (self.root.winfo_width() // 2)) - (380 // 2)
        y = (self.root.winfo_y() + (self.root.winfo_height() // 2)) - (480 // 2)
        self.date_popup.geometry(f"380x480+{x}+{y}")
        
        # Current year and month
        self.current_year = current_date.year
        self.current_month = current_date.month
        self.selected_day = current_date.day
        
        # Header frame with increased height
        header_frame = ctk.CTkFrame(self.date_popup, fg_color=self.colors['primary'], height=90)
        header_frame.pack(fill="x", padx=15, pady=15)
        header_frame.pack_propagate(False)
        
        # Year navigation row
        year_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        year_frame.pack(fill="x", pady=(8, 0))
        
        prev_year_btn = ctk.CTkButton(
            year_frame, text="<<", width=40, height=28,
            fg_color=self.colors['secondary'], hover_color=self.colors['accent'],
            font=ctk.CTkFont(family="Arial", size=11),
            command=self.prev_year
        )
        prev_year_btn.pack(side="left", padx=(15, 8))
        
        self.year_label = ctk.CTkLabel(
            year_frame,
            text=str(self.current_year),
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            text_color="white"
        )
        self.year_label.pack(side="left", expand=True)
        
        next_year_btn = ctk.CTkButton(
            year_frame, text=">>", width=40, height=28,
            fg_color=self.colors['secondary'], hover_color=self.colors['accent'],
            font=ctk.CTkFont(family="Arial", size=11),
            command=self.next_year
        )
        next_year_btn.pack(side="right", padx=(8, 15))
        
        # Month navigation row
        month_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        month_frame.pack(fill="x", pady=(8, 8))
        
        prev_btn = ctk.CTkButton(
            month_frame, text="◀", width=40, height=32,
            fg_color=self.colors['secondary'], hover_color=self.colors['accent'],
            font=ctk.CTkFont(family="Arial", size=12),
            command=self.prev_month
        )
        prev_btn.pack(side="left", padx=(15, 8))
        
        self.month_label = ctk.CTkLabel(
            month_frame,
            text=calendar.month_name[self.current_month],
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color="white"
        )
        self.month_label.pack(side="left", expand=True)
        
        next_btn = ctk.CTkButton(
            month_frame, text="▶", width=40, height=32,
            fg_color=self.colors['secondary'], hover_color=self.colors['accent'],
            font=ctk.CTkFont(family="Arial", size=12),
            command=self.next_month
        )
        next_btn.pack(side="right", padx=(8, 15))
        
        # Calendar grid container with more space
        self.calendar_frame = ctk.CTkFrame(self.date_popup, fg_color=self.colors['surface_variant'])
        self.calendar_frame.pack(fill="both", expand=True, padx=15, pady=8)
        
        # Configure grid columns
        for i in range(7):
            self.calendar_frame.grid_columnconfigure(i, weight=1, uniform="col")
        
        # Day headers with larger size
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days):
            label = ctk.CTkLabel(
                self.calendar_frame, text=day,
                font=ctk.CTkFont(family="Arial", size=13, weight="bold"),
                text_color=self.colors['text_primary'],
                width=45, height=35
            )
            label.grid(row=0, column=i, padx=3, pady=3, sticky="nsew")
        
        self.day_buttons = []
        self.target_entry = target_entry
        self.update_calendar()
        
        # Action buttons with more space
        action_frame = ctk.CTkFrame(self.date_popup, fg_color="transparent", height=60)
        action_frame.pack(fill="x", padx=15, pady=15)
        action_frame.pack_propagate(False)
        
        cancel_btn = ctk.CTkButton(
            action_frame, text="Cancel", width=90, height=35,
            fg_color=self.colors['surface_variant'], hover_color=self.colors['surface'],
            font=ctk.CTkFont(family="Arial", size=12),
            command=self.close_date_picker
        )
        cancel_btn.pack(side="left", padx=8)
        
        today_btn = ctk.CTkButton(
            action_frame, text="Today", width=90, height=35,
            fg_color=self.colors['accent'], hover_color=self.colors['primary'],
            font=ctk.CTkFont(family="Arial", size=12),
            command=self.select_today
        )
        today_btn.pack(side="left", padx=8)
        
        ok_btn = ctk.CTkButton(
            action_frame, text="OK", width=90, height=35,
            fg_color=self.colors['success'], hover_color='#45a049',
            font=ctk.CTkFont(family="Arial", size=12),
            command=self.confirm_date
        )
        ok_btn.pack(side="right", padx=8)
        
        # Now grab focus after everything is set up
        self.date_popup.after(100, self.grab_focus)

    def update_calendar(self):
        """Update calendar display with proper button sizing"""
        # Clear existing buttons
        for btn in self.day_buttons:
            btn.destroy()
        self.day_buttons.clear()
        
        # Get calendar for current month
        cal = calendar.monthcalendar(self.current_year, self.current_month)
        
        # Get currently selected date for highlighting
        try:
            current_selected = datetime.strptime(self.target_entry.get(), "%Y-%m-%d")
            is_same_month = (self.current_month == current_selected.month and 
                        self.current_year == current_selected.year)
        except:
            is_same_month = False
            current_selected = None
        
        for week_num, week in enumerate(cal, 1):
            for day_num, day in enumerate(week):
                if day == 0:
                    # Empty cell
                    label = ctk.CTkLabel(
                        self.calendar_frame, 
                        text="", 
                        width=45, 
                        height=40,
                        fg_color="transparent"
                    )
                    label.grid(row=week_num, column=day_num, padx=3, pady=3, sticky="nsew")
                    self.day_buttons.append(label)
                else:
                    # Day button with larger size
                    is_selected = (is_same_month and current_selected and day == current_selected.day)
                    
                    btn = ctk.CTkButton(
                        self.calendar_frame, 
                        text=str(day), 
                        width=45, 
                        height=40,
                        font=ctk.CTkFont(family="Arial", size=13),
                        fg_color=self.colors['primary'] if is_selected else self.colors['surface'],
                        hover_color=self.colors['accent'],
                        text_color="white",
                        command=lambda d=day: self.select_day(d)
                    )
                    btn.grid(row=week_num, column=day_num, padx=3, pady=3, sticky="nsew")
                    self.day_buttons.append(btn)
        
        # Configure grid rows
        for i in range(len(cal) + 1):
            self.calendar_frame.grid_rowconfigure(i, weight=1)

    def grab_focus(self):
        """Safely grab focus after window is displayed"""
        try:
            if self.date_popup and self.date_popup.winfo_exists():
                self.date_popup.grab_set()
                self.date_popup.focus_set()
        except:
            pass  # Ignore if grab fails

    def close_date_picker(self):
        """Close the date picker safely"""
        if self.date_popup:
            try:
                self.date_popup.grab_release()
            except:
                pass
            self.date_popup.destroy()
            self.date_popup = None

    def prev_month(self):
        """Navigate to previous month"""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
            self.year_label.configure(text=str(self.current_year))
        else:
            self.current_month -= 1
        self.month_label.configure(text=calendar.month_name[self.current_month])
        self.update_calendar()

    def next_month(self):
        """Navigate to next month"""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
            self.year_label.configure(text=str(self.current_year))
        else:
            self.current_month += 1
        self.month_label.configure(text=calendar.month_name[self.current_month])
        self.update_calendar()

    def prev_year(self):
        """Navigate to previous year"""
        self.current_year -= 1
        self.year_label.configure(text=str(self.current_year))
        self.update_calendar()

    def next_year(self):
        """Navigate to next year"""
        self.current_year += 1
        self.year_label.configure(text=str(self.current_year))
        self.update_calendar()

    def select_day(self, day):
        """Select a specific day"""
        self.selected_day = day
        self.update_calendar()

    def select_today(self):
        """Select today's date"""
        today = datetime.now()
        self.current_year = today.year
        self.current_month = today.month
        self.selected_day = today.day
        self.year_label.configure(text=str(self.current_year))
        self.month_label.configure(text=calendar.month_name[self.current_month])
        self.update_calendar()

    def confirm_date(self):
        """Confirm date selection"""
        selected_date = datetime(self.current_year, self.current_month, self.selected_day)
        self.target_entry.delete(0, "end")
        self.target_entry.insert(0, selected_date.strftime("%Y-%m-%d"))
        self.close_date_picker()

    def create_widgets(self):
        # Main container
        main_container = ctk.CTkFrame(self.root, fg_color=self.colors['surface'], corner_radius=0)
        main_container.pack(fill="both", expand=True)

        # Top navigation bar
        nav_frame = ctk.CTkFrame(main_container, fg_color=self.colors['surface_variant'], height=60, corner_radius=0)
        nav_frame.pack(fill="x", padx=0, pady=0)
        nav_frame.pack_propagate(False)

        # Clear button (left side)
        self.clear_btn = ctk.CTkButton(
            nav_frame,
            text="🗑️ Clear",
            command=self.controller.clear_button_clicked,
            corner_radius=8,
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            width=120,
            height=40,
            fg_color=self.colors['danger'],
            hover_color='#d32f2f'
        )
        self.clear_btn.pack(side="left", padx=20, pady=10)

        # Select File button (center)
        self.select_file_btn = ctk.CTkButton(
            nav_frame,
            text="📁 Select File",
            command=self.controller.select_file_button_clicked,
            corner_radius=8,
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            width=140,
            height=40,
            fg_color=self.colors['accent'],
            hover_color=self.colors['primary']
        )
        self.select_file_btn.pack(side="left", padx=10, pady=10)

        # Proceed button (right side)
        self.proceed_btn = ctk.CTkButton(
            nav_frame,
            text="Proceed ➤",
            command=self.controller.proceed_button_clicked,
            corner_radius=8,
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            width=120,
            height=40,
            fg_color=self.colors['success'],
            hover_color='#45a049'
        )
        self.proceed_btn.pack(side="right", padx=20, pady=10)

        # Content area with modern card design
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Scrollable frame with modern styling
        self.frame = ctk.CTkScrollableFrame(
            content_frame,
            fg_color=self.colors['surface_variant'],
            corner_radius=15,
            scrollbar_button_color=self.colors['accent'],
            scrollbar_button_hover_color=self.colors['primary']
        )
        self.frame.pack(fill="both", expand=True)

        # Configure grid with better spacing
        self.frame.grid_columnconfigure(0, weight=0, minsize=200)
        self.frame.grid_columnconfigure(1, weight=1)

        date_fields = ["dob", "P_exp"]
        sex_field = "sex"
        marital_field = "marital"

        # Get the keys and values from raw_data, ensuring we have all expected fields
        field_keys = list(self.raw_data.keys())
        
        for idx, key in enumerate(field_keys):
            value = self.raw_data[key]
            label_text = self.label_names[idx] if idx < len(self.label_names) else key

            # Modern label styling with icons
            icon_map = {
                "Surname": "👤", "Other Name": "📝", "Date of birth": "📅", 
                "Passport Number": "🛂", "Passport Expiry": "⏰", "Gender": "⚧",
                "Nationality": "🌍", "Email": "📧", "NIC": "🆔", 
                "Phone 1": "📱", "Phone 2": "☎️", "Place of Birth": "📍",
                "Country of Birth": "🌐", "Marital": "💍", "Address": "🏠",
                "Delegate Name": "👥", "Delegate Passport": "🛂", "Delegate NIC": "🆔"
            }
            
            icon = icon_map.get(label_text, "📋")
            
            label = ctk.CTkLabel(
                self.frame, 
                text=f"{icon} {label_text}",
                font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
                text_color=self.colors['text_primary']
            )
            label.grid(row=idx, column=0, padx=(25, 20), pady=15, sticky="w")

            if key in date_fields:
                # Modern date selector - handle empty dates
                initial_date = value if value else ""
                entry = self.create_date_selector(self.frame, initial_date)
                entry.grid(row=idx, column=1, pady=15, padx=(0, 25), sticky="ew")
                
            elif key == sex_field:
                entry = ctk.CTkComboBox(
                    self.frame, 
                    values=["M", "F"],
                    font=ctk.CTkFont(family="Arial", size=13),
                    dropdown_font=ctk.CTkFont(family="Arial", size=12),
                    corner_radius=10,
                    border_width=0,
                    button_color=self.colors['accent'],
                    button_hover_color=self.colors['primary']
                )
                # Set default value or empty
                if value and value in ["M", "F"]:
                    entry.set(value)
                else:
                    entry.set("M")  # Default to M if empty
                entry.grid(row=idx, column=1, pady=15, padx=(0, 25), sticky="ew")
                
            elif key == marital_field:
                entry = ctk.CTkComboBox(
                    self.frame, 
                    values=["Married", "Single"],
                    font=ctk.CTkFont(family="Arial", size=13),
                    dropdown_font=ctk.CTkFont(family="Arial", size=12),
                    corner_radius=10,
                    border_width=0,
                    button_color=self.colors['accent'],
                    button_hover_color=self.colors['primary']
                )
                # Set default value or empty
                if value and value in ["Married", "Single"]:
                    entry.set(value)
                else:
                    entry.set("Single")  # Default to Single if empty
                entry.grid(row=idx, column=1, pady=15, padx=(0, 25), sticky="ew")
                
            else:
                entry = ctk.CTkEntry(
                    self.frame,
                    font=ctk.CTkFont(family="Arial", size=13),
                    corner_radius=10,
                    border_width=0,
                    height=40
                )
                # Insert value or leave empty
                if value:
                    entry.insert(0, str(value))
                entry.grid(row=idx, column=1, pady=15, padx=(0, 25), sticky="ew")

            self.entries[key] = entry

        # Modern action button with hover effects
        button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        button_frame.grid(row=len(field_keys), column=0, columnspan=2, pady=30)
        
        self.action_btn = ctk.CTkButton(
            button_frame,
            text="✏️ Edit Data",
            command=self.controller.toggle_edit,
            corner_radius=25,
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            width=200,
            height=50,
            fg_color=self.colors['accent'],
            hover_color=self.colors['primary'],
            border_width=2,
            border_color=self.colors['primary']
        )
        self.action_btn.pack()

        # Status indicator
        self.status_label = ctk.CTkLabel(
            button_frame,
            text="🔒 Read-only mode",
            font=ctk.CTkFont(family="Arial", size=12),
            text_color=self.colors['text_secondary']
        )
        self.status_label.pack(pady=(10, 0))

    def bind_mouse_wheel(self):
        """Bind mouse wheel events to enable scrolling"""
        def _on_mousewheel(event):
            self.frame._parent_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(widget):
            widget.bind("<MouseWheel>", _on_mousewheel)
            widget.bind("<Button-4>", lambda e: self.frame._parent_canvas.yview_scroll(-1, "units"))
            widget.bind("<Button-5>", lambda e: self.frame._parent_canvas.yview_scroll(1, "units"))
        
        # Bind to root and frame
        _bind_to_mousewheel(self.root)
        _bind_to_mousewheel(self.frame)
        
        # Bind to all entry widgets
        for entry in self.entries.values():
            _bind_to_mousewheel(entry)

    def set_fields_state(self, editable):
        for key, entry in self.entries.items():
            if hasattr(entry, 'date_entry'):  # Custom date selector
                entry.date_entry.configure(state="normal" if editable else "disabled")
                entry.cal_button.configure(state="normal" if editable else "disabled")
            else:
                entry.configure(state="normal" if editable else "disabled")