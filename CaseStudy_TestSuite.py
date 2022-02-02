import unittest
from selenium import webdriver
import selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

def print_numbers():
    for i in range(1, 101):
        if i % 3 == 0 and i % 5 == 0:
            print("Resolver")
        elif i % 3 == 0:
            print("MThree")
        elif i % 5 == 0:
            print("MFive")
        else:
            print(i)


class ResolverCaseStudy(unittest.TestCase):

    # Sets up drivers to start running the test cases
    def setUp(self):
        self._option = Options()
        self._option.add_argument("--start-maximized")
        self._option.add_experimental_option("excludeSwitches", ["enable-logging"])
        self._option.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self._option)
        self.driver.get("http://localhost:5500/index.html")
        self.driver.implicitly_wait(15)

    # Verifies if the home page shows up by checking the header tag
    def test_smoke(self):
        heading = self.driver.find_element(By.TAG_NAME, "h1").text
        self.assertIn("Test 1", heading, msg="Smoke testing failed, check the server")

    # Tries entering values into modal and validates if it's visible on home page
    def test_modal(self):
        self.driver.find_element(By.XPATH, "//div[@id='test-1-div']//button").click()
        self.driver.find_element(By.XPATH, "//div[@class='modal-body']//input[@id='name']").send_keys("DummyValue1")
        self.driver.find_element(By.XPATH, "//div[@class='modal-body']//input[@id='city']").send_keys("DummyValue2")
        self.driver.find_element(By.XPATH, "//div[@class='modal-body']//button[@id='enter']").click()
        self.driver.find_element(By.XPATH, "//div[@class='modal-footer']//button").click()
        name = self.driver.find_element(By.ID, "nameVal").text
        city = self.driver.find_element(By.ID, "cityVal").text
        self.assertListEqual(["DummyValue1", "DummyValue2"], [name, city], msg="Entered values are not listed as expected")
    
    # Verifies dropdown menu with different edge cases
    def test_dropDown(self):
        self.driver.find_element(By.XPATH, "//div[@class='dropdown']//button").click()
        dropDown = [ele.text for ele in self.driver.find_elements(By.XPATH, "//ul[@class='dropdown-menu show']//li")]
        print(dropDown)
        self.driver.find_element(By.XPATH, "//input[@id='myInput']").send_keys("Angular")
        dropDown = [ele.text for ele in self.driver.find_elements(By.XPATH, "//ul[@class='dropdown-menu show']//li[not(@style)]")]
        self.assertListEqual(["Angular 2", "Angular"], dropDown, msg="Values in dropdown are not as expected")
        self.driver.find_element(By.XPATH, "//input[@id='myInput']").clear()
        self.driver.find_element(By.XPATH, "//input[@id='myInput']").send_keys("ReactJs")
        dropDown = self.driver.find_elements(By.XPATH, "//ul[@class='dropdown-menu show']//li[not(@style)]")
        self.assertCountEqual([], dropDown, msg="Dropdown is not empty as expected")


    # Verifies search functionality in the table
    def test_tableSearch(self):
        self.driver.find_element(By.XPATH, "//input[@id='searchMe']").send_keys("USA")
        searchResults = self.driver.find_elements(By.XPATH, "//tbody[@id='someTable']/tr[not(@style)]/td[contains(text(), 'USA')]")
        self.assertEqual(2, len(searchResults), msg="2 results are not displayed for USA as expected")
        self.driver.find_element(By.XPATH, "//input[@id='searchMe']").send_keys(Keys.CONTROL, 'a')
        self.driver.find_element(By.XPATH, "//input[@id='searchMe']").send_keys(Keys.BACKSPACE)
        searchResults = self.driver.find_elements(By.XPATH, "//tbody[@id='someTable']/tr[not(@style='display: none;')]")
        self.assertEqual(4, len(searchResults), msg="All contents of table is not displayed as expected")

    # Verifies if drag and drop is working as expected
    def test_dragNdrop(self):
        source = self.driver.find_element(By.XPATH, "//button[@id='drag1']")
        destination = self.driver.find_element(By.XPATH, "//div[@id='div1']")
        # Work around for known bug on drag functionality in Python selenium lib
        drag_file = open("drag_drop_script.js",  "r")
        javascript = drag_file.read()
        drag_file.close()
        self.driver.execute_script(javascript, source, destination)
        self.assertTrue(self.driver.find_element(By.XPATH, "//div[@id='div1']/button[@id='drag1']").is_displayed(), msg="Drag functionality is not working as expected")

    # Tears down the setup initialized once all the test cases are ran
    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':

    # unittest.main(verbosity=2)
    print_numbers()