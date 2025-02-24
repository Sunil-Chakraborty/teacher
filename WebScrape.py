from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in background (remove for debugging)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_t20i_runs(url):
    driver.get(url)

    try:
        # Wait for the statistics table to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cb-col.cb-col-100.cb-plyr-thead"))
        )

        # Find all rows in the stats table
        table_rows = driver.find_elements(By.CSS_SELECTOR, "table tr")

        for row in table_rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if cols and "T20I" in cols[0].text:
                t20i_runs = cols[4].text.strip()
                return t20i_runs
    except Exception as e:
        print("Error:", e)
        return None
    finally:
        driver.quit()

# Cricbuzz profile URL
url = "https://www.cricbuzz.com/profiles/1413/virat-kohli"
t20i_runs = scrape_t20i_runs(url)

if t20i_runs:
    print(f"Virat Kohli's T20I overall runs: {t20i_runs}")
else:
    print("Failed to scrape T20I runs.")
