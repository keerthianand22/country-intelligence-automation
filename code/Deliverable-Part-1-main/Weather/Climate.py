from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv

# Set up headless Chrome browser
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Set of countries you're interested in (from your list)
target_countries = {
    'afghanistan', 'albania', 'angola', 'antartica', 'argentina', 'australia', 'azerbaijan',
    'bahamas', 'bangladesh', 'belgium', 'brazil', 'bulgaria', 'canada', 'canary islands',
    'china', 'chile', 'costa rica', 'cuba', 'czech republic', 'denmark', 'dominican republic',
    'ecuador', 'egypt', 'england', 'ethiopia', 'fiji', 'finland', 'france', 'georgia',
    'germany', 'ghana', 'greece', 'greenland', 'guinea', 'hawaii', 'honduras', 'hungary',
    'iceland', 'indonesia', 'italy', 'japan', 'kazakhstan', 'kenya', 'lebanon', 'libya',
    'madagascar', 'malaysia', 'maldives', 'mauritius', 'mexico', 'morocco', 'nepal',
    'netherlands', 'new zealand', 'nigeria', 'north korea', 'norway', 'oman', 'pakistan',
    'paraguay', 'peru', 'philippines', 'poland', 'portugal', 'puerto rico', 'romania',
    'russia', 'saudi arabia', 'scotland', 'senegal', 'serbia', 'siberia', 'slovakia',
    'south africa', 'south korea', 'spain', 'sri lanka', 'sweden', 'switzerland', 'syria',
    'taiwan', 'tajikstan', 'thailand', 'tunisia', 'turkey', 'turkmenistan', 'uganda',
    'ukraine', 'uae', 'uk', 'uruguay', 'uzbekistan', 'venezula', 'vietnam', 'yemen',
    'zambia', 'zimbabwe'
}

# Load country-city links from the world climates page
main_url = "https://www.climatestotravel.com/world-climates/countries"
driver.get(main_url)
time.sleep(3)
soup = BeautifulSoup(driver.page_source, "html.parser")

city_links = []
for link in soup.select("a[href*='/climate/']"):
    href = link['href']
    full_url = "https://www.climatestotravel.com" + href
    city_name = link.text.strip()
    parts = href.split("/")
    if len(parts) > 2:
        country_key = parts[2].replace("-", " ").lower()
        if country_key in target_countries:
            city_links.append((city_name, full_url))

print(f"✅ Found {len(city_links)} matching city links for specified countries.")

# Scrape temperature tables
with open("climate_temperatures.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Country", "City", "Month", "Min Temp (°C)", "Max Temp (°C)", "Mean Temp (°C)"])

    for city_name, url in city_links:
        try:
            driver.get(url)
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            table = soup.find("table")
            if not table:
                print(f"⚠️ No table found for {city_name}")
                continue

            rows = table.find_all("tr")[1:]  # Skip header
            country = url.split("/")[4].replace("-", " ").title()

            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 4:
                    month = cols[0].text.strip()
                    min_temp = cols[1].text.strip()
                    max_temp = cols[2].text.strip()
                    mean_temp = cols[3].text.strip()
                    writer.writerow([country, city_name, month, min_temp, max_temp, mean_temp])
        except Exception as e:
            print(f"❌ Error scraping {city_name}: {e}")

driver.quit()
print("🎉 All data scraped and saved to 'climate_temperatures.csv'.")
