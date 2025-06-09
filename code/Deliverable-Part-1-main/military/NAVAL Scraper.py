from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

# Path to your ChromeDriver
CHROME_DRIVER_PATH = r"C:\Web Driver\chromedriver.exe"

# Base URL for WDMMW
BASE_URL = "https://www.wdmmw.org/"

# Country-Navy Mapping (sample - expand this list as needed)
country_codes = {
    "Algeria": "algerian-navy",
    "Argentina": "argentine-navy",
    "Australia": "royal-australian-navy",
    "Bangladesh": "bangladesh-navy",
    "Belgium": "belgian-navy",
    "Brazil": "brazilian-navy",
    "Canada": "royal-canadian-navy",
    "China": "peoples-liberation-army-navy-china",
    "Colombia": "colombian-navy",
    "Egypt": "egyptian-navy",
    "France": "french-navy",
    "Germany": "german-navy",
    "Greece": "hellenic-navy-greece",
    "India": "indian-navy",
    "Indonesia": "indonesian-navy",
    "Iran": "islamic-republic-of-iran-navy",
    "Israel": "israeli-navy",
    "Italy": "italian-navy",
    "Japan": "japan-maritime-self-defense-force",
    "Malaysia": "royal-malaysian-navy",
    "Netherlands": "royal-netherlands-navy",
    "North Korea": "korean-peoples-navy-north-korea",
    "Pakistan": "pakistan-navy",
    "Poland": "polish-navy",
    "Philippines": "philippine-navy",
    "Portugal": "portuguese-navy",
    "Russia": "russian-navy",
    "Saudi Arabia": "royal-saudi-navy",
    "Singapore": "republic-of-singapore-navy",
    "South Africa": "south-african-navy",
    "South Korea": "republic-of-korea-navy-south-korea",
    "Spain": "spanish-navy",
    "Sweden": "swedish-navy",
    "Taiwan": "republic-of-china-navy-taiwan",
    "Thailand": "royal-thai-navy-thailand",
    "Turkey": "turkish-navy",
    "Turkmenistan": "turkmen-naval-forces",
    "Ukraine": "ukrainian-naval-forces-ukraine",
    "United Kingdom": "royal-navy-britain",
    "United States": "united-states-navy"
}

# Set up ChromeDriver
service = Service(CHROME_DRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)

def scrape_navy(country, code):
    url = f"{BASE_URL}{code}.php"
    driver.get(url)
    time.sleep(5)

    navy_data = []

    # Find all major role sections (like Submarines, Frigates, etc.)
    sections = driver.find_elements(By.CLASS_NAME, "shpStripContainers")

    for section in sections:
        try:
            # Extract the role (e.g., Submarines, Frigates)
            role_header = section.find_element(By.TAG_NAME, "h3").text
            role = role_header.split(" (")[0].strip()

            # Get all ships in this role section (skip TOTAL blocks)
            ship_blocks = section.find_elements(By.CLASS_NAME, "shpPlateContainer")
            for block in ship_blocks:
                # Skip TOTAL block (usually white background, top card)
                if "TOTAL" in block.text:
                    continue

                try:
                    hull_count = block.find_element(By.CLASS_NAME, "circle").text.split()[0].strip()
                    spans = block.find_elements(By.TAG_NAME, "span")
                    name = spans[2].text.strip() if len(spans) > 2 else "N/A"
                    navy_data.append([country, name, hull_count, role])
                except Exception as inner_e:
                    print(f"⚠️ Ship block error in {country}: {inner_e}")
                    continue

        except Exception as section_e:
            print(f"❌ Could not process a section in {country}: {section_e}")
            continue

    if not navy_data:
        print(f"⚠️ No ship data found for {country} at {url}")

    return navy_data

# Collect data for all navies
all_navy_data = []

for country, code in country_codes.items():
    print(f"🔍 Scraping navy data for {country}...")
    country_data = scrape_navy(country, code)
    all_navy_data.extend(country_data)

# Save to CSV
df = pd.DataFrame(all_navy_data, columns=["Country", "Ship", "Units", "Role"])
df.to_csv("naval_inventory3.csv", index=False)
print("✅ Scraping complete! Data saved to 'naval_inventory3.csv'.")

# Close driver
driver.quit()