# naukri_update.py
import os
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------------------
# Read credentials from environment variables
# Make sure NAUKRI_USERNAME and NAUKRI_PASSWORD are set as GitHub Secrets
USERNAME = os.getenv("NAUKRI_USERNAME")
PASSWORD = os.getenv("NAUKRI_PASSWORD")

# Path to resume inside repo
RESUME_PATH = os.path.join(os.getcwd(), "Resume.pdf")

# -------------------------------
# Chrome setup for headless server environment
options = Options()
options.add_argument("--headless=new")          # Headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Temporary user data dir to avoid session conflicts
temp_dir = tempfile.mkdtemp()
options.add_argument(f"--user-data-dir={temp_dir}")

driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(60)
wait = WebDriverWait(driver, 60)

try:
    # -------------------------------
    # Open Naukri login page
    driver.get("https://www.naukri.com/nlogin/login")

    # -------------------------------
    # Wait for login fields and enter credentials
    username_input = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
    username_input.send_keys(USERNAME)

    password_input = wait.until(EC.presence_of_element_located((By.ID, "passwordField")))
    password_input.send_keys(PASSWORD)

    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']")))
    login_button.click()

    # -------------------------------
    # Wait for profile info to load
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='info__heading']")))
    profile_name = driver.find_element(By.XPATH, "//*[@class='info__heading']").get_attribute("title")
    print(f"Logged in as: {profile_name}")

    # -------------------------------
    # Go to profile page
    driver.get("https://www.naukri.com/mnjuser/profile")

    # Wait for resume upload input
    file_input = wait.until(EC.presence_of_element_located((By.ID, "attachCV")))
    file_input.send_keys(RESUME_PATH)

    print("✅ Resume updated successfully!")

finally:
    driver.quit()
    
