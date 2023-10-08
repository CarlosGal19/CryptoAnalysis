import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import numpy as np

def insert_data(soup):                      # Function which insert the data in a csv file

    data=[]                                 # All the arrays that will be needed are declared.

    names=[]
    prices=np.array([])
    capacities=np.array([])
    volumes=np.array([])
    history_hour=np.array([])
    history_day=np.array([])
    history_week=np.array([])


    name_items=soup.find_all('p', class_='sc-4984dd93-0 kKpPOn')            # Getting names

    for item in name_items:
        name=item.text.strip()
        names.append(name)


    elements = soup.find_all('td', style='text-align:end')                  # Getting prices, volumes and capacities
    elements_volume = soup.find_all('p', class_='sc-4984dd93-0 jZrMxO font_weight_500')

    values=np.array([0])

    for item in elements:                                      # Inserting the data that starts with '$' in a new array

        content = item.get_text(strip=True)

        if content.startswith('$'):
            content=content[1:]
            content=content.replace(',','')
            values=np.append(values,content)


    for i, element in enumerate(values):

        if i%3==0:                                            # Numbers with index 0,3,6,9,12,... belong to volumes

            volumes=np.append(volumes,element)                # The elements recorded in volumes aren´t corrects, so the
            volumes=np.delete(volumes,0)                      # array insert a data and then delete that data

        elif i%3==1:                                          # Numbers with index 1,4,7,10,13,... belong to prices
            prices=np.append(prices, float(element))
        else:                                                 # Numbers with index 2,5,8,11,14,... belong to volumes,
            cadena=element.split('$')                         # however the data gotten is not correct, it is necesary
            element=cadena[1]                                 # clean the data and take just the right part.
            capacities=np.append(capacities,element)


    for volume in elements_volume:                            # The array volumes is void, here the values are recorded
        insert=volume.get_text()                              # and cleaned correctly
        insert=insert[1:]
        insert=insert.replace(',','')
        volumes=np.append(volumes, int(insert))


    markets = soup.find_all('td', style='text-align:end')     # Getting history in last 24 hrs

    histories=np.array([0])                                   # All histories are saved here

    for market in markets:

        change=str(market)
        # If change contains the class='icon-Caret-down' a negative value is recorded
        if change.startswith('<td style="text-align:end"><span class="sc-d55c02b-0 gUnzUB"><span class="icon-Caret-down"'):
            change = market.get_text(strip=True)
            if change.endswith('%'):
                number = -float(change[:-1])
                histories=np.append(histories,number)
        # If change contains the class='icon-Caret-up' a positive value is saved
        elif change.startswith('<td style="text-align:end"><span class="sc-d55c02b-0 iwhBxy"><span class="icon-Caret-up"'):
            change = market.get_text(strip=True)
            if change.endswith('%'):
                number = float(change[:-1])
                histories=np.append(histories,number)

    for i,history in enumerate(histories):
        if i%3==0:                                          # Numbers with index 0,3,6,9,12,... belong to history_week
            history_week=np.append(history_week, history)
        elif i%3==1:                                        # Numbers with index 1,4,7,10,13,... belong to history_hour
            history_hour=np.append(history_hour, history)
        else:                                               # Numbers with index 2,5,8,11,14,... belong to history_day
            history_day=np.append(history_day, history)

    history_week=np.delete(history_week,0)                  # The first number of the array (0) is removed

    min_length = min(len(names), len(prices), len(volumes), len(capacities), len(history_hour), len(history_day), len(history_week))

    for i in range( min_length ):                           # The data are inserted in the array 'data'
        data.append({
            'Name':names[i],
            'Price':prices[i],
            'Volume':volumes[i],
            'Capacity':capacities[i],
            'History last hour':history_hour[i],
            'History last day':history_day[i],
            'History last week':history_week[i],
        })

    df = pd.DataFrame(data)                                  # Saving the array data as a DataFrame with Pandas
    current_time=datetime.now()
    format = "%Y-%m-%d_%H-%M-%S"
    df.to_csv(f"C:\\Users\\carlo\\OneDrive\\Escritorio\\CryptoAnalysis\\Data\\Data_{current_time.strftime(format)}", index=False)


def get_content(url):                                        # Sending request for get html code
    response = requests.get(url)
    return response.content



def analyze_content(html):                                   # Getting HTML code
    return BeautifulSoup(html, 'html.parser')


content_page=get_content("https://coinmarketcap.com/es/coins/")
soup= analyze_content(content_page)
insert_data(soup)
