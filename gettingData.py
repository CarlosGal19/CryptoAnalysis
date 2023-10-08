import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd


def insert_data(soup):

    data=[]

    names=[]
    prices=[]
    capacities=[]
    volumes=[]
    history_hour=[]
    history_day=[]
    history_week=[]

    # Getting names

    name_items=soup.find_all('p', class_='sc-4984dd93-0 kKpPOn')

    for item in name_items:
        name=item.text.strip()
        names.append(name)

    # Gettin prices, volumes and capacities

    elements = soup.find_all('td', style='text-align:end')

    values=[0]

    for item in elements:

        content = item.get_text(strip=True)

        if content.startswith('$'):
            content=content[1:]
            content=content.replace(',','')
            values.append(content)


    for i, element in enumerate(values):
        if i%3==0:
            if i>0:
                element=element[:-4]
            volumes.append(int(element))
        elif i%3==1:
            prices.append(float(element))
        else:
            cadena=element.split('$')
            element=cadena[1]
            capacities.append(int(element))

    volumes.remove(0)

    # Getting history in last 24 hrs

    markets = soup.find_all('td', style='text-align:end')

    histories=[0]

    for market in markets:

        change=str(market)

        if change.startswith('<td style="text-align:end"><span class="sc-d55c02b-0 gUnzUB"><span class="icon-Caret-down"'):
            change = market.get_text(strip=True)
            if change.endswith('%'):
                number = -float(change[:-1])
                histories.append(number)

        elif change.startswith('<td style="text-align:end"><span class="sc-d55c02b-0 iwhBxy"><span class="icon-Caret-up"'):
            change = market.get_text(strip=True)
            if change.endswith('%'):
                number = float(change[:-1])
                histories.append(number)

    for i,history in enumerate(histories):
        if i%3==0:
            history_week.append(history)
        elif i%3==1:
            history_hour.append(history)
        else:
            history_day.append(history)

    history_week.remove(0)

    min_length = min(len(names), len(prices), len(volumes), len(capacities), len(history_hour), len(history_day), len(history_week))

    for i in range( min_length ):
        data.append({
            'Name':names[i],
            'Price':prices[i],
            'Volume':volumes[i],
            'Capacity':capacities[i],
            'History last hour':history_hour[i],
            'History last day':history_day[i],
            'History last week':history_week[i],
        })

    df = pd.DataFrame(data)
    current_date = datetime.now().date()
    df.to_csv(f"C:\\Users\\carlo\\OneDrive\\Escritorio\\CryptoAnalysis\\Data\\Data_{current_date}", index=False)


def get_content(url):
    response = requests.get(url)
    return response.content



def analyze_content(html):
    return BeautifulSoup(html, 'html.parser')


content_page=get_content("https://coinmarketcap.com/es/coins/")
soup= analyze_content(content_page)

insert_data(soup)
