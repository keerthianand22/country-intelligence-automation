# countries = ['belarus', 'uruguay', 'jordan', 'botswana', 'taiwan', 'central-african-republic', 'niger', 'ethiopia', 'oman', 'algeria', 'chad', 'south-sudan', 'mozambique', 'austria', 'germany', 'nicaragua', 'japan', 'united-arab-emirates', 'belgium', 'paraguay', 'canada', 'peru', 'libya', 'somalia', 'north-macedonia', 'tajikistan', 'france', 'turkey', 'venezuela', 'romania', 'bulgaria', 'angola', 'kenya', 'thailand', 'democratic-republic-of-the-congo', 'latvia', 'saudi-arabia', 'denmark', 'cuba', 'guatemala', 'el-salvador', 'spain', 'mali', 'suriname', 'india', 'vietnam', 'israel', 'georgia', 'philippines', 'slovenia', 'chile', 'ivory-coast', 'sweden', 'colombia', 'republic-of-the-congo', 'qatar', 'eritrea', 'malaysia', 'united-kingdom', 'kazakhstan', 'estonia', 'luxembourg', 'mongolia', 'uganda', 'turkmenistan', 'croatia', 'iceland', 'mauritania', 'zimbabwe', 'russia', 'afghanistan', 'albania', 'argentina', 'ukraine', 'azerbaijan', 'sierra-leone', 'benin', 'burkina-faso', 'bahrain', 'serbia', 'kosovo', 'liberia', 'sudan', 'namibia', 'bolivia', 'greece', 'mexico', 'portugal', 'netherlands', 'ghana', 'senegal', 'moldova', 'south-africa', 'dominican-republic', 'yemen', 'gabon', 'egypt', 'ecuador', 'uzbekistan', 'indonesia', 'iran', 'armenia', 'ireland', 'myanmar', 'bangladesh', 'bosnia-and-herzegovina', 'cambodia', 'iraq', 'lebanon', 'new-zealand', 'united-states-of-america', 'montenegro', 'italy', 'tunisia', 'hungary', 'panama', 'singapore', 'laos', 'madagascar', 'honduras', 'bhutan', 'sri-lanka', 'poland', 'slovakia', 'switzerland', 'nigeria', 'czech-republic', 'cameroon', 'zambia', 'beliz', 'north-korea', 'kyrgyzstan', 'lithuania', 'pakistan', 'syria', 'nepal', 'south-korea', 'finland', 'brazil', 'kuwait', 'australia', 'china', 'morocco', 'tanzania', 'norway']
# import requests
# from bs4 import BeautifulSoup

# for c in countries:
#     # URL for Russia military strength details on Global Firepower
#     url = "https://www.globalfirepower.com/country-military-strength-detail.php?country_id="+c
#     country_data = {"Country": c.replace("-"," ")}
#     # Fetch the webpage content
#     response = requests.get(url)
#     if response.status_code != 200:
#         raise Exception(f"Failed to fetch page, status code: {response.status_code}")

#     # Parse the page with BeautifulSoup
#     soup = BeautifulSoup(response.text, "html.parser")

#     # Define the resource labels to search for
#     resources = [
#         "Oil Production", "Oil Consumption", "Oil Deficit", "Oil Proven Reserves",
#         "Natural Gas Production", "Natural Gas Consumption", "Natural Gas Deficit", "Nat.Gas Proven Rez",
#         "Coal Production", "Coal Consumption", "Coal Deficit", "Coal Proven Reserves"
#     ]

#     # Dictionary to store extracted data
#     data = {}

#     # Find the "NATURAL RESOURCES" section
#     natural_resources_section = soup.find("button", string="NATURAL RESOURCES [+]").find_next("div", class_="contentSpecs")

#     # Extract values based on labels
#     for resource in resources:
#         label_element = natural_resources_section.find("span", string=lambda text: text and resource in text)
#         if label_element:
#             value_element = label_element.find_next("span", class_="textWhite textShadow")
#             if value_element:
#                 data[resource] = value_element.get_text(strip=True)

