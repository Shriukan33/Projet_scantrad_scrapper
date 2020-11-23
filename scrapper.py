# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

def get_last_chapter(link):
    """
    Gets the last chapter of a given manga with the url of the main page 
    of the website scantrad-union.com

    Parameters
    ----------
    link : str
        link must be an URL directing to the main page of the manga.
        Exemple : https://scantrad-union.com/manga/solo-leveling/

    Returns
    -------
    chapter : string
        The last available chapter. 

    """
    # Gets the html code and search for the last chapter out
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    chapter = soup.find_all("span", class_ = "chapter-number")[0]
    chapter = str(chapter)
    
    # Deletes the html tags to get only the number of the chapter
    skips = ['<span class="chapter-number">#',"</span>"]
    for char in skips:
        chapter = chapter.replace(char, "")
        
    return chapter


url = "https://scantrad-union.com/manga/star-martial-god-technique/"
chapter = get_last_chapter(url)

