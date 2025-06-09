import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import shutil
import time

# List of countries
countries = [
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

# Military data categories
manpower_resources = [
    "Total Population:", "Available Manpower", "Fit-for-Service", "Reaching Mil Age Annually",
    "Tot Mil. Personnel (est.)", "Active Personnel", "Reserve Personnel", "Paramilitary"
]
airpower_resources = [
    "Aircraft Total", "Fighters", "Attack Types", "Transports (Fixed-Wing)", "Trainers", "Special-Mission",
    "Tanker Fleet", "Helicopters", "Attack Helicopters"
]
naval_resources = [
    "Total Assets", "Total Tonnage", "Aircraft Carriers", "Helicopter Carriers", "Destroyers", "Frigates",
    "Corvettes", "Submarines", "Patrol Vessels", "Mine Warfare"
]

# Initialize list to store all data
all_data = []

# Function to scrape Global Firepower data
def scrape_military_data(country):
    print(f"Scraping Global Firepower data for {country}...")
    url = f"https://www.globalfirepower.com/country-military-strength-detail.php?country_id={country}"
    
    country_data = {"Country": country.replace("-", " ")}

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch {country}, status code: {response.status_code}")
            return country_data

        soup = BeautifulSoup(response.text, "html.parser")

        # Scrape manpower data
        manpower_section = soup.find("button", string="MANPOWER [+]")
        if manpower_section:
            manpower_section = manpower_section.find_next("div", class_="contentSpecs")
            for resource in manpower_resources:
                label = manpower_section.find("span", string=lambda text: text and resource in text)
                if label:
                    value = label.find_next("span", class_="textWhite textShadow")
                    country_data[resource] = value.get_text(strip=True) if value else "Not Found"

        # Scrape airpower data
        airpower_section = soup.find("button", string="AIRPOWER [+]")
        if airpower_section:
            airpower_section = airpower_section.find_next("div", class_="contentSpecs")
            for category in airpower_resources:
                label = airpower_section.find("span", string=lambda text: text and category in text)
                if label:
                    value = label.find_next("span", class_="textWhite textShadow")
                    raw_text = value.get_text(strip=True) if value else "Not Found"
                    
                    # Extract Stock and Readiness separately
                    stock_match = re.search(r"Stock:\s*(\d+)", raw_text)
                    readiness_match = re.search(r"Readiness:\s*(\d+)", raw_text)
                    
                    country_data[f"{category} Stock"] = stock_match.group(1) if stock_match else "0"
                    country_data[f"{category} Readiness"] = readiness_match.group(1) if readiness_match else "0"

        # Scrape naval data
        naval_section = soup.find("button", string="NAVAL FORCES [+]")
        if naval_section:
            naval_section = naval_section.find_next("div", class_="contentSpecs")
            for category in naval_resources:
                label = naval_section.find("span", string=lambda text: text and category in text)
                if label:
                    value = label.find_next("span", class_="textWhite textShadow")
                    country_data[category] = value.get_text(strip=True) if value else "Not Found"

    except Exception as e:
        print(f"Error processing {country}: {e}")

    return country_data

# Scrape data for all countries
for country in countries:
    country_data = scrape_military_data(country)  # Global Firepower data
    all_data.append(country_data)

# Convert the data to a pandas DataFrame
df = pd.DataFrame(all_data)

# Save the cleaned data to CSV
csv_filename = "cleaned_military_power_data.csv"
df.to_csv(csv_filename, index=False)

# Move file to OneDrive directory
destination_folder = r"C:\Users\arman\OneDrive\Documents\PURDUE\Spring 2025\LOCKHEED IP"
destination_path = f"{destination_folder}\\cleaned_military_power_data.csv"

shutil.move(csv_filename, destination_path)

# Display cleaned data preview
print("\nCleaned Military Power Data Preview:")
print(df.head())

print(f"\nData successfully saved to: {destination_path}")