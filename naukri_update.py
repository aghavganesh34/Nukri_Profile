from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Your credentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tempfile
import os

options = Options()
options.add_argument("--headless=new")          # headless mode for server
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Use a temporary directory for Chrome user data
temp_dir = tempfile.mkdtemp()
options.add_argument(f"--user-data-dir={temp_dir}")

driver = webdriver.Chrome(options=options)

RESUME_PATH = r"C:\Users\admin\Downloads\Resume.pdf"   # Update path to your resume

# Launch browser
driver.maximize_window()
driver.get("https://www.naukri.com/nlogin/login")

# Login
time.sleep(3)
driver.find_element(By.ID, "usernameField").send_keys(USERNAME)
driver.find_element(By.ID, "passwordField").send_keys(PASSWORD)
driver.find_element(By.XPATH, "//button[text()='Login']").click()

time.sleep(5)  # wait for login

# Go to profile page
# driver.get("https://www.naukri.com/mnjuser/profile")

time.sleep(5)
driver.set_page_load_timeout(20)
wait = WebDriverWait(driver, 60)
wait.until(
    EC.visibility_of_element_located((By.XPATH, "//*[@class='info__heading']"))
)


ele=driver.find_element(By.XPATH,"//*[@class='info__heading']").get_attribute("title")
print(ele)
driver.get("https://www.naukri.com/mnjuser/profile")
# Click upload resume
file_input = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@id='attachCV']"))
)
file_input.send_keys(RESUME_PATH)

# upload_button = driver.find_element(By.XPATH, "//input[@id='attachCV']")
# upload_button.send_keys(RESUME_PATH)

time.sleep(5)

print("✅ Resume updated successfully!")
driver.quit()

