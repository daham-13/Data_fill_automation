from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class BrowserAutomation:
    def __init__(self):
        self.driver = None
        self.target_url = "http://127.0.0.1:5500/index.html"

    def setup_browser(self):
        chromedriver_path = '/usr/bin/chromedriver'
        service = Service(chromedriver_path)
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        try:
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("✅ Chrome browser initialized successfully!")
            return True
        except Exception as e:
            print(f"❌ Error initializing browser: {e}")
            return False

    def open_webpage(self):
        if not self.driver:
            print("Browser not initialized. Call setup_browser() first.")
            return False
        try:
            print(f"Opening webpage: {self.target_url}")
            self.driver.get(self.target_url)
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("Webpage opened successfully!")
            return True
        except Exception as e:
            print(f"Error opening webpage: {e}")
            return False

    def handle_first_form(self):
        """
        Handle the first form: select 'i am an agency' and '1' applicant
        """
        try:
            print("🔍 Looking for first form...")
            
            # Wait for the first form to be present
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "user_type"))
            )
            
            # Select "i am an agency"
            user_type_dropdown = Select(self.driver.find_element(By.NAME, "user_type"))
            user_type_dropdown.select_by_value("i am an agency")
            print("✅ Selected: I am an agency")
            
            # Select "1" applicant
            num_applicants_dropdown = Select(self.driver.find_element(By.NAME, "num_applicants"))
            num_applicants_dropdown.select_by_value("1")
            print("✅ Selected: 1 applicant")
            
            # Click the proceed button
            proceed_button = self.driver.find_element(By.CSS_SELECTOR, "button[onclick='proceedToMainForm()']")
            proceed_button.click()
            print("✅ Clicked proceed button")
            
            # Wait for the second form to appear
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "surname"))
            )
            print("✅ Second form appeared successfully!")
            time.sleep(1)  # Small delay for form to fully load
            return True
            
        except Exception as e:
            print(f"❌ Error handling first form: {e}")
            return False

    def close_browser(self):
        """
        Close the browser when done
        """
        if self.driver:
            self.driver.quit()
            print("Browser closed.")

    def insert_data(self, data):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            for field_name, value in data.items():
                if field_name in ['sex', 'marital']:
                    select_element = Select(self.driver.find_element(By.NAME, field_name))
                    select_element.select_by_value(value)
                elif field_name in ['dob', 'P_exp']:
                    date = ((value.split(" "))[0]).split('-')
                    act_date = ""
                    for i in reversed(date):
                        act_date = act_date + i + "/"
                    act_date = act_date.strip("/")
                    print(date)
                    print(act_date)
                    input_element = self.driver.find_element(By.NAME, field_name)
                    input_element.send_keys(act_date)
                else:
                    input_element = self.driver.find_element(By.NAME, field_name)
                    input_element.clear()
                    input_element.send_keys(value)
            print("All fields filled with dummy data (form NOT submitted).")
        except Exception as e:
            print(f"Error filling the form: {e}")

    def execute(self, data):
        if self.setup_browser():
            if self.open_webpage():
                # NEW: Handle the first form first
                if self.handle_first_form():
                    # Then proceed with the original form filling
                    self.insert_data(data)
                    print("Press Enter when you want to close the browser...")
                    input()
                else:
                    print("❌ Failed to handle first form, stopping execution")
                self.close_browser()
