import os
import tempfile
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# -------------------------------
# Load credentials
if os.getenv("GITHUB_ACTIONS") != "true":
    # Local: use .env
    from dotenv import load_dotenv
    load_dotenv()

USERNAME = os.getenv("NAUKRI_USERNAME")
PASSWORD = os.getenv("NAUKRI_PASSWORD")

if not USERNAME or not PASSWORD:
    raise ValueError("❌ Username/Password not found. Set .env locally or GitHub Secrets.")

# Path to resume inside repo
RESUME_PATH = os.path.join(os.getcwd(), "Resume.pdf")

# -------------------------------
# Chrome options
options = Options()

if os.getenv("GITHUB_ACTIONS") == "true":
    # Headless mode for GitHub CI
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
else:
    print("ℹ️ Running locally → GUI mode (not headless)")

# Temporary user data dir
temp_dir = tempfile.mkdtemp()
options.add_argument(f"--user-data-dir={temp_dir}")
