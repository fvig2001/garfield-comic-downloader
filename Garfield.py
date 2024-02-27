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
import sys

message = "Go check out /comics to find the downloaded comic strips!"
html = ''
lastHTML = ""
lastFile = ""

def prerequesites():
    top_url = "https://www.gocomics.com/garfield/"
    startDate = input(
        "Enter date from when you need the comic strips(YYYY/MM/DD):  ")
    endDate = input("Enter end date(YYYY/MM/DD): ")
    os.makedirs('comics', exist_ok=True)
    return top_url + startDate, top_url + endDate

def prerequesites_2(cusDate):
    top_url = "https://www.gocomics.com/garfield/"
    startDate = cusDate.replace("-","/")
    endDate = startDate
    os.makedirs('comics', exist_ok=True)
    return top_url + startDate, top_url + endDate

def get_html():
    page = requests.get(url)
    page.raise_for_status()
    global html
    html = bs4.BeautifulSoup(page.text, 'html.parser')
    return html


def download_comic(html):
    global lastFile
    Invalid = True
    while Invalid == True:    
        lastFile= f"comics/{url[34:38]}-{url[39:41]}-{url[42:44]}.jpg"
        comicElement = html.select('img')
        comicUrl = comicElement[4].get('src')
        comicFile = requests.get(comicUrl)
        imageFile = open(lastFile, 'wb')
        print("Downloading from", url)

    
        for i in comicFile.iter_content(100000):
            imageFile.write(i)
        imageFile.close()
        if os.path.getsize(lastFile) > 5000: #Check that it is greater than 5 KB as each comic is usually 40KB at least
            Invalid = False
        else:
            print("Retry Downloading from", url)        


def next_comic(html):
    nextComic = html.select(
        'a[class="fa btn btn-outline-secondary btn-circle fa-caret-right sm"]')
    global url
    url = "https://www.gocomics.com" + nextComic[0].get("href")


def get_all_comics():
    global lastHTML
    err = False
    while not url.endswith('#'):
        html = get_html()
        lastHTML = html
        try:
            err = False
            download_comic(html)
        except IndexError:
            err = True
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
    n = len(sys.argv)
    try:    
        if n > 1:
            url, endurl = prerequesites_2(sys.argv[1])
        else:
            url, endurl = prerequesites()
        get_all_comics()
    except KeyboardInterrupt:
        print("You have the aborted the process with Ctrl+C")
 