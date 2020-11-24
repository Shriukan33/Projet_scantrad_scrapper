# -*- coding: utf-8 -*-
"""
This scrapper is used to get basic information on releases on the website
scantrad-union.com and save them in tracking.csv
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from os import path

def html_parser(link):
    
    try:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser")
    except:
        RuntimeError(link + " might be down or unreachable")
        quit()
        
    return page, soup

def get_info(link):
    """ 
    Returns basic informations about a manga's mainpage as strings
    """
    page, soup = html_parser(link)
    
    chapter = soup.find_all("span", class_ = "chapter-number")[0]\
        .get_text().replace("#", "")
    title = soup.select("div h2")[0].get_text()
    last_release = soup.find_all("span", style="margin: 0 15px;float: right;")[0].get_text()
    
    return chapter, title, last_release, link

# List of mangas I track
tracked = ["https://scantrad-union.com/manga/solo-leveling/",
           "https://scantrad-union.com/manga/volcanic-age/"]

# Getting basic informations to track
for link in tracked:
    chapter , title, last_release, link = get_info(link)

    # Inserting the previously collected datas in database
    data = [{
        "Name": title,
        "Last chapter": chapter,
        "Last release": last_release,
        "Link": link}]
    
    # Creates or update the database
    if path.exists("tracking.csv"):
        tracking_database = pd.read_csv("tracking.csv")
        tracking_database = tracking_database.append(data)
        tracking_database.to_csv("tracking.csv", index=False)
    else:
        tracking_database = pd.DataFrame(data)
        tracking_database.to_csv("tracking.csv", index=False)
        
# Deleting the duplicates
tracking_database = pd.read_csv("tracking.csv")
tracking_database.drop_duplicates(subset=["Name"] , keep='last', inplace=True)
tracking_database.to_csv("tracking.csv", index=False)

print(tracking_database)
