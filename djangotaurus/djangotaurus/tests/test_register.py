from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import os
from django.conf import settings

@override_settings(DEBUG=True)
@override_settings(STATICFILES_DIRS=(os.path.join(settings.BASE_DIR,'assets'),))
class Test_Register_User_Interface(StaticLiveServerTestCase):
    """
        Selenium Register Page User Interface Test
            - Accessing Register Page
            - Registering a form with invalid first name
            - Registering a form with invalid last name
            - Registering a form with invalid email
            - Registering a form with invalid password length
            - Registering a form with mismatch passwords
            - Registering a form with valid inputs but did not perform reCAPTCHA
            - Registering a form with valid inputs
    """

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.headless = True
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')  
        self.chrome = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.url = f"{self.live_server_url}/register"
        self.browser = self.chrome
        self.browser.implicitly_wait(10)
        self.browser.get(self.url)    

        # find the form elements
        self.browser.implicitly_wait(10)
        self.first_name = self.browser.find_element(By.ID, 'fn')
        self.last_name = self.browser.find_element(By.ID, 'ln')
        self.dob = self.browser.find_element(By.ID, 'dob')
        self.email = self.browser.find_element(By.ID, 'em')
        self.password = self.browser.find_element(By.ID, 'pw')
        self.confirm_password = self.browser.find_element(By.ID, 'cpw')

        super().setUp()

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

    def test_connection(self):
        """
            Accessing Register Page

            Upon accessing register page, browser title is 'Register'
        """
        assert 'Register' in self.browser.title

    def test_register_form_invalid_first_name(self):
        """
            Registering a form with invalid first name

            'btnRegister' will be disabled and not allow user to submit the form
            'fn' field will be highlighted in red
        """
        # populate form with data
        self.first_name.send_keys("SELECT * FROM Users WHERE user_id = 1 OR 1=1;")
        self.last_name.send_keys('Smith')
        self.dob.click()
        
        dob_day = '26'
        dob_month = 'July'
        dob_year = '1996'

        month = Select(self.browser.find_element(By.XPATH, "//div[@class='flatpickr-month']/div/select"))
        month.select_by_visible_text(dob_month)    
        year = self.browser.find_element(By.CLASS_NAME, 'numInput.cur-year')
        year.click()
        year.send_keys(dob_year)
        day = self.browser.find_element(By.XPATH, f"//span[contains(@class,'flatpickr-day') and contains(text(),{dob_day})]")
        day.click()

        self.email.send_keys('johnsmith@gmail.com')
        self.password.send_keys('johnsmithpassword')
        self.confirm_password.send_keys('johnsmithpassword')

        enabled = self.browser.find_element(By.ID, 'btnRegister').is_enabled()

        assert 'is-danger' in self.first_name.get_attribute("class")
        assert enabled is False
    
    def test_register_form_invalid_last_name(self):
        """
            Registering a form with invalid last name

            'btnRegister' will be disabled and not allow user to submit the form
            'ln' field will be highlighted in red
        """
        # populate form with data
        self.first_name.send_keys("John")
        self.last_name.send_keys('SELECT * FROM Users WHERE user_id = 1 OR 1=1;')
        self.dob.click()
        
        dob_day = '26'
        dob_month = 'July'
        dob_year = '1996'

        month = Select(self.browser.find_element(By.CLASS_NAME, 'flatpickr-monthDropdown-months'))
        month.select_by_visible_text(dob_month)    
        year = self.browser.find_element(By.CLASS_NAME, 'numInput.cur-year')
        year.click()
        year.send_keys(dob_year)
        day = self.browser.find_element(By.XPATH, f"//span[contains(@class,'flatpickr-day') and contains(text(),{dob_day})]")
        day.click()

        self.email.send_keys('johnsmith@gmail.com')
        self.password.send_keys('johnsmithpassword')
        self.confirm_password.send_keys('johnsmithpassword')

        enabled = self.browser.find_element(By.ID, 'btnRegister').is_enabled()

        assert 'is-danger' in self.last_name.get_attribute("class")
        assert enabled is False
    
    def test_register_form_invalid_email(self):
        """
            Registering a form with invalid email

            'btnRegister' will be disabled and not allow user to submit the form
            'em' field will be highlighted in red
        """
        # populate form with data
        self.first_name.send_keys("John")
        self.last_name.send_keys('Smith')
        self.dob.click()

        dob_day = '26'
        dob_month = 'July'
        dob_year = '1996'

        month = Select(self.browser.find_element(By.CLASS_NAME, 'flatpickr-monthDropdown-months'))
        month.select_by_visible_text(dob_month)    
        year = self.browser.find_element(By.CLASS_NAME, 'numInput.cur-year')
        year.click()
        year.send_keys(dob_year)
        day = self.browser.find_element(By.XPATH, f"//span[contains(@class,'flatpickr-day') and contains(text(),{dob_day})]")
        day.click()

        self.email.send_keys('SELECT * FROM Users WHERE user_id = 1 OR 1=1;')
        self.password.send_keys('johnsmithpassword')
        self.confirm_password.send_keys('johnsmithpassword')

        enabled = self.browser.find_element(By.ID, 'btnRegister').is_enabled()

        assert 'is-danger' in self.email.get_attribute("class")
        assert enabled is False
    
    def test_register_form_invalid_password_length(self):
        """
            Registering a form with password length < 10

            'btnRegister' will be disabled and not allow user to submit the form
            'pw' field will be highlighted in red
        """
        # populate form with data
        self.first_name.send_keys("John")
        self.last_name.send_keys('Smith')
        self.dob.click()
        
        dob_day = '26'
        dob_month = 'July'
        dob_year = '1996'

        month = Select(self.browser.find_element(By.CLASS_NAME, 'flatpickr-monthDropdown-months'))
        month.select_by_visible_text(dob_month)    
        year = self.browser.find_element(By.CLASS_NAME, 'numInput.cur-year')
        year.click()
        year.send_keys(dob_year)
        day = self.browser.find_element(By.XPATH, f"//span[contains(@class,'flatpickr-day') and contains(text(),{dob_day})]")
        day.click()

        self.email.send_keys('johnsmith@gmail.com')
        self.password.send_keys('123')
        self.confirm_password.send_keys('123')

        enabled = self.browser.find_element(By.ID, 'btnRegister').is_enabled()

        assert 'is-danger' in self.password.get_attribute("class")
        assert enabled is False

    def test_register_form_invalid_password_mismatch(self):
        """
            Registering a form with mismatch passwords

            'btnRegister' will be disabled and not allow user to submit the form
            'cpw' field will be highlighted in red
        """
        # populate form with data
        self.first_name.send_keys("Chicken")
        self.last_name.send_keys('Nugget')
        self.dob.click()
        
        dob_day = '26'
        dob_month = 'July'
        dob_year = '1996'

        month = Select(self.browser.find_element(By.CLASS_NAME, 'flatpickr-monthDropdown-months'))
        month.select_by_visible_text(dob_month)    
        year = self.browser.find_element(By.CLASS_NAME, 'numInput.cur-year')
        year.click()
        year.send_keys(dob_year)
        day = self.browser.find_element(By.XPATH, f"//span[contains(@class,'flatpickr-day') and contains(text(),{dob_day})]")
        day.click()

        self.email.send_keys('chickennugget@gmail.com')
        self.password.send_keys('ChickenNugget')
        self.confirm_password.send_keys('ChickenNugget@gmail')

        enabled = self.browser.find_element(By.ID, 'btnRegister').is_enabled()

        assert 'is-danger' in self.confirm_password.get_attribute("class")
        assert enabled is False

    def test_register_form_no_captcha(self):       
        """
            Registering a form with valid but without Captcha

            Browser popup will appear to prompt the user
        """
        # populate form with data
        self.first_name.send_keys("Chicken")
        self.last_name.send_keys('Nugget')
        self.dob.click()
        
        dob_day = '26'
        dob_month = 'July'
        dob_year = '1996'

        month = Select(self.browser.find_element(By.CLASS_NAME, 'flatpickr-monthDropdown-months'))
        month.select_by_visible_text(dob_month)    
        year = self.browser.find_element(By.CLASS_NAME, 'numInput.cur-year')
        year.click()
        year.send_keys(dob_year)
        day = self.browser.find_element(By.XPATH, f"//span[contains(@class,'flatpickr-day') and contains(text(),{dob_day})]")
        day.click()

        self.email.send_keys('chickennugget@gmail.com')
        self.password.send_keys('Rsk3GC7VurZeGVAu')
        self.confirm_password.send_keys('Rsk3GC7VurZeGVAu')

        time.sleep(1)

        register = self.browser.find_element(By.ID, 'btnRegister')
        register.click()

        time.sleep(1)

        alert = self.browser.switch_to.alert
        assert "Please complete the captcha" in alert.text

    
    def test_register_form_valid_form(self):       
        """
            Registering a form with valid inputs

            Browser will be redirected to 'Verify Email' page
        """
        # populate form with data
        self.first_name.send_keys("Chicken")
        self.last_name.send_keys('Nugget')
        self.dob.click()
        
        dob_day = '26'
        dob_month = 'July'
        dob_year = '1996'

        month = Select(self.browser.find_element(By.CLASS_NAME, 'flatpickr-monthDropdown-months'))
        month.select_by_visible_text(dob_month)    
        year = self.browser.find_element(By.CLASS_NAME, 'numInput.cur-year')
        year.click()
        year.send_keys(dob_year)
        day = self.browser.find_element(By.XPATH, f"//span[contains(@class,'flatpickr-day') and contains(text(),{dob_day})]")
        day.click()

        self.email.send_keys('chickennugget@gmail.com')
        self.password.send_keys('Rsk3GC7VurZeGVAu')
        self.confirm_password.send_keys('Rsk3GC7VurZeGVAu')

        captcha = self.browser.find_element(By.XPATH, '//*[@id="captcha"]/div/div/iframe')
        captcha.click()
        time.sleep(3)

        register = self.browser.find_element(By.ID, 'btnRegister')
        register.click()

        time.sleep(5)

        assert 'Verify Email' in self.browser.title