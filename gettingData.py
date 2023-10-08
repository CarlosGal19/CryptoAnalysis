import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd


def insert_data():
    pass


def get_content(url):
    response = requests.get(url)
    return response.content



def analyze_content(html):
    return BeautifulSoup(html, 'html.parser')


content_page=get_content("https://coinmarketcap.com/es/coins/")
soup= analyze_content(content_page)

insert_data(soup)
