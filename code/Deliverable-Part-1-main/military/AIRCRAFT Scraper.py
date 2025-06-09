from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

# Path to your ChromeDriver
CHROME_DRIVER_PATH = r"C:\Web Driver\chromedriver.exe"

# Base URL for WDMMA
BASE_URL = "https://www.wdmma.org/"

# Country-Air Force Mapping (Sample, Expand as needed)
country_codes = {
    "Lithuania": "lithuanian-air-force",
    "Malaysia": "royal-malaysian-air-force",
    "Mexico": "mexican-air-force",
    "Moldova": "moldovan-air-force",
    "Mongolia": "mongolian-air-force",
    "Morocco": "royal-moroccan-air-force",
    "Mozambique": "mozambique-air-force",
    "Myanmar": "myanmar-air-force",
    "NATO": "nato-current-aircraft-inventory",
    "Nepal": "nepalese-army-air-service-nepal",
    "Netherlands": "royal-netherlands-air-force",
    "New Zealand": "royal-new-zealand-air-force-rnzaf",
    "Niger": "niger-air-force",
    "Nigeria": "nigerian-air-force",
    "North Korea": "korean-peoples-army-air-force-north-korea",
    "Norway": "royal-norwegian-air-force-norway",
    "Oman": "royal-air-force-of-oman",
    "Pakistan": "pakistan-air-force",
    "Peru": "peruvian-air-force",
    "Philippines": "philippine-air-force",
    "Poland": "polish-air-force",
    "Portugal": "portuguese-air-force",
    "Qatar": "qatar-emiri-air-force",
    "Romania": "romanian-air-force",
    "Russia": "russian-air-force",
    "Saudi Arabia": "royal-saudi-air-force-saudi-arabia",
    "Serbia": "serbian-air-force",
    "Slovakia": "slovak-air-force",
    "Singapore": "republic-of-singapore-air-force",
    "South Africa": "south-african-air-force",
    "South Korea": "republic-of-korea-air-force-south-korea",
    "Spain": "spanish-air-force",
    "Sri Lanka": "sri-lanka-air-force",
    "Sweden": "swedish-air-force",
    "Switzerland": "swiss-air-force",
    "Syria": "syrian-air-force",
    "Taiwan": "republic-of-china-air-force-taiwan",
    "Thailand": "royal-thai-air-force-thailand",
    "Tunisia": "tunisian-air-force",
    "Turkey": "turkish-air-force-turkey",
    "Turkmenistan": "turkmen-air-force",
    "Ukraine": "ukrainian-air-force",
    "UAE": "united-arab-emirates-air-force",
    "United Kingdom": "royal-air-force-britain",
    "United States": "united-states-air-force",
    "Uzbekistan": "uzbekistan-air-and-air-defence-forces",
    "Venezuela": "venezuelan-national-bolivarian-military-aviation",
    "Vietnam": "vietnamese-peoples-air-force-vietnam",
    "Yemen": "yemen-arab-republic-air-force"
}

# Set up ChromeDriver
service = Service(CHROME_DRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode for efficiency
driver = webdriver.Chrome(service=service, options=options)

def scrape_air_force(country, code):
    url = f"{BASE_URL}{code}.php"
    driver.get(url)
    time.sleep(5)

    aircraft_data = []

    # Get all aircraft tiles (ignore "TOTAL" blocks by checking text)
    plate_blocks = driver.find_elements(By.CLASS_NAME, "acPlateContainer")

    for block in plate_blocks:
        try:
            # Skip summary blocks (usually have 'TOTAL' in them)
            if "TOTAL" in block.text:
                continue

            # Aircraft unit count (inside the inner .circle)
            unit = block.find_element(By.CLASS_NAME, "circle").text.split()[0].strip()

            # Aircraft name and role
            aircraft_name = block.find_elements(By.TAG_NAME, "span")[2].text.strip()
            role = block.find_elements(By.TAG_NAME, "span")[3].text.strip()

            aircraft_data.append([country, aircraft_name, unit, role])

        except Exception as e:
            print(f"❌ Error extracting aircraft for {country}: {e}")
            continue

    return aircraft_data

    if not aircraft_data:
        print(f"⚠️ No aircraft data found for {country} at {url}")

# Collect data for all specified countries
all_aircraft_data = []

for country, code in country_codes.items():
    print(f"Scraping data for {country}...")
    country_data = scrape_air_force(country, code)
    all_aircraft_data.extend(country_data)

# Save to CSV
df = pd.DataFrame(all_aircraft_data, columns=["Country", "Aircraft", "Units", "Role"])
df.to_csv("air_force_inventory4.csv", index=False)
print("✅ Scraping complete! Data saved to 'air_force_inventory4.csv'.")

# Close driver
driver.quit()