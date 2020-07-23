import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.aljazeera.com/news/2020/03/coronavirus-travel-restrictions-border-shutdowns-country-200318091505922.html"

# makes a request to the web page and gets its HTML
r = requests.get(url)

# stores the HTML page in 'soup', a BeautifulSoup object
soup = BeautifulSoup(r.content, features="html.parser")

df = pd.DataFrame(columns =['Country', 'Restriction'])
country = []
restriction = []
flag = 0
for link in soup.find_all("h3"):
    if flag == 0:
        country.append(link.get_text())
        next_sib = link.find_next_sibling(['p', 'h3'])
        text = []
        # loop to go through all paragraphs that come after a h3 tag
        while next_sib.name != 'h3':
            text.append(next_sib.get_text())
            next_sib = next_sib.find_next_sibling(['p','h3'])
            if next_sib is None :
                flag = 1
                break
        restriction.append(' '.join(text))
    else:
        break
df['Country'] = country
df['Restriction'] = restriction

df.to_json('travel-restriction.json')
df.to_csv('travel-restriction.csv')