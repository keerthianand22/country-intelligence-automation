import requests
from bs4 import BeautifulSoup
import csv

# List of countries to scrape (from Macrotrends or other sources)
countries = [
    "america", "antigua-and-barbuda", "argentina", "aruba", "bahamas", "barbados", "belize", "bermuda", "bolivia", "brazil", "canada", "cayman-islands", "chile", "colombia", "costa-rica", "cuba", "dominica", "dominican-republic", "ecuador", "el-salvador", "grenada", "guatemala", "guyana", "haiti", "honduras", "jamaica", "mexico", "nicaragua", "panama", "paraguay", "peru", "puerto-rico", "suriname", "trinidad-and-tobago", "united-states", "uruguay", "venezuela", "albania", "andorra", "austria", "belarus", "belgium", "bosnia-and-herzegovina", "bulgaria", "croatia", "cyprus", "czech-republic", "denmark", "estonia", "euro-area", "faroe-islands", "finland", "france", "germany", "greece", "hungary", "iceland", "ireland", "isle-of-man", "italy", "kosovo", "latvia", "liechtenstein", "lithuania", "luxembourg", "malta", "moldova", "monaco", "montenegro", "netherlands", "north-macedonia", "norway", "poland", "portugal", "romania", "russia", "serbia", "slovakia", "slovenia", "spain", "sweden", "switzerland", "turkey", "ukraine", "united-kingdom", "algeria", "angola", "benin", "botswana", "burkina-faso", "burundi", "cameroon", "cape-verde", "central-african-republic", "chad", "comoros", "congo", "djibouti", "egypt", "equatorial-guinea", "eritrea", "ethiopia", "gabon", "gambia", "ghana", "guinea", "guinea-bissau", "ivory-coast", "kenya", "lesotho", "liberia", "libya", "madagascar", "malawi", "mali", "mauritania", "mauritius", "morocco", "mozambique", "namibia", "niger", "nigeria", "republic-of-the-congo", "rwanda", "sao-tome-and-principe", "senegal", "seychelles", "sierra-leone", "somalia", "south-africa", "south-sudan", "sudan", "swaziland", "tanzania", "togo", "tunisia", "uganda", "zambia", "zimbabwe", "afghanistan", "armenia", "azerbaijan", "bahrain", "bangladesh", "bhutan", "brunei", "cambodia", "china", "east-timor", "georgia", "hong-kong", "india", "indonesia", "iran", "iraq", "israel", "japan", "jordan", "kazakhstan", "kuwait", "kyrgyzstan", "laos", "lebanon", "macao", "malaysia", "maldives", "mongolia", "myanmar", "nepal", "north-korea", "oman", "palestine", "pakistan", "philippines", "qatar", "saudi-arabia", "singapore", "south-korea", "sri-lanka", "syria", "taiwan", "tajikistan", "thailand", "turkmenistan", "united-arab-emirates", "uzbekistan", "vietnam", "yemen", "australia", "fiji", "kiribati", "new-caledonia", "new-zealand", "papua-new-guinea", "samoa", "solomon-islands", "tonga", "vanuatu"
]

# Base URLs for exports and imports
base_urls = {
    "Export": "https://tradingeconomics.com/{}/exports-by-category",
    "Import": "https://tradingeconomics.com/{}/imports-by-category"
}

# Open a single CSV file to store all data
filename = "Trade_by_category_all_countries.csv"
with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    headers_written = False

    # Loop through each country and each trade type
    for trade_type, base_url in base_urls.items():
        for country in countries:
            url = base_url.format(country)
            headers = {"User-Agent": "Mozilla/5.0"}  # Set a user agent to avoid blocking
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                table = soup.find("table", class_="table table-hover")

                if table:
                    headers = [th.text.strip() for th in table.find_all("th")]
                    headers.append("Country")  # Add country column header
                    headers.append("Trade Type")  # Add trade type column header

                    if not headers_written:
                        writer.writerow(headers)  # Write headers only once
                        headers_written = True

                    for tr in table.find_all("tr")[1:11]:  # Extract only the first 10 rows
                        cells = [td.text.strip() for td in tr.find_all("td")]
                        if cells:
                            cells.append(country)  # Append country name
                            cells.append(trade_type)  # Append trade type (Export/Import)
                            writer.writerow(cells)

                    print(f"Data successfully added for {trade_type} of {country}")
                else:
                    print(f"Table not found for {trade_type} of {country}.")
            else:
                print(f"Failed to retrieve data for {trade_type} of {country}. Status code: {response.status_code}")
