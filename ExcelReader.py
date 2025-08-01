import pandas as pd 

class ExcelReader:
    
    def __init__ (self, file_href):
        self.data_frame = pd.read_excel(file_href, header=None)
        self.raw_data = {
            "surname":"",
            "other_name":"",
            "dob":"",
            "P_num":"",
            "P_exp":"",
            "sex":"",
            "nationality":"",
            "email":"",
            "nic":"",
            "phone1":"",
            "phone2":"",
            "pob":"",
            "cob":"",
            "marital":"",
            "address":"",
            "d_name":"",
            "d_passport":"",
            "dnic":"",
        }
    
    def read_data(self):
        key_list = list(self.raw_data.keys())
        # Loop over each key and assign the first cell in the corresponding row to the raw_data dictionary
        for i, key in enumerate(key_list):
            if i < len(self.data_frame):
                self.raw_data[key] = self.data_frame.iloc[i, 0]
            else:
                self.raw_data[key] = ""
        print(self.raw_data)