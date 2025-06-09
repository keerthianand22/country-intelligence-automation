from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import csv

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (optional)
chrome_options.add_argument("start-maximized")  # Open in full-screen mode
chrome_options.add_argument("disable-infobars")  # Disables the 'Chrome is being controlled by automated software' infobar
chrome_options.add_argument("--disable-extensions")  # Disable extensions
chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
chrome_options.add_argument("--no-sandbox")  # Disable sandbox mode

# Add a real User-Agent to mimic a browser request
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

countries = [
    "afghanistan", "akrotiri-and-dhekelia", "albania", "algeria", "american-samoa",
    "andorra", "angola", "anguilla", "antarctica", "antigua-and-barbuda",
    "argentina", "armenia", "aruba", "ashmore-and-cartier-islands", "australia",
    "austria", "azerbaijan", "bahamas-the", "bahrain", "baker-island",
    "bangladesh", "barbados", "belarus", "belgium", "belize", "benin", "bermuda",
    "bhutan", "bolivia", "bosnia-and-herzegovina", "botswana", "bouvet-island",
    "brazil", "british-indian-ocean-territory", "british-virgin-islands",
    "brunei", "bulgaria", "burkina-faso", "burma", "burundi", "cabo-verde",
    "cambodia", "cameroon", "canada", "cayman-islands",
    "central-african-republic", "chad", "chile", "china", "christmas-island",
    "clipperton-island", "cocos-keeling-islands", "colombia", "comoros",
    "congo-democratic-republic-of-the", "congo-republic-of-the", "cook-islands",
    "coral-sea-islands", "costa-rica", "cote-divoire", "croatia", "cuba",
    "curacao", "cyprus", "czechia", "denmark", "djibouti", "dominica",
    "dominican-republic", "ecuador", "egypt", "el-salvador", "equatorial-guinea",
    "eritrea", "estonia", "eswatini", "ethiopia", "european-union",
    "falkland-islands-islas-malvinas", "faroe-islands", "fiji", "finland",
    "france", "french-polynesia", "french-southern-and-antarctic-lands", "gabon",
    "gambia-the", "gaza-strip", "georgia", "germany", "ghana", "gibraltar",
    "greece", "greenland", "grenada", "guam", "guatemala", "guernsey", "guinea",
    "guinea-bissau", "guyana", "haiti", "heard-island-and-mcdonald-islands",
    "holy-see-vatican-city", "honduras", "hong-kong", "howland-island",
    "hungary", "iceland", "india", "indonesia", "iran", "iraq", "ireland",
    "isle-of-man", "israel", "italy", "jamaica", "jan-mayen", "japan",
    "jarvis-island", "jersey", "johnston-atoll", "jordan", "kazakhstan", "kenya",
    "kingman-reef", "kiribati", "korea-north", "korea-south", "kosovo",
    "kuwait", "kyrgyzstan", "laos", "latvia", "lebanon", "lesotho", "liberia",
    "libya", "liechtenstein", "lithuania", "luxembourg", "macau", "madagascar",
    "malawi", "malaysia", "maldives", "mali", "malta", "marshall-islands",
    "mauritania", "mauritius", "mexico", "micronesia-federated-states-of",
    "midway-islands", "moldova", "monaco", "mongolia", "montenegro", "montserrat",
    "morocco", "mozambique", "namibia", "nauru", "navassa-island", "nepal",
    "netherlands", "new-caledonia", "new-zealand", "nicaragua", "niger",
    "nigeria", "niue", "norfolk-island", "north-macedonia",
    "northern-mariana-islands", "norway", "oman", "pakistan", "palau",
    "palmyra-atoll", "panama", "papua-new-guinea", "paracel-islands", "paraguay",
    "peru", "philippines", "pitcairn-islands", "poland", "portugal", "puerto-rico",
    "qatar", "romania", "russia", "rwanda", "saint-barthelemy",
    "saint-helena-ascension-and-tristan-da-cunha", "saint-kitts-and-nevis",
    "saint-lucia", "saint-martin", "saint-pierre-and-miquelon",
    "saint-vincent-and-the-grenadines", "samoa", "san-marino",
    "sao-tome-and-principe", "saudi-arabia", "senegal", "serbia", "seychelles",
    "sierra-leone", "singapore", "sint-maarten", "slovakia", "slovenia",
    "solomon-islands", "somalia", "south-africa",
    "south-georgia-and-south-sandwich-islands", "south-sudan", "spain",
    "spratly-islands", "sri-lanka", "sudan", "suriname", "svalbard", "sweden",
    "switzerland", "syria", "taiwan", "tajikistan", "tanzania", "thailand",
    "timor-leste", "togo", "tokelau", "tonga", "trinidad-and-tobago", "tunisia",
    "turkey-turkiye", "turkmenistan", "turks-and-caicos-islands", "tuvalu",
    "uganda", "ukraine", "united-arab-emirates", "united-kingdom",
    "united-states", "united-states-pacific-island-wildlife-refuges", "uruguay",
    "uzbekistan", "vanuatu", "venezuela", "vietnam", "virgin-islands",
    "wake-island", "wallis-and-futuna", "west-bank", "world", "yemen", "zambia",
    "zimbabwe"
]
country_dict = {}
for c in countries:
    try:
        # Set up the WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # URL of the page
        url = "https://www.cia.gov/the-world-factbook/countries/" + c

        # Open the webpage using Selenium
        driver.get(url)

        # Allow time for the page to load
        time.sleep(3)
        sources = ["Coal","Petroleum","Natural gas"]
        # Now parse the page source and extract the energy section
        
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find the Energy section div using its id
        energy_section = soup.find("div", id="energy")
        content = []
        if energy_section:
            for child in energy_section.children:
                if isinstance(child, str):  # If the child is a string (text)
                    if any(search_string in child.strip() for search_string in sources):
                        content.extend(child.strip().split("\n"))
                elif child.name:  # If the child is a tag
                    if any(search_string in child.get_text().strip() for search_string in sources):
                        content.extend(child.get_text(separator="\n").split("\n"))

        else:
            print("Energy section not found!")

        # Close the Selenium WebDriver
        driver.quit()

        csv_dict = {
            "coal": {
            "production": [],
            "consumption": [],
            "proven reserves": []
            },
            "petroleum": {
            "production": [],
            "consumption": [],
            "proven reserves": []
            },
            "natural gas": {
            "production": [],
            "consumption": [],
            "proven reserves": []
            }
        }

        for i in range(0,len(content)-1):
            
            if "Coal" in content[i]:
                resource = "coal"
                print(resource)
            elif "Petroleum" in content[i]:
                resource = "petroleum"
                print(resource)
            elif "Natural gas" in content[i]:
                resource = "natural gas"
                print(resource)
            if "production" in content[i]:
                csv_dict[resource]["production"].append(content[i+1])
                print("production")
                print(content[i+1])
            elif "consumption" in content[i]:
                csv_dict[resource]["consumption"].append(content[i+1])
                print("consumption")
                print(content[i+1])
            elif "proven reserves" in content[i]:
                csv_dict[resource]["proven reserves"].append(content[i+1])
                print("reserves")
                print(content[i+1])
        
        country_dict[c] = csv_dict
    except Exception as e:
        print("Error!",e)
    
