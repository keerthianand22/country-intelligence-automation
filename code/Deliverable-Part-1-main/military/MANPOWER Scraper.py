from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import random

# Constants
CHROME_DRIVER_PATH = r"C:\Web Driver\chromedriver.exe"
BASE_URL = "https://www.globalfirepower.com/country-military-strength-detail.php?country_id="

# Your full country_codes list
country_codes = [ 
      'belarus', 'uruguay', 'jordan', 'botswana', 'taiwan', 'central-african-republic', 'niger', 'ethiopia',
    'oman', 'algeria', 'chad', 'south-sudan', 'mozambique', 'austria', 'germany', 'nicaragua', 'japan',
    'united-arab-emirates', 'belgium', 'paraguay', 'canada', 'peru', 'libya', 'somalia', 'north-macedonia',
    'tajikistan', 'france', 'turkey', 'venezuela', 'romania', 'bulgaria', 'angola', 'kenya', 'thailand',
    'democratic-republic-of-the-congo', 'latvia', 'saudi-arabia', 'denmark', 'cuba', 'guatemala',
    'el-salvador', 'spain', 'mali', 'suriname', 'india', 'vietnam', 'israel', 'georgia', 'philippines',
    'slovenia', 'chile', 'ivory-coast', 'sweden', 'colombia', 'republic-of-the-congo', 'qatar', 'eritrea',
    'malaysia', 'united-kingdom', 'kazakhstan', 'estonia', 'luxembourg', 'mongolia', 'uganda', 'turkmenistan',
    'croatia', 'iceland', 'mauritania', 'zimbabwe', 'russia', 'afghanistan', 'albania', 'argentina', 'ukraine',
    'azerbaijan', 'sierra-leone', 'benin', 'burkina-faso', 'bahrain', 'serbia', 'kosovo', 'liberia', 'sudan',
    'namibia', 'bolivia', 'greece', 'mexico', 'portugal', 'netherlands', 'ghana', 'senegal', 'moldova',
    'south-africa', 'dominican-republic', 'yemen', 'gabon', 'egypt', 'ecuador', 'uzbekistan', 'indonesia',
    'iran', 'armenia', 'ireland', 'myanmar', 'bangladesh', 'bosnia-and-herzegovina', 'cambodia', 'iraq',
    'lebanon', 'new-zealand', 'united-states-of-america', 'montenegro', 'italy', 'tunisia', 'hungary', 'panama',
    'singapore', 'laos', 'madagascar', 'honduras', 'bhutan', 'sri-lanka', 'poland', 'slovakia', 'switzerland',
    'nigeria', 'czech-republic', 'cameroon', 'zambia', 'beliz', 'north-korea', 'kyrgyzstan', 'lithuania',
    'pakistan', 'syria', 'nepal', 'south-korea', 'finland', 'brazil', 'kuwait', 'australia', 'china', 'morocco',
    'tanzania', 'norway'
]

def scrape_manpower(country_code):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122 Safari/537.36")
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    manpower_data = []
    url = f"{BASE_URL}{country_code}"

    try:
        driver.get(url)
        time.sleep(3)

        # Click the MANPOWER section
        manpower_button = driver.find_element(By.XPATH, "//button[contains(text(),'MANPOWER')]")
        driver.execute_script("arguments[0].click();", manpower_button)
        time.sleep(2)

        # Now grab all the spec containers under that section
        section = manpower_button.find_element(By.XPATH, "following-sibling::div[contains(@class, 'contentSpecs')]")
        containers = section.find_elements(By.CLASS_NAME, "specsGenContainers")

        for container in containers:
            try:
                # Find the yellow label
                label_elem = container.find_element(By.XPATH, ".//span[contains(@class, 'textYellow')]")
                label = label_elem.text.strip().rstrip(":")

                # Find the white value span (main number)
                value_elem = container.find_element(By.XPATH, ".//span[contains(@class, 'textWhite')]")
                value = value_elem.text.strip().replace(",", "")

                if label and value:
                    manpower_data.append([country_code, label, value])
            except Exception as inner:
                print(f"⚠️ Skipped one metric in {country_code}: {inner}")

    except Exception as e:
        print(f"❌ Failed for {country_code}: {e}")

    finally:
        driver.quit()

    return manpower_data

# Run for all countries
all_manpower = []
for country in sorted(country_codes):
    print(f"🔍 Scraping manpower data for {country}...")
    data = scrape_manpower(country)
    all_manpower.extend(data)
    time.sleep(random.uniform(1.5, 3.5))  # simulate human-like delay

# Save to CSV
df = pd.DataFrame(all_manpower, columns=["Country", "Metric", "Value"])
df.to_csv("manpower_data.csv", index=False)
print("✅ All manpower data scraped and saved to 'manpower_data.csv'.")