import os
import tempfile
from time import sleep
# from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# -------------------------------
# Load credentials
# load_dotenv()  # works locally with .env
USERNAME = os.getenv("NAUKRI_USERNAME")
PASSWORD = os.getenv("NAUKRI_PASSWORD")

if not USERNAME or not PASSWORD:
    raise ValueError("❌ Username/Password not found. Set .env locally or GitHub Secrets.")

# Path to resume inside repo
RESUME_PATH = os.path.join(os.getcwd(), "Resume.pdf")

# -------------------------------
# Chrome options
options = Options()

# Detect if running in GitHub Actions
if os.getenv("GITHUB_ACTIONS") == "true":
    # Headless mode for GitHub CI
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
else:
    print("ℹ️ Running locally → GUI mode (not headless)")

# Temporary user data dir
temp_dir = tempfile.mkdtemp()
options.add_argument(f"--user-data-dir={temp_dir}")

# -------------------------------
# Start driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.set_page_load_timeout(60)
wait = WebDriverWait(driver, 60)

try:
    print("🌐 Opening Naukri login page...")
    driver.get("https://www.naukri.com/nlogin/login")

    # Extra wait for login page JS
    sleep(5)

    # -------------------------------
    # Login
    username_input = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
    username_input.send_keys(USERNAME)

    password_input = wait.until(EC.presence_of_element_located((By.ID, "passwordField")))
    password_input.send_keys(PASSWORD)

    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']")))
    login_button.click()

    # -------------------------------
    # Wait for profile info
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='info__heading']")))
    profile_name = driver.find_element(By.XPATH, "//*[@class='info__heading']").get_attribute("title")
    print(f"✅ Logged in as: {profile_name}")

    # -------------------------------
    # Go to profile page
    driver.get("https://www.naukri.com/mnjuser/profile")

    # Upload resume
    file_input = wait.until(EC.presence_of_element_located((By.ID, "attachCV")))
    file_input.send_keys(RESUME_PATH)

    # Confirm upload
    try:
        success_msg = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(),'successfully uploaded') or contains(text(),'uploaded successfully')]")
            )
        )
        print("✅ Resume updated:", success_msg.text)
    except:
        print("⚠️ Resume upload attempted, but success message not found. Check UI manually.")

finally:
    driver.quit()
    print("🚪 Closed browser.")
