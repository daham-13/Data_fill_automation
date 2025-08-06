Data Fill Automation

A desktop application that automatically fills web forms using data from Excel files. This solution streamlines repetitive form-filling tasks by reading Excel data and populating web forms automatically while maintaining user control over the process.

## 🚀 Features

- **Excel Integration**: Upload and read data from Excel files (.xlsx, .xls)
- **Web Form Automation**: Automatically populate web forms with Excel data
- **User-Friendly GUI**: Built with Tkinter for easy interaction
- **Flexible Data Mapping**: Convert Excel data to Python dictionaries for easy manipulation
- **Browser Control**: Opens and controls web browsers for form filling
- **Example Implementation**: Includes sample webpage (index.html) for testing

## 📁 Project Structure

```
Data_fill_automation/
├── Main.py                           # Main application entry point
├── ExcelReader.py                    # Excel file processing and data conversion
├── ExcelReaderFrontEnd.py           # Tkinter GUI implementation
├── ExcelReaderFrontEndController.py # Frontend controller and logic
├── index.html                       # Sample webpage for testing
└── README.md                        # Project documentation
```

## 🛠️ Components

### Core Files

- **`Main.py`**: Main application class and entry point
- **`ExcelReader.py`**: Handles Excel file reading and converts data to Python dictionaries
- **`ExcelReaderFrontEnd.py`**: Tkinter-based user interface for file selection and interaction
- **`ExcelReaderFrontEndController.py`**: Controller class managing frontend logic and user interactions
- **`index.html`**: Example webpage demonstrating form structure for testing

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Data_fill_automation.git
cd Data_fill_automation
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python Main.py
```

## 📋 Requirements

```
tkinter          # GUI framework (usually included with Python)
openpyxl         # Excel file handling
pandas           # Data manipulation
selenium         # Web browser automation
webdriver-manager # Automatic driver management
```

## 🎯 Usage

1. **Launch Application**: Run `python Main.py` to start the GUI
2. **Upload Excel File**: Use the interface to select and upload your Excel file
3. **Configure Mapping**: The application converts Excel data to a Python dictionary format
4. **Form Filling**: Navigate to your target webpage and let the automation fill the forms
5. **Monitor Process**: Watch the automated form filling process in real-time

## 💡 Use Cases

- **Visa Applications**: Automatically fill repetitive visa application forms
- **Job Applications**: Populate multiple job application forms with consistent data
- **Registration Forms**: Handle bulk registrations for events or services
- **Data Entry**: Streamline any repetitive web form data entry tasks

## 🏗️ Architecture

The application follows a Model-View-Controller (MVC) pattern:

- **Model**: `ExcelReader.py` handles data processing
- **View**: `ExcelReaderFrontEnd.py` manages the user interface
- **Controller**: `ExcelReaderFrontEndController.py` coordinates between model and view
- **Main**: `Main.py` orchestrates the entire application

## 🧪 Testing

Use the provided `index.html` file to test the form-filling functionality:

1. Open `index.html` in a web browser
2. Run the application with your Excel data
3. Observe the automated form filling process

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For questions, issues, or feature requests, please open an issue on GitHub.

---

**Note**: This application is designed for legitimate form-filling automation. Users are responsible for ensuring compliance with website terms of service and applicable regulations.