print(country_dict)
csv_data = []
header = [
    'Country',
    'coal production', 'coal production year', 
    'coal consumption', 'coal consumption year', 
    'coal proven reserves', 'coal proven reserves year',
    'petroleum production', 'petroleum production year', 
    'petroleum consumption', 'petroleum consumption year', 
    'petroleum proven reserves', 'petroleum proven reserves year',
    'natural gas production', 'natural gas production year', 
    'natural gas consumption', 'natural gas consumption year', 
    'natural gas proven reserves', 'natural gas proven reserves year'
]
# Function to remove year from text and return year if present
def remove_year(value):
    if '(' in value and ')' in value:  # Check for text with brackets containing the year
        start = value.find('(')
        end = value.find(')')
        year = value[start+1:end]  # Extract year inside the parentheses
        value = value[:start].strip()  # Remove the year from the original text
        return value, year
    return value.strip(), ''  # No year found, return the value and empty string

# Process each country and resource
for country, resources in country_dict.items():
    row = [country]  # Start with the country name
    for resource, values in resources.items():
        # Ensure we handle missing values gracefully
        production, production_year = remove_year(values.get('production', [''])[0]) if values.get('production') else ('', '')
        consumption, consumption_year = remove_year(values.get('consumption', [''])[0]) if values.get('consumption') else ('', '')
        proven_reserves, proven_reserves_year = remove_year(values.get('proven reserves', [''])[0]) if values.get('proven reserves') else ('', '')

        # Add these resource-specific values to the row
        row.extend([production, production_year, consumption, consumption_year, proven_reserves, proven_reserves_year])


    csv_data.append(row)

# Write data to CSV
with open('resources_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(header)  # Write the dynamic header row
    writer.writerows(csv_data)  # Write the rows of data

print("CSV file 'resources_data.csv' has been created.")
