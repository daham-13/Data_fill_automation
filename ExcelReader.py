import pandas as pd

class ExcelReader:
    def __init__(self):
        self.raw_data = {
            "surname": "",
            "other_name": "",
            "dob": "",
            "P_num": "",
            "P_exp": "",
            "sex": "",
            "nationality": "",
            "email": "",
            "nic": "",
            "phone1": "",
            "phone2": "",
            "pob": "",
            "cob": "",
            "marital": "",
            "address": "",
            "d_name": "",
            "d_passport": "",
            "dnic": "",
        }
        self.data_frame = None

    def select_file(self, file_path):
        try:
            self.data_frame = pd.read_excel(file_path, header=None)
            self.read_data()
            return True
        except Exception as e:
            print(f"Error reading file: {e}")
            return False

    def read_data(self):
        key_list = list(self.raw_data.keys())
        # Loop over each key and assign the first cell in the corresponding row to the raw_data dictionary
        for i, key in enumerate(key_list):
            if i < len(self.data_frame):
                cell_value = self.data_frame.iloc[i, 0]
                # Handle NaN values
                if pd.isna(cell_value):
                    self.raw_data[key] = ""
                else:
                    self.raw_data[key] = str(cell_value)
            else:
                self.raw_data[key] = ""
        print("Data loaded:", self.raw_data)