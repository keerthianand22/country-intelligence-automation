from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import random

CHROME_DRIVER_PATH = r"C:\Web Driver\chromedriver.exe"
BASE_URL = "https://www.militaryfactory.com/armor/by-country.php?Nation="

# List of countries formatted as in the URL path
country_list = [
    "belarus", "uruguay", "jordan", "botswana", "taiwan", "central-african-republic", "niger", "ethiopia",
    "oman", "algeria", "chad", "south-sudan", "mozambique", "austria", "germany", "nicaragua", "japan",
    "united-arab-emirates", "belgium", "paraguay", "canada", "peru", "libya", "somalia", "north-macedonia",
    "tajikistan", "france", "turkey", "venezuela", "romania", "bulgaria", "angola", "kenya", "thailand",
    "democratic-republic-of-the-congo", "latvia", "saudi-arabia", "denmark", "cuba", "guatemala",
    "el-salvador", "spain", "mali", "suriname", "india", "vietnam", "israel", "georgia", "philippines",
    "slovenia", "chile", "ivory-coast", "sweden", "colombia", "republic-of-the-congo", "qatar", "eritrea",
    "malaysia", "united-kingdom", "kazakhstan", "estonia", "luxembourg", "mongolia", "uganda", "turkmenistan",
    "croatia", "iceland", "mauritania", "zimbabwe", "russia", "afghanistan", "albania", "argentina", "ukraine",
    "azerbaijan", "sierra-leone", "benin", "burkina-faso", "bahrain", "serbia", "kosovo", "liberia", "sudan",
    "namibia", "bolivia", "greece", "mexico", "portugal", "netherlands", "ghana", "senegal", "moldova",
    "south-africa", "dominican-republic", "yemen", "gabon", "egypt", "ecuador", "uzbekistan", "indonesia",
    "iran", "armenia", "ireland", "myanmar", "bangladesh", "bosnia-and-herzegovina", "cambodia", "iraq",
    "lebanon", "new-zealand", "united-states", "montenegro", "italy", "tunisia", "hungary", "panama",
    "singapore", "laos", "madagascar", "honduras", "bhutan", "sri-lanka", "poland", "slovakia", "switzerland",
    "nigeria", "czech-republic", "cameroon", "zambia", "belize", "north-korea", "kyrgyzstan", "lithuania",
    "pakistan", "syria", "nepal", "south-korea", "finland", "brazil", "kuwait", "australia", "china", "morocco",
    "tanzania", "norway"
]

def scrape_armor_inventory(country_code):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0")
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    armor_data = []
    url = f"{BASE_URL}{country_code}"

    try:
        driver.get(url)
        time.sleep(2.5)

        entries = driver.find_elements(By.XPATH, "//div[@class='box']")

        for entry in entries:
            try:
                name = entry.find_element(By.CLASS_NAME, "textLarge.textBold.textDkGray").text.strip()
                role = entry.find_element(By.CLASS_NAME, "textNormal.textGray").text.strip()
                year = entry.find_element(By.CLASS_NAME, "textNormal.textWhite").text.strip()
                armor_data.append([country_code, name, role, year])
            except Exception as inner:
                print(f"⚠️ Skipped an entry in {country_code}: {inner}")

    except Exception as e:
        print(f"❌ Failed for {country_code}: {e}")

    finally:
        driver.quit()

    return armor_data


# Master list
all_armor_data = []

# Run scraper per country
for country in sorted(country_list):
    print(f"🔍 Scraping armor data for {country}...")
    data = scrape_armor_inventory(country)
    all_armor_data.extend(data)
    time.sleep(random.uniform(1.5, 3.5))  # delay to mimic human behavior

# Save to CSV
df = pd.DataFrame(all_armor_data, columns=["Country", "System Name", "Role", "Year"])
df.to_csv("armor_inventory.csv", index=False)
print("✅ Scraping complete! Data saved to 'armor_inventory.csv'.")
