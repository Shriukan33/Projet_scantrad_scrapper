# -*- coding: utf-8 -*-

"""
This scrapper is used to get basic information on releases on the website
scantrad-union.com and save them in tracking.csv
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from os import path
from win10toast import ToastNotifier
import webbrowser
from sys import exit


def html_parser(link):
    """Gets the html code from a webpage, exits the scripts if unreachable"""
    try:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser")
    except Exception:
        exit()

    return page, soup


def get_info(link):
    """Return basic informations about a manga's mainpage as strings."""
    page, soup = html_parser(link)

    chapter = soup.find_all("span", class_="chapter-number")[0]\
        .get_text().replace("#", "")
    title = soup.select("div h2")[0].get_text()
    last_release = soup.find_all("span", style="margin: 0 15px;float: right;")[0].get_text()

    return chapter, title, last_release, link


def open_browser_tab(link):
    webbrowser.open_new(link)


def check_presence(tracking_database, link):
    """Checks the presence of the tracked link in the database."""
    return len(tracking_database.loc[tracking_database["Link"] == link]) == 1


def update_database(tracking_database, link, data):
    """Checks if the chapter number is greater than current one and updates."""
    # If the current saved last chapter number is lower than
    # the one we extracted
    if int(tracking_database.loc[tracking_database["Link"] == link].values[0][1]) <\
            int(data[0]["Last chapter"]):
        # Count the number of released episodes since last update
        global unread_chapter
        unread_chapter += (int(tracking_database.loc[tracking_database["Link"] == link].values[0][1]) -
                           int(data[0]["Last chapter"]))*-1

        tracking_database.loc[tracking_database["Link"] == link, "Last chapter"]\
            = data[0]["Last chapter"]


def main():

    # List of mangas I track
    tracked = ["https://scantrad-union.com/manga/solo-leveling/",
               "https://scantrad-union.com/manga/volcanic-age/"]

    # Makes the database accessible for all functions
    if path.exists("tracking.csv"):
        # global tracking_database
        tracking_database = pd.read_csv("tracking.csv")

    # Is used to display the notification afterwards
    global unread_chapter
    unread_chapter = 0

    # Getting basic informations to track
    for link in tracked:
        chapter, title, last_release, link = get_info(link)

        # Inserting the previously collected datas in database
        data = [{
            "Name": title,
            "Last chapter": chapter,
            "Last release": last_release,
            "Link": link}]

        # Creates or update the database
        if path.exists("tracking.csv") and \
                check_presence(tracking_database, link):

            update_database(tracking_database, link, data)

        elif path.exists("tracking.csv"):
            tracking_database = tracking_database.append(data)
            tracking_database.to_csv("tracking.csv", index=False)

        else:
            tracking_database = pd.DataFrame(data)
            tracking_database.to_csv("tracking.csv", index=False)

    toaster = ToastNotifier()
    if unread_chapter == 1:
        toaster.show_toast("Scantrad-union.com",
                           str(unread_chapter) + " new chapter to read !")
        tracking_database.to_csv("tracking.csv", index=False)
    elif unread_chapter > 1:
        toaster.show_toast("Scantrad-union.com",
                           str(unread_chapter) + " new chapters to read !")
        tracking_database.to_csv("tracking.csv", index=False)


if __name__ == '__main__':
    main()
