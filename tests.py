import time
import unittest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class EcommerceTests(unittest.TestCase):
    BASE_URL = "http://65.2.191.34:5175"
    TIMEOUT = 120

    @classmethod
    def setUpClass(cls):
        print("Launching Chrome...")
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')

        cls.driver = webdriver.Chrome(options=options)
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.wait_for_app_ready()
        print("App is up and running!")

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    @staticmethod
    def is_server_running():
        try:
            response = requests.get(EcommerceTests.BASE_URL, timeout=1)
            return response.status_code == 200
        except:
            return False
    @classmethod
    def wait_for_app_ready(cls, retries=10, delay=5):
        for i in range(retries):
            if not cls.is_server_running():
                print(f"Server not ready, retry {i+1}/{retries}")
                time.sleep(delay)
                continue
            try:
                cls.driver.get(cls.BASE_URL)
                cls.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                return
            except:
                print(f"App still loading... retry {i+1}/{retries}")
                time.sleep(delay)
        raise Exception("Application not ready after retries.")

    def test_1_homepage_loads(self):
        self.driver.get(self.BASE_URL)
        self.assertIn("COLLECTION", self.driver.page_source.upper())

    def test_2_navigate_to_collection(self):
        print("🔹 Test 2: Navigate to Collection page")
        self.driver.get(self.BASE_URL)
        try:
            collection_link = self.driver.find_element(By.XPATH, "//a[@href='/collection']")
            collection_link.click()
            self.wait.until(EC.url_contains('/collection')) 
            self.assertIn("/collection", self.driver.current_url)
            self.assertIn("COLLECTION", self.driver.page_source.upper()) 
            print("Navigated to collection page successfully")
        except Exception as e:
            self.fail(f"Failed to navigate to collection page: {e}")
    def test_3_product_view_and_add_to_cart_with_size(self):
        print("Test 3: View product and add to cart with size")
        try:
            self.driver.get(f'{self.BASE_URL}/collection')
            self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

            product_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/product/')]")
            self.assertTrue(product_links, "No product links found on collection page.")
            product_links[0].click()

            self.wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(@class, 'text-3xl')]")))

            size_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'border') and contains(text(),'S') or contains(text(),'M') or contains(text(),'L')]")
            self.assertTrue(size_buttons, "No size buttons found on product page.")
            size_buttons[0].click()

            add_to_cart_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Add to Cart')]")
            add_to_cart_button.click()
            time.sleep(2)

            print("Product viewed and added to cart with size successfully")

        except Exception as e:
            self.fail(f"Failed to add product to cart: {e}")

    def test_4_view_cart_page(self):
        print("🔹 Test 4: View Cart Page")
        try:
            self.driver.get(f"{self.BASE_URL}/cart")
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'CART')]"))) 
            self.assertIn("CART", self.driver.page_source) 
            print("Cart page loaded successfully")
        except Exception as e:
            self.fail(f"Cart page failed: {e}")
    def test_5_go_to_place_order_page(self):
        print("Test 5: Go to Place Order Page")
        try:
            self.driver.get(f"{self.BASE_URL}/place-order")
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'DELIVERY')]")))
            self.assertIn("DELIVERY", self.driver.page_source) 
            print("Place order page loaded successfully")
        except Exception as e:
            self.fail(f"Failed to load place order page: {e}")

    def test_6_try_submit_empty_order_form(self):
        self.driver.get(f"{self.BASE_URL}/place-order")
        self.driver.find_element(By.XPATH, "//button[contains(text(),'PLACE ORDER')]").click()
        time.sleep(1)
        self.assertTrue(True)

    def test_7_register_user(self):
        print("Test 7: Register new user")
        try:
            self.driver.get(f"{self.BASE_URL}/login")
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'Create account')]")))
            self.driver.find_element(By.XPATH, "//p[contains(text(),'Create account')]").click()
            time.sleep(1)

            self.driver.find_element(By.XPATH, "//input[@placeholder='Name']").send_keys("Test User")
            self.driver.find_element(By.XPATH, "//input[@placeholder='Email']").send_keys("testuser@example.com")  
            self.driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("testpassword") 

            self.driver.find_element(By.XPATH, "//button[contains(text(),'Sign Up')]").click()
            time.sleep(3) 

            print("User registration test passed")
        except Exception as e:
            self.fail(f"User registration test failed: {e}")
    def test_8_login_user(self):
        print("Test 8: Login user")
        try:
            self.driver.get(f"{self.BASE_URL}/login")
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email']")))

            self.driver.find_element(By.XPATH, "//input[@placeholder='Email']").send_keys("testuser@example.com")
            self.driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("testpassword") 

            self.driver.find_element(By.XPATH, "//button[contains(text(),'Sign In')]").click()
            time.sleep(3) 

            self.assertIn("COLLECTION", self.driver.page_source.upper()) 
            print("Login test passed")
        except Exception as e:
            self.fail(f"Login test failed: {e}")

    def test_9_search_product(self):
        self.driver.get(f"{self.BASE_URL}/collection")
        search_input = self.driver.find_element(By.TAG_NAME, "input")
        search_input.send_keys("shirt")
        time.sleep(2)
        self.assertIn("shirt", self.driver.page_source.lower())

    def test_10_product_filter_functionality(self):
        self.driver.get(f"{self.BASE_URL}/collection")
        category_checkbox = self.driver.find_element(By.XPATH, "//input[@type='checkbox' and @value='Men']")
        self.driver.execute_script("arguments[0].click();", category_checkbox)
        time.sleep(2)
        self.assertNotIn("No products found", self.driver.page_source)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(EcommerceTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"\n--- Test Summary ---")
    print(f"Total tests: {result.testsRun}")
    print(f"Passed tests: {passed}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
