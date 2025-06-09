import requests
from bs4 import BeautifulSoup
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

url = 'https://www.metoffice.gov.uk/research/climate/maps-and-data/location-specific-long-term-averages/gcpsvg3nc'

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    tables = soup.find_all('table')

    for idx, table in enumerate(tables):
        rows = []

        for row in table.find_all('tr'):
            cells = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
            rows.append(cells)

        csv_filename = f'heathrow_climate_data_table_{idx + 1}.csv'

        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)

        print(f'Table {idx + 1} has been written to {csv_filename}')
else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
