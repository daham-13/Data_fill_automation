from ExcelReader import ExcelReader
from ExcelReaderFrontEnd import ExcelReaderFrontEnd

if __name__ == "__main__":
    # Create ExcelReader instance
    reader = ExcelReader()
    
    # Create frontend app with ExcelReader reference
    app = ExcelReaderFrontEnd(reader)
    
    # Start the application
    app.root.mainloop()