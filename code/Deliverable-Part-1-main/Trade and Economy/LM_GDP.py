import requests
import csv
from bs4 import BeautifulSoup

# List of countries and their URL representations
countries = {
    "USA": "united-states",
"CHN": "china",
"DEU": "germany",
"JPN": "japan",
"IND": "india",
"GBR": "united-kingdom",
"FRA": "france",
"ITA": "italy",
"BRA": "brazil",
"CAN": "canada",
"RUS": "russia",
"MEX": "mexico",
"AUS": "australia",
"KOR": "south-korea",
"ESP": "spain",
"IDN": "indonesia",
"NLD": "netherlands",
"TUR": "turkey",
"SAU": "saudi-arabia",
"CHE": "switzerland",
"POL": "poland",
"ARG": "argentina",
"BEL": "belgium",
"SWE": "sweden",
"IRL": "ireland",
"AUT": "austria",
"THA": "thailand",
"ISR": "israel",
"ARE": "uae",
"SGP": "singapore",
"NOR": "norway",
"BGD": "bangladesh",
"PHL": "philippines",
"VNM": "vietnam",
"DNK": "denmark",
"IRN": "iran",
"MYS": "malaysia",
"EGY": "egypt",
"HKG": "hong-kong",
"ZAF": "south-africa",
"COL": "colombia",
"NGA": "nigeria",
"ROU": "romania",
"PAK": "pakistan",
"CHL": "chile",
"CZE": "czech-republic",
"FIN": "finland",
"PRT": "portugal",
"PER": "peru",
"KAZ": "kazakhstan",
"NZL": "new-zealand",
"IRQ": "iraq",
"DZA": "algeria",
"GRC": "greece",
"HUN": "hungary",
"UKR": "ukraine",
"ETH": "ethiopia",
"KWT": "kuwait",
"MAR": "morocco",
"SVK": "slovak-republic",
"DOM": "dominican-republic",
"ECU": "ecuador",
"PRI": "puerto-rico",
"SDN": "sudan",
"OMN": "oman",
"KEN": "kenya",
"GTM": "guatemala",
"BGR": "bulgaria",
"UZB": "uzbekistan",
"CRI": "costa-rica",
"LUX": "luxembourg",
"AGO": "angola",
"LKA": "sri-lanka",
"PAN": "panama",
"HRV": "croatia",
"TZA": "tanzania",
"LTU": "lithuania",
"URY": "uruguay",
"GHA": "ghana",
"SRB": "serbia",
"AZE": "azerbaijan",
"BLR": "belarus",
"SVN": "slovenia",
"COD": "democratic-republic-of-congo",
"MMR": "myanmar",
"TKM": "turkmenistan",
"JOR": "jordan",
"LBY": "libya",
"UGA": "uganda",
"TUN": "tunisia",
"CMR": "cameroon",
"MAC": "macao",
"BOL": "bolivia",
"LVA": "latvia",
"BHR": "bahrain",
"PRY": "paraguay",
"NPL": "nepal",
"EST": "estonia",
"HND": "honduras",
"SLV": "el-salvador",
"CYP": "cyprus",
"KHM": "cambodia",
"ISL": "iceland",
"SEN": "senegal",
"PNG": "papua-new-guinea",
"GEO": "georgia",
"ZMB": "zambia",
"TTO": "trinidad-and-tobago",
"BIH": "bosnia",
"ZWE": "zimbabwe",
"ARM": "armenia",
"GIN": "guinea",
"ALB": "albania",
"MLT": "malta",
"MLI": "mali",
"MOZ": "mozambique",
"GAB": "gabon",
"BFA": "burkina-faso",
"MNG": "mongolia",
"HTI": "haiti",
"BEN": "benin",
"JAM": "jamaica",
"BWA": "botswana",
"NIC": "nicaragua",
"PSE": "west-bank-and-gaza",
"NER": "niger",
"GUY": "guyana",
"MDA": "moldova",
"MDG": "madagascar",
"LAO": "lao-pdr",
"COG": "republic-of-congo",
"BRN": "brunei",
"MKD": "north-macedonia",
"MUS": "mauritius",
"BHS": "bahamas",
"RWA": "rwanda",
"MWI": "malawi",
"KGZ": "kyrgyz-republic",
"TCD": "chad",
"NAM": "namibia",
"GNQ": "equatorial-guinea",
"TJK": "tajikistan",
"SOM": "somalia",
"MRT": "mauritania",
"XKX": "kosovo",
"TGO": "togo",
"MNE": "montenegro",
"MDV": "maldives",
"BRB": "barbados",
"FJI": "fiji",
"SWZ": "eswatini",
"LBR": "liberia",
"DJI": "djibouti",
"SLE": "sierra-leone",
"SUR": "suriname",
"AND": "andorra",
"BLZ": "belize",
"BDI": "burundi",
"CPV": "cabo-verde",
"CAF": "central-african-republic",
"LCA": "st-lucia",
"GMB": "gambia",
"TLS": "timor-leste",
"SYC": "seychelles",
"LSO": "lesotho",
"ATG": "antigua-and-barbuda",
"GNB": "guinea-bissau",
"SLB": "solomon-islands",
"SXM": "sint-maarten-dutch-part",
"TCA": "turks-and-caicos-islands",
"COM": "comoros",
"GRD": "grenada",
"VUT": "vanuatu",
"KNA": "st-kitts-and-nevis",
"VCT": "st-vincent-and-the-grenadines",
"WSM": "samoa",
"DMA": "dominica",
"STP": "sao-tome-and-principe",
"FSM": "micronesia",
"MHL": "marshall-islands",
"KIR": "kiribati",
"PLW": "palau",
"NRU": "nauru",
"TUV": "tuvalu",
"CUB": "cuba",
"IMN": "isle-of-man",
"CHI": "channel-islands",
"QAT": "qatar",
"CUW": "curacao",
"GRL": "greenland",
"SMR": "san-marino",
"BMU": "bermuda",
"MCO": "monaco",
"CYM": "cayman-islands",
"SYR": "syrian-arab-republic",
"MNP": "northern-mariana-islands",
"GUM": "guam",
"LIE": "liechtenstein",
"VIR": "virgin-islands-us",
"BTN": "bhutan",
"ASM": "american-samoa",
"ABW": "aruba",
"FRO": "faroe-islands",
"LBN": "lebanon",
"NCL": "new-caledonia",
"MAF": "st-martin-french-part",
"AFG": "afghanistan",
"PYF": "french-polynesia",
"TON": "tonga"
}

# Base URL for scraping
base_url = "https://www.macrotrends.net/global-metrics/countries/{}/gdp-gross-domestic-product"

# Prepare CSV file
csv_filename = "gdp_all_countries.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Country", "Year", "GDP", "Per Capita", "Growth"])  # Column headers

    for country_code, country_name in countries.items():
        url = base_url.format(f"{country_code}/{country_name}")
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the relevant tables
        tables = soup.find_all("table", class_="historical_data_table")
        if len(tables) < 2:
            print(f"Error: Less than two tables found for {country_name}")
            continue

        table = tables[1]  # Selecting the second table

        # Extract table rows
        for tr in table.find("tbody").find_all("tr"):
            cells = [td.text.strip() for td in tr.find_all("td")]
            if cells:  # Only add non-empty rows
                writer.writerow([country_name] + cells)

print(f"Data successfully saved to {csv_filename}")
