import pandas as pd
import requests
from io import StringIO

# Fetch the data
url = "https://ourworldindata.org/grapher/electricity-prod-source-stacked.csv?v=1&csvType=full&useColumnShortNames=true"
response = requests.get(url, headers={'User-Agent': 'Our World In Data data fetch/1.0'}, verify=False)

df = pd.read_csv(StringIO(response.text))
df.to_csv('energy.csv')