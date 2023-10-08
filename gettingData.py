import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import numpy as np

def insert_data(soup):

    data=[]

    names=[]
    prices=np.array([])
    capacities=np.array([])
    volumes=np.array([])
    history_hour=np.array([])
    history_day=np.array([])
    history_week=np.array([])

    # Getting names

    name_items=soup.find_all('p', class_='sc-4984dd93-0 kKpPOn')

    for item in name_items:
        name=item.text.strip()
        names.append(name)

    # Gettin prices, volumes and capacities

    elements = soup.find_all('td', style='text-align:end')
    elements_volume = soup.find_all('p', class_='sc-4984dd93-0 jZrMxO font_weight_500')

    values=np.array([0])

    for item in elements:

        content = item.get_text(strip=True)

        if content.startswith('$'):
            content=content[1:]
            content=content.replace(',','')
            values=np.append(values,content)


    for i, element in enumerate(values):
        if i%3==0:
            volumes=np.append(volumes,element)
            volumes=np.delete(volumes,0)
        elif i%3==1:
            prices=np.append(prices, float(element))
        else:
            cadena=element.split('$')
            element=cadena[1]
            capacities=np.append(capacities,element)


    for volume in elements_volume:
        insert=volume.get_text()
        insert=insert[1:]
        insert=insert.replace(',','')
        volumes=np.append(volumes, int(insert))

    # Getting history in last 24 hrs

    markets = soup.find_all('td', style='text-align:end')

    histories=np.array([0])

    for market in markets:

        change=str(market)

        if change.startswith('<td style="text-align:end"><span class="sc-d55c02b-0 gUnzUB"><span class="icon-Caret-down"'):
            change = market.get_text(strip=True)
            if change.endswith('%'):
                number = -float(change[:-1])
                histories=np.append(histories,number)

        elif change.startswith('<td style="text-align:end"><span class="sc-d55c02b-0 iwhBxy"><span class="icon-Caret-up"'):
            change = market.get_text(strip=True)
            if change.endswith('%'):
                number = float(change[:-1])
                histories=np.append(histories,number)

    for i,history in enumerate(histories):
        if i%3==0:
            history_week=np.append(history_week, history)
        elif i%3==1:
            history_hour=np.append(history_hour, history)
        else:
            history_day=np.append(history_day, history)

    history_week=np.delete(history_week,0)

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
    current_time=datetime.now()
    format = "%Y-%m-%d_%H-%M-%S"
    df.to_csv(f"C:\\Users\\carlo\\OneDrive\\Escritorio\\CryptoAnalysis\\Data\\Data_{current_time.strftime(format)}", index=False)


def get_content(url):
    response = requests.get(url)
    return response.content



def analyze_content(html):
    return BeautifulSoup(html, 'html.parser')


content_page=get_content("https://coinmarketcap.com/es/coins/")
soup= analyze_content(content_page)

insert_data(soup)
