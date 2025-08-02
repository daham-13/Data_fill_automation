from ExcelReader import ExcelReader
from ExcelReaderFrontEnd import ExcelReaderFrontEnd

reader = ExcelReader("test data.xlsx")
reader.read_data()  
app = ExcelReaderFrontEnd(reader.raw_data)
app.root.mainloop() 