#     # Print extracted data
#     for key, value in data.items():
#         print(f"{key}: {value if value else 'Not Found'}")

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# List of countries
countries = ['belarus', 'uruguay', 'jordan', 'botswana', 'taiwan', 'central-african-republic', 'niger', 'ethiopia', 'oman', 'algeria', 'chad', 'south-sudan', 'mozambique', 'austria', 'germany', 'nicaragua', 'japan', 'united-arab-emirates', 'belgium', 'paraguay', 'canada', 'peru', 'libya', 'somalia', 'north-macedonia', 'tajikistan', 'france', 'turkey', 'venezuela', 'romania', 'bulgaria', 'angola', 'kenya', 'thailand', 'democratic-republic-of-the-congo', 'latvia', 'saudi-arabia', 'denmark', 'cuba', 'guatemala', 'el-salvador', 'spain', 'mali', 'suriname', 'india', 'vietnam', 'israel', 'georgia', 'philippines', 'slovenia', 'chile', 'ivory-coast', 'sweden', 'colombia', 'republic-of-the-congo', 'qatar', 'eritrea', 'malaysia', 'united-kingdom', 'kazakhstan', 'estonia', 'luxembourg', 'mongolia', 'uganda', 'turkmenistan', 'croatia', 'iceland', 'mauritania', 'zimbabwe', 'russia', 'afghanistan', 'albania', 'argentina', 'ukraine', 'azerbaijan', 'sierra-leone', 'benin', 'burkina-faso', 'bahrain', 'serbia', 'kosovo', 'liberia', 'sudan', 'namibia', 'bolivia', 'greece', 'mexico', 'portugal', 'netherlands', 'ghana', 'senegal', 'moldova', 'south-africa', 'dominican-republic', 'yemen', 'gabon', 'egypt', 'ecuador', 'uzbekistan', 'indonesia', 'iran', 'armenia', 'ireland', 'myanmar', 'bangladesh', 'bosnia-and-herzegovina', 'cambodia', 'iraq', 'lebanon', 'new-zealand', 'united-states-of-america', 'montenegro', 'italy', 'tunisia', 'hungary', 'panama', 'singapore', 'laos', 'madagascar', 'honduras', 'bhutan', 'sri-lanka', 'poland', 'slovakia', 'switzerland', 'nigeria', 'czech-republic', 'cameroon', 'zambia', 'beliz', 'north-korea', 'kyrgyzstan', 'lithuania', 'pakistan', 'syria', 'nepal', 'south-korea', 'finland', 'brazil', 'kuwait', 'australia', 'china', 'morocco', 'tanzania', 'norway']

# Define resource labels
resources = [
    "Oil Production", "Oil Consumption", "Oil Deficit", "Oil Proven Reserves",
    "Natural Gas Production", "Natural Gas Consumption", "Natural Gas Deficit", "Nat.Gas Proven Rez",
    "Coal Production", "Coal Consumption", "Coal Deficit", "Coal Proven Reserves"
]

# Initialize an empty list to store all country data
all_data = []

# Function to scrape data for a single country
def scrape_country_data(country):
    print(f"Scraping data for {country}...")
    url = f"https://www.globalfirepower.com/country-military-strength-detail.php?country_id={country}"
    country_data = {"Country": country.replace("-"," ")}

    try:
        # Fetch the webpage
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch {country}, status code: {response.status_code}")
            return None  # Skip this country

        # Parse the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Locate the "NATURAL RESOURCES" section
        natural_resources_section = soup.find("button", string="NATURAL RESOURCES [+]").find_next("div", class_="contentSpecs")
        if not natural_resources_section:
            print(f"No Natural Resources section found for {country}")
            return None

        # Extract resource values
        for resource in resources:
            label_element = natural_resources_section.find("span", string=lambda text: text and resource in text)
            if label_element:
                value_element = label_element.find_next("span", class_="textWhite textShadow")
                country_data[resource] = value_element.get_text(strip=True) if value_element else "Not Found"
            else:
                country_data[resource] = "Not Found"

        return country_data  # Return extracted data

    except Exception as e:
        print(f"Error processing {country}: {e}")
        return None  # Skip this country

# Scrape data for all countries
for country in countries:
    data = scrape_country_data(country)
    if data:
        all_data.append(data)  # Append valid data to the list
    time.sleep(1)  # Sleep to prevent overloading the server

# Convert the data to a pandas DataFrame
df = pd.DataFrame(all_data)

# Save the DataFrame to CSV
csv_filename = "natural_resources_all_countries.csv"
df.to_csv(csv_filename, index=False)

print(f"\nData successfully saved to {csv_filename}")
