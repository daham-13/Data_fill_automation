from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime

class BrowserAutomation:
    def __init__(self,raw_data):
        self.driver = None
        self.timeout = 300  # 5 minutes timeout
        self.start_time = None
        self.initial_tab = None
        self.form_tab = None
        self.raw_data = raw_data 

    def setup_browser(self):
        """Initialize Chrome browser and open the initial website"""
        chromedriver_path = 'C:/Program Files/Google/chromedriver-win64/chromedriver.exe'
        service = Service(chromedriver_path)
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--start-maximized")
        
        try:
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Open the initial website
            print("🌐 Opening initial website: https://visa.vfsglobal.com/lka/en/ita/Legalisation")
            self.driver.get("http://127.0.0.1:5500/Webpages/Legalization%20Services%20_%20vfsglobal.html")
            self.initial_tab = self.driver.current_window_handle
            
            # Wait for the page to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            print("✅ Initial page loaded successfully!")
            return True
        except Exception as e:
            print(f"❌ Error initializing browser: {e}")
            return False

    def wait_for_form_tab(self, target_url_pattern="http://127.0.0.1:5500/Webpages/page2.html"):
        start_time = time.time()
        processed_tabs = {self.initial_tab}  
        
        while time.time() - start_time < self.timeout:
            current_handles = set(self.driver.window_handles)
            
            new_tabs = current_handles - processed_tabs
            
            if new_tabs:
                for handle in new_tabs:
                    print(f"\n✅ NEW TAB DETECTED! Checking...")
                    
                    self.driver.switch_to.window(handle)
                    current_url = self.driver.current_url
                    print(f"📍 Tab URL: {current_url}")
                    
                    is_target = False
                    if target_url_pattern:
                        is_target = target_url_pattern in current_url
                    else:
                        is_target = "form" in current_url.lower() or "application" in current_url.lower()
                    
                    if is_target:
                        print(f"🎯 TARGET FORM TAB FOUND! URL: {current_url}")
                        self.form_tab = handle
                        return True
                    else:
                        print(f"❌ Not the target tab, continuing to monitor...")
                    
                    processed_tabs.add(handle)
                    
                    self.driver.switch_to.window(self.initial_tab)
            
            elapsed = int(time.time() - start_time)
            if elapsed % 15 == 0 and elapsed > 0:
                print(f"⌛ Still waiting for target form tab... ({elapsed}s elapsed)")
                
            time.sleep(1)
        
        print(f"❌ Timed out after {self.timeout} seconds waiting for form tab")
        return False

    def wait_for_detailed_form(self):
        if not self.form_tab:
            print("❌ No form tab available to monitor")
            return False
            
        self.start_time = time.time()
        print("⏳ Continuously monitoring for detailed form appearance...")
        print("🔄 No timeout - will keep checking until form appears")
        
        check_count = 0
        
        while True:  # Infinite loop - no timeout
            check_count += 1
            
            try:
                # Show progress every 30 seconds
                elapsed = time.time() - self.start_time
                if check_count % 30 == 0:  # Every 30 iterations (roughly 30 seconds if sleep is 1s)
                    print(f"⌛ Still monitoring... ({elapsed:.1f}s elapsed, check #{check_count})")
                
                # First, try to find the divApplicants container
                try:
                    # Use a very short timeout since we're in a loop
                    applicants_container = WebDriverWait(self.driver, 2).until(
                        EC.visibility_of_element_located((By.ID, "divApplicants"))
                    )
                    
                    if check_count <= 3 or check_count % 20 == 0:  # Reduce spam
                        print("✅ Found divApplicants container")
                    
                    # Check if it's visible and has content
                    if applicants_container.is_displayed():
                        if check_count <= 3 or check_count % 20 == 0:
                            print("✅ divApplicants is visible")
                        
                        content = applicants_container.get_attribute('innerHTML').strip()
                        if len(content) > 100:
                            print("✅ divApplicants has substantial content - checking fields...")
                            
                            # Now check for specific fields
                            required_fields = {
                                "txtFirstName1": "First Name field",
                                "txtLastName1": "Last Name field", 
                                "txtPassportNo1": "Passport Number field",
                                "txtContactNo1": "Primary Phone field",
                                "txtSecondaryPhone1": "Secondary Phone field",
                                "txtAddress1": "Address field"
                            }
                            
                            fields_found = 0
                            for field_id, field_name in required_fields.items():
                                try:
                                    element = self.driver.find_element(By.ID, field_id)
                                    if element.is_displayed():
                                        fields_found += 1
                                        print(f"✅ Found {field_name} (ID: {field_id})")
                                    else:
                                        print(f"⚠️ {field_name} exists but not visible")
                                except:
                                    print(f"❌ Could not find {field_name} (ID: {field_id})")
                            
                            # If we found most/all fields, consider form ready
                            if fields_found >= len(required_fields) * 0.8:  # 80% of fields found
                                elapsed = time.time() - self.start_time
                                print("\n" + "="*60)
                                print(f"✅✅✅ FORM APPEARED AFTER {elapsed:.1f} SECONDS!")
                                print(f"✅✅✅ Found {fields_found}/{len(required_fields)} required fields")
                                print("✅✅✅ Automation will now fill the form.")
                                print("="*60)
                                return True
                            else:
                                print(f"⚠️ Only found {fields_found}/{len(required_fields)} fields, continuing to wait...")
                        else:
                            if check_count <= 3 or check_count % 30 == 0:
                                print("⚠️ divApplicants content still insufficient, waiting...")
                    else:
                        if check_count <= 3 or check_count % 30 == 0:
                            print("⚠️ divApplicants not visible yet, waiting...")
                            
                except Exception as e:
                    if check_count <= 3:
                        print(f"⚠️ divApplicants not ready yet: {str(e)[:50]}...")
                    # Don't return False, just continue checking
                
                # Brief pause before next check
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n⚠️ Monitoring interrupted by user")
                return False
            except Exception as e:
                print(f"⚠️ Unexpected error during monitoring: {e}")
                print("🔄 Continuing to monitor...")
                time.sleep(2)  # Slightly longer pause on errors
                
        # This line should never be reached due to infinite loop
        return False

    def debug_current_page(self):
        """Debug information about current page state"""
        try:
            print("\n" + "="*60)
            print("🛠️ CURRENT PAGE DEBUG INFORMATION")
            print("="*60)
            
            # Basic page info
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page title: {self.driver.title}")
            print(f"Window handles: {len(self.driver.window_handles)}")
            
            print("="*60 + "\n")
            
        except Exception as debug_e:
            print(f"⚠️ Debug failed: {debug_e}")

    def fill_applicant_form(self, applicant_data):
        """Fill the detailed applicant form with provided data"""
        print("\n📝 Filling applicant form...")
        
        # Define field mappings
        text_fields = {
            "txtFirstName1": "surname",
            "txtLastName1": "other_name", 
            "txtPassportNo1": "P_num",
            "txtEmail1": "email",
            "txtContactNo1": "phone1",
            "txtSecondaryPhone1": "phone2",
            "txtNationalId1": "nic",
            "txtBirthPlace1": "pob",
            "txtAddress1": "address"
        }
        
        d_text_fields = {
            "txtDelegateName1": "d_name",
            "txtDelegatePassNo1": "d_passport",
            "txtDelegateNatId1": "dnic"
        }

        try:
            # Fill text fields
            print("📝 Filling text fields...")
            for field_id, data_key in text_fields.items():
                try:
                    if data_key in applicant_data and applicant_data[data_key]:
                        element = self.driver.find_element(By.ID, field_id)
                        element.clear()  # Clear existing content
                        element.send_keys(applicant_data[data_key])
                        print(f"✅ Filled {field_id}: {applicant_data[data_key]}")
                    else:
                        print(f"⚠️ No data for {field_id} (key: {data_key})")
                except Exception as e:
                    print(f"❌ Failed to fill {field_id}: {str(e)[:50]}")
            
            Select(self.driver.find_element(By.ID, "ddlNationality1")).select_by_value("200")
            Select(self.driver.find_element(By.ID, "ddlBirthCountry1")).select_by_value("200")

            if applicant_data["sex"].lower() == "m":
                Select(self.driver.find_element(By.ID, "ddlGender1")).select_by_value("Male")
            elif applicant_data["sex"].lower() == "f":
                Select(self.driver.find_element(By.ID, "ddlGender1")).select_by_value("Female")
            else:
                Select(self.driver.find_element(By.ID, "ddlGender1")).select_by_value("0")

            if applicant_data["marital"].lower() == "m":
                Select(self.driver.find_element(By.ID, "ddlMaritalSts1")).select_by_value("2")
            elif applicant_data["marital"].lower() == "s":
                Select(self.driver.find_element(By.ID, "ddlMaritalSts1")).select_by_value("1")
            else:
                Select(self.driver.find_element(By.ID, "ddlMaritalSts1")).select_by_value("0")

            if applicant_data["d_name"] != "":
                Select(self.driver.find_element(By.ID, "ddlDelegate1")).select_by_value("2") 
                time.sleep(0.7)
                for field_id, data_key in d_text_fields.items():
                    try:
                        if data_key in applicant_data and applicant_data[data_key]:
                            element = self.driver.find_element(By.ID, field_id)
                            element.clear()
                            element.send_keys(applicant_data[data_key])
                            print(f"✅ Filled {field_id}: {applicant_data[data_key]}")
                        else:
                            print(f"⚠️ No data for {field_id} (key: {data_key})")
                    except Exception as e:
                        print(f"❌ Failed to fill {field_id}: {str(e)[:50]}")               
            else:
                Select(self.driver.find_element(By.ID, "ddlDelegate1")).select_by_value("1")
                        
        except Exception as e:
            print(f"❌ Error filling form: {e}")
            self.debug_current_page()
            return False

    def run(self):
        """Main workflow to fill the form"""
        print("🚀 Starting VFS Form Filler...")
        
        try:
            if not self.setup_browser():
                return False
                
            # Wait for form tab to be opened by user
            if not self.wait_for_form_tab():
                return False
                
            # Now wait for the detailed form to appear
            if self.wait_for_detailed_form():
                return self.fill_applicant_form(self.raw_data)
            return False
            
        except Exception as e:
            print(f"\n❌ Automation failed: {str(e)}")
            return False
        finally:
            input("\nPress Enter to close browser...")
            self.close_browser()

    def close_browser(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("🔄 Browser closed")
