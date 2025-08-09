from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import threading

class BrowserAutomation:
    def __init__(self):
        self.driver = None
        self.main_window = None
        self.booking_window = None
        # Update this to the actual VFS legalization page
        self.target_url = ""
        self.booking_url = ""
        self.automation_paused = False

    def setup_browser(self):
        chromedriver_path = 'C:/Program Files/Google/chromedriver-win64/chromedriver.exe'
        service = Service(chromedriver_path)
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        # Don't use headless mode - user needs to interact with OTP
        try:
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("✅ Chrome browser initialized successfully!")
            return True
        except Exception as e:
            print(f"❌ Error initializing browser: {e}")
            return False

    
    def handle_cookies_and_popups(self):
        """Handle OneTrust cookie banner - click 'Accept All Cookies'."""
        try:
            print("🍪 Waiting for cookie banner...")

            # Wait up to 10 seconds for the accept button to be present and clickable
            accept_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )

            self.driver.execute_script("arguments[0].click();", accept_button)
            print("✅ Accepted all cookies")
            return True

        except Exception as e:
            print(f"ℹ️ No cookie banner found or already dismissed: {e}")
            return True

    def open_legalization_page(self):
        """Open the main legalization page"""
        if not self.driver:
            print("Browser not initialized. Call setup_browser() first.")
            return False
        try:
            print(f"Opening legalization page: {self.target_url}")
            self.driver.get(self.target_url)
            self.main_window = self.driver.current_window_handle
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Handle cookies immediately after page load
            self.handle_cookies_and_popups()
            
            print("✅ Legalization page opened successfully!")
            return True
        except Exception as e:
            print(f"❌ Error opening legalization page: {e}")
            return False

    def click_book_now(self):
        """Click the 'Book now' button"""
        try:
            print("🔍 Looking for 'Book now' button...")
            
            # Handle any remaining popups before clicking
            self.handle_cookies_and_popups()
            
            # Wait for and click the "Book now" button
            book_now_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "lets-get-started"))
            )
            
            print("✅ Found 'Book now' button, clicking...")
            
            # Scroll to button to ensure it's visible
            self.driver.execute_script("arguments[0].scrollIntoView(true);", book_now_button)
            time.sleep(1)
            
            # Click using JavaScript to avoid interception
            self.driver.execute_script("arguments[0].click();", book_now_button)
            
            # Handle the new tab that opens
            time.sleep(3)  # Wait for new tab to open
            
            # Switch to the new booking tab
            all_windows = self.driver.window_handles
            for window in all_windows:
                if window != self.main_window:
                    self.booking_window = window
                    self.driver.switch_to.window(window)
                    break
            
            # Handle cookies on the new page too
            time.sleep(2)
            self.handle_cookies_and_popups()
            
            print("✅ Switched to booking page tab")
            return True
            
        except Exception as e:
            print(f"❌ Error clicking 'Book now' button: {e}")
            return False

    def wait_for_otp_completion(self):
        """Wait for user to complete email/OTP verification"""
        print("\n" + "="*60)
        print("🔄 MANUAL INTERVENTION REQUIRED")
        print("="*60)
        print("Please complete the following steps manually:")
        print("1. Enter your email address")
        print("2. Complete OTP verification")
        print("3. Handle any page reloads if server is busy")
        print("4. Navigate to the actual form page")
        print("\n⚠️  The automation will automatically resume when it detects the form page!")
        print("="*60)
        
        # Monitor for form page in a separate thread
        self.automation_paused = True
        monitor_thread = threading.Thread(target=self._monitor_for_form_page)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # Wait for user input or automatic detection
        while self.automation_paused:
            time.sleep(2)
            # Check if user wants to manually signal completion
            try:
                # Non-blocking input check (you might want to implement this differently)
                pass
            except:
                pass
        
        print("✅ Form page detected! Resuming automation...")
        return True

    def _monitor_for_form_page(self):
        """Monitor for form page appearance (runs in background thread)"""
        while self.automation_paused:
            try:
                # Handle cookies on any new pages
                self.handle_cookies_and_popups()
                
                # Check for form indicators - update these selectors based on your form page
                form_indicators = [
                    (By.NAME, "surname"),  # From your original code
                    (By.NAME, "user_type"),  # From your original code
                    (By.TAG_NAME, "form"),
                    (By.CSS_SELECTOR, "input[type='text']"),
                ]
                
                for by_method, selector in form_indicators:
                    try:
                        element = self.driver.find_element(by_method, selector)
                        if element and element.is_displayed():
                            print(f"✅ Form detected using selector: {selector}")
                            self.automation_paused = False
                            return
                    except:
                        continue
                        
                time.sleep(3)  # Check every 3 seconds
                
            except Exception as e:
                # Browser might be closed or page changed
                time.sleep(5)
                continue

    def handle_first_form(self):
        """Handle the first form: select 'i am an agency' and '1' applicant"""
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
            print("✅ Main form appeared successfully!")
            time.sleep(1)  # Small delay for form to fully load
            return True
            
        except Exception as e:
            print(f"❌ Error handling first form: {e}")
            return False

    def insert_data(self, data):
        """Fill the main form with data from Excel"""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            
            print("🔄 Filling form with data...")
            filled_count = 0
            
            for field_name, value in data.items():
                if value == '' or value == []:
                    continue
                    
                try:
                    if field_name in ['sex', 'marital']:
                        select_element = Select(self.driver.find_element(By.NAME, field_name))
                        select_element.select_by_value(value)
                        print(f"✅ Filled dropdown {field_name}: {value}")
                    elif field_name in ['dob', 'P_exp']:
                        date = ((value.split(" "))[0]).split('-')
                        act_date = ""
                        for i in reversed(date):
                            act_date = act_date + i + "/"
                        act_date = act_date.strip("/")
                        input_element = self.driver.find_element(By.NAME, field_name)
                        input_element.send_keys(act_date)
                        print(f"✅ Filled date {field_name}: {act_date}")
                    else:
                        input_element = self.driver.find_element(By.NAME, field_name)
                        input_element.clear()
                        input_element.send_keys(value)
                        print(f"✅ Filled text {field_name}: {value}")
                    
                    filled_count += 1
                    time.sleep(0.5)  # Small delay between fields
                    
                except Exception as field_error:
                    print(f"⚠️  Could not fill {field_name}: {field_error}")
                    continue
            
            print(f"✅ Successfully filled {filled_count} fields!")
            print("📝 Form filling completed (form NOT submitted automatically)")
            return True
            
        except Exception as e:
            print(f"❌ Error filling the form: {e}")
            return False

    def smart_retry_mechanism(self, max_retries=5):
        """Handle page reloads and server busy situations"""
        for attempt in range(max_retries):
            try:
                # Check if page is responsive
                self.driver.find_element(By.TAG_NAME, "body")
                return True
            except:
                print(f"🔄 Attempt {attempt + 1}: Page not responsive, refreshing...")
                self.driver.refresh()
                time.sleep(3)
        
        print("❌ Page still not responsive after retries")
        return False

    def close_browser(self):
        """Close the browser when done"""
        if self.driver:
            self.driver.quit()
            print("🔒 Browser closed.")

    def execute_full_flow(self, data):
        """Execute the complete visa automation flow"""
        print("🚀 Starting Visa Automation Flow...")
        print("=" * 50)
        
        # Step 1: Setup browser
        if not self.setup_browser():
            return False
        
        # Step 2: Open legalization page
        if not self.open_legalization_page():
            self.close_browser()
            return False
        
        # Step 3: Click "Book now" button
        if not self.click_book_now():
            self.close_browser()
            return False
        
        # Step 4: Wait for human to complete OTP
        if not self.wait_for_otp_completion():
            self.close_browser()
            return False
        
        # Step 5: Handle first form (if it appears)
        try:
            if self.handle_first_form():
                # Step 6: Fill main form
                self.insert_data(data)
            else:
                # Maybe we're already at the main form
                print("ℹ️  No first form found, attempting to fill main form directly...")
                self.insert_data(data)
        except Exception as e:
            print(f"⚠️  Form handling error: {e}")
        
        # Step 7: Keep browser open for final review
        print("\n" + "="*60)
        print("✅ AUTOMATION COMPLETED!")
        print("🔍 Please review the filled form before submitting")
        print("📝 The form has NOT been automatically submitted")
        print("▶️  Submit manually when ready")
        print("="*60)
        print("Press Enter when you want to close the browser...")
        input()
        
        self.close_browser()
        return True

    def manual_continue_option(self):
        """Provide manual override for OTP completion"""
        print("\n🆘 MANUAL OVERRIDE AVAILABLE")
        print("If you've completed OTP and reached the form page,")
        print("press 'c' + Enter to continue automation: ")
        
        while True:
            user_input = input().strip().lower()
            if user_input == 'c':
                self.automation_paused = False
                break
            elif user_input == 'q':
                print("❌ Automation cancelled by user")
                return False
        return True

