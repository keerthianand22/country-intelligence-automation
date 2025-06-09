import os
import requests
from bs4 import BeautifulSoup
import csv

os.makedirs('climate_data', exist_ok=True)

cities = [
    "London", "Manchester", "Edinburgh", "Bristol", "Glasgow", 
    "Birmingham", "Liverpool", "Leeds", "Sheffield", "Newcastle upon Tyne", 
    "Nottingham", "Cardiff", "Southampton", "Leicester", "Coventry", 
    "Belfast", "Plymouth", "Derby", "Wakefield"
]
for city in cities:
    url = f"https://en.wikipedia.org/wiki/{city}#climate"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    tables = soup.find_all('table', {'class': 'wikitable'})
    
    if tables:
        table = tables[0]
        
        with open(f'climate_data/{city}_climate_data.csv', 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            
            headers = table.find_all('th')
            writer.writerow([header.get_text(strip=True) for header in headers])
            
            rows = table.find_all('tr')[1:]  # Skip header row
            for row in rows:
                cols = row.find_all('td')
                if cols:  # Ensure the row has columns
                    writer.writerow([col.get_text(strip=True) for col in cols])
    else:
        print(f"No climate table found for {city}.")
