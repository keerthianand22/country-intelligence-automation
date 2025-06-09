import requests
from bs4 import BeautifulSoup
import pandas as pd
import wbgapi as wb
from functools import reduce

# Step 1: Scrape currency data
def get_currency_data():
    url = 'https://taxsummaries.pwc.com/glossary/currency-codes'
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print(f"Failed to fetch, status code: {response.status_code}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")
    section = soup.find('table')

    rows = section.find_all("tr")
    headers = [header.get_text(strip=True) for header in rows[0].find_all("td")]
    data = [[td.get_text(strip=True) for td in row.find_all("td")] for row in rows[1:]]
    df = pd.DataFrame(data, columns=headers)
    return df.rename(columns={'Territory': 'Country'})

# Step 2: Fetch defense spending as % of GDP data
def get_defense_data():
    df = wb.data.DataFrame('MS.MIL.XPND.GD.ZS', time=range(2014, 2028, 1), labels=True)
    df = df.rename(columns=lambda x: x.replace("YR", "defenseYR"))
    df.reset_index(inplace=True)
    return df

# Step 3: Fetch economy sector contribution data
def get_economy_data():
    df_agr = wb.data.DataFrame('NV.AGR.TOTL.ZS', time=2023, labels=True)
    df_ind = wb.data.DataFrame('NV.IND.TOTL.ZS', time=2023, labels=True)
    df_srv = wb.data.DataFrame('NV.SRV.TOTL.ZS', time=2023, labels=True)
    df_manf = wb.data.DataFrame('NV.IND.MANF.ZS', time=2023, labels=True)

    dfs = [df_agr, df_ind, df_srv, df_manf]
    df_combined = reduce(lambda left, right: pd.merge(left, right, on='Country', how='inner'), dfs)
    df_combined.reset_index(inplace=True)
    return df_combined

# Step 4: Fetch unemployment data
def get_unemployment_data():
    df = wb.data.DataFrame('SL.UEM.TOTL.ZS', time=2023, labels=True)
    df.reset_index(inplace=True)
    return df

# Fetch all data
df_currency = get_currency_data()
df_defense = get_defense_data()
df_economy = get_economy_data()
df_unemployment = get_unemployment_data()

# Merge all data on "Country"
dfs_to_merge = [df_currency, df_defense, df_economy, df_unemployment]
# print(df_currency.head())
# print(df_defense.head())
# print(df_economy.head())
# print(df_unemployment.head())
final_df = reduce(lambda left, right: pd.merge(left, right, on="Country", how="inner"), dfs_to_merge)
final_df.drop(['economy_x','economy_y'], inplace=True, axis=1)
#Save to CSV
final_df.to_csv("worldbank_overview.csv", index=False)

print("CSV file 'worldbank_overview.csv' has been created successfully!")
