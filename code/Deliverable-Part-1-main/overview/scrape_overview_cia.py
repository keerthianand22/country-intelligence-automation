from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import csv
from pprint import pprint
import re
from html import unescape

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

# Define CSV file name
csv_filename = "overview.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
# Writing header
    writer.writerow([
                "Country", "Age structure - 0 - 14", "Age structure - 15 - 64", "Age structure - 65+",
                "Life expectancy at birth", "Median age", "Population", "Population growth rate",
                "Religion", "Religion %"
            ])

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
        
        # Now parse the page source and extract the energy section
        
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find the Energy section div using its id
        pas_section = soup.find("div", id="people-and-society")
        # Now, extract relevant data for each section
        sections = pas_section.find_all('div')

        data = {}

        fields_of_interest = [
            "Population", 
            "Age structure",
            "Population growth rate", 
            "Median age", 
            "Life expectancy at birth",
            "Religions"
        ]
        
        for field in fields_of_interest:
            section = soup.find(string=field)
            if section:
                value = str(section.find_next()).split("strong")
                data[field] = value
        
        # Close the Selenium WebDriver
        driver.quit()
        new_data = {
                'Age structure':{'0-14':"",'15-64':"",'65+':""},
                "Population":"",
                "Population growth rate":"",
                "Median age":"",
                "Life expectancy at birth":"",
                "Religions":[]
                }
        try:
            for i in data:
                if i == 'Age structure':
                    for j in range(0,len(data[i])):
                        if '0-14' in data[i][j]:
                            new_data[i]['0-14'] = data[i][j+1].split("%")[0].split(">")[-1]
                        elif '15-64' in data[i][j]:
                            new_data[i]['15-64'] = data[i][j+1].split("%")[0].split(">")[-1]
                        elif '65 years' in data[i][j]:
                            new_data[i]['65+'] = data[i][j+1].split("%")[0].split(">")[-1]
                elif i == 'Life expectancy at birth':
                    for j in range(0,len(data[i])):
                        if 'total' in data[i][j]:
                            new_data[i] = data[i][j+1].split("years")[0].split(">")[-1]
                            break
                elif i == 'Median age':
                    for j in range(0,len(data[i])):
                        if 'total' in data[i][j]:
                            new_data[i] = data[i][j+1].split("years")[0].split(">")[-1]
                            break
                elif i == 'Population':
                    for j in range(0,len(data[i])):
                        if 'total' in data[i][j]:
                            new_data[i] = data[i][j+1].split("<")[0].split(">")[-1]
                            break
                elif i == 'Population growth rate':
                    new_data[i] = data[i][0].split("%")[0].split(">")[-1]
                elif i == 'Religions':
                    religion=re.sub(r'\(.*?\)|<.*?>', '', data[i][0]).split(",")
                    def extract_info(entry):
                        entry = unescape(entry).strip()  # Convert HTML entities like &lt; to < and remove spaces
                        match = re.match(r'(.+?)\s*<?(\d+\.?\d*)%', entry)  # Extract name and number
                        if match:
                            return match.group(1).strip(), match.group(2) + '%'  # Reattach '%' to the number
                        return None
                    new_data[i]=[extract_info(item) for item in religion if extract_info(item)]
        except:
            pass
        age_structure = new_data['Age structure']
        common_values = [
            c.replace("-"," "),
            age_structure['0-14'].strip(),
            age_structure['15-64'].strip(),
            age_structure['65+'].strip(),
            new_data['Life expectancy at birth'].strip(),
            new_data['Median age'].strip(),
            new_data['Population'].strip(),
            new_data['Population growth rate'].strip()
        ]


        # Writing to CSV
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Writing data rows
            for religion, percentage in new_data['Religions']:
                writer.writerow(common_values + [religion, percentage.strip('%')])  # Remove % for numeric consistency

    except:
        raise

print(f"CSV file '{csv_filename}' has been created successfully!")    
