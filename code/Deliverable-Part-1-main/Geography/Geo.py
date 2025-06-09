from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import csv
from bs4 import BeautifulSoup

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# List of countries
countries = [
    "afghanistan", "albania", "algeria", "andorra", "angola", "argentina", "armenia", "australia", "austria", "azerbaijan",
    "bahamas-the", "bahrain", "bangladesh", "barbados", "belarus", "belgium", "belize", "benin", "bhutan", "bolivia",
    "bosnia-and-herzegovina", "botswana", "brazil", "brunei", "bulgaria", "burkina-faso", "burundi", "cambodia", "cameroon",
    "canada", "cape-verde", "central-african-republic", "chad", "chile", "china", "colombia", "comoros", "congo-democratic-republic-of-the",
    "congo-republic-of-the", "costa-rica", "cote-divoire", "croatia", "cuba", "cyprus", "czechia", "denmark", "djibouti", "dominican-republic",
    "ecuador", "egypt", "el-salvador", "equatorial-guinea", "eritrea", "estonia", "eswatini", "ethiopia", "fiji", "finland",
    "france", "gabon", "gambia-the", "georgia", "germany", "ghana", "greece", "greenland", "guatemala", "guinea",
    "guinea-bissau", "guyana", "haiti", "honduras", "hungary", "iceland", "india", "indonesia", "iran", "iraq", "ireland", "israel", "italy",
    "jamaica", "japan", "jordan", "kazakhstan", "kenya", "kiribati", "korea-north", "korea-south", "kosovo", "kuwait",
    "kyrgyzstan", "laos", "latvia", "lebanon", "lesotho", "liberia", "libya", "liechtenstein", "lithuania", "luxembourg",
    "madagascar", "malawi", "malaysia", "maldives", "mali", "malta", "marshall-islands", "mauritania", "mauritius", "mexico",
    "micronesia-federated-states-of", "moldova", "monaco", "mongolia", "montenegro", "morocco", "mozambique", "myanmar",
    "namibia", "nepal", "netherlands", "new-zealand", "nicaragua", "niger", "nigeria", "norway", "oman", "pakistan",
    "palau", "panama", "papua-new-guinea", "paraguay", "peru", "philippines", "poland", "portugal", "qatar", "romania",
    "russia", "rwanda", "saudi-arabia", "senegal", "serbia", "seychelles", "sierra-leone", "singapore", "slovakia", "slovenia",
    "solomon-islands", "somalia", "south-africa", "south-sudan", "spain", "sri-lanka", "sudan", "suriname", "sweden", "switzerland",
    "syria", "taiwan", "tajikistan", "tanzania", "thailand", "togo", "tonga", "trinidad-and-tobago", "tunisia", "turkey-turkiye",
    "turkmenistan", "uganda", "ukraine", "united-arab-emirates", "united-kingdom", "united-states", "uruguay", "uzbekistan",
    "vanuatu", "venezuela", "vietnam", "yemen", "zambia", "zimbabwe"
]

# Open CSV file for writing
csv_file = "geography_data_all_countries.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    header_written = False
    
    for country in countries:
        print(f"Scraping: {country}")  # Debugging log
        
        url = f"https://www.cia.gov/the-world-factbook/countries/{country}/#geography"
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        time.sleep(3)  # Allow time for the page to load
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()  # Close WebDriver
        
        geo_section = soup.find("div", id="geography")
        data_dict = {"Country": country.capitalize()}
        
        if geo_section:
            for item in geo_section.find_all("p"):
                strong_tag = item.find("strong")
                if strong_tag:
                    key = strong_tag.get_text(strip=True).replace(" :", "").strip()
                    value = item.get_text(strip=True).replace(key, "").strip()
                    data_dict[key] = value
        else:
            print(f"⚠️ Geography section not found for {country}!")
        
        # Write the header only once
        if not header_written:
            writer.writerow(data_dict.keys())
            header_written = True
        
        # Write the data row
        writer.writerow(data_dict.values())

print(f"✅ CSV file '{csv_file}' has been created with extracted geography data for all countries.")
