r"""
              --      --
            .:"  | .:'" |
          --  ___   ___  -
        /:.  /  .\ /.  \ .\
       |:|. ;\___/O\___/  :|
       |:|. |  `__|__'  | .|
       |:|.  \_,     ,_/  /
        \______       |__/
         |:.           \
        /.:,|  |        \
       /.:,.|  |         \
       |::.. \_;_\-;       |
 _____|::..    .::|       |
/   ----,     .::/__,    /__,
\_______|,...____;_;_|../_;_|
"""

import requests
import bs4
import os

message = "Go check out /comics to find the downloaded comic strips!"
html = ''


def prerequesites():
    top_url = "https://www.gocomics.com/garfield/"
    startDate = input(
        "Enter date from when you need the comic strips(YYYY/MM/DD):  ")
    endDate = input("Enter end date(YYYY/MM/DD): ")
    os.makedirs('comics', exist_ok=True)
    return top_url + startDate, top_url + endDate


def get_html():
    page = requests.get(url)
    page.raise_for_status()
    global html
    html = bs4.BeautifulSoup(page.text, 'html.parser')
    return html


def download_comic(html):
    comicElement = html.select('img')
    comicUrl = comicElement[4].get('src')
    comicFile = requests.get(comicUrl)
    imageFile = open(
        f"comics/{url[34:38]}-{url[39:41]}-{url[42:44]}.jpg", 'wb')
    print("Downloading from", url)
    for i in comicFile.iter_content(100000):
        imageFile.write(i)
    imageFile.close()


def next_comic(html):
    nextComic = html.select(
        'a[class="fa btn btn-outline-secondary btn-circle fa-caret-right sm"]')
    global url
    url = "https://www.gocomics.com" + nextComic[0].get("href")


def get_all_comics():
    while not url.endswith('#'):
        html = get_html()
        try:
            download_comic(html)
        except IndexError:
            print("An error occurred, the comic wasn't found.")

        if url == endurl:
            print(message)
            break
        try:
            next_comic(html)
        except IndexError:
            print("That comic isn't available yet!")
            print(message)
            break


if __name__ == '__main__':
    try:
        url, endurl = prerequesites()
        get_all_comics()
    except KeyboardInterrupt:
        print("You have the aborted the process with Ctrl+C")
 
