import requests, bs4, os
from datetime import date

def prerequesites():
    top_url = "https://www.gocomics.com/garfield/"
    startDate = input(
        "Enter date from when you need the comic strips(YYYY/MM/DD):  ")
    endDate = input("Enter end date(YYYY/MM/DD): ")
    os.makedirs('comics', exist_ok=True)
    return top_url + startDate, top_url + endDate


def get_html(url):
    page = requests.get(url)
    page.raise_for_status()
    html = bs4.BeautifulSoup(page.text, 'html.parser')
    return html


def getComic():
    url, endurl = prerequesites()
    
    while not url.endswith('#'):
        page = requests.get(url)
        page.raise_for_status()

        html = get_html(url)
        comicElement = html.select('img')

        if len(comicElement) == 0:
            print("An error occurred, the comic wasn't found.")
        else:
            comicUrl = comicElement[4].get('src')
            comicFile = requests.get(comicUrl)
            imageFile = open(
                f"comics/{url[34:38]}-{url[39:41]}-{url[42:44]}.jpg", 'wb')
            print("Downloading from", url)
            for i in comicFile.iter_content(100000):
                imageFile.write(i)
            imageFile.close()

        if url == endurl:
            print("Go check out /comics to be amused by the brilliance of Garfield!")
            break

        nextComic = html.select(
            'a[class="fa btn btn-outline-secondary btn-circle fa-caret-right sm"]')
        if len(nextComic) == 0:
            print("Bro you can't time travel, neither can I. ")
            print("Go check out /comics to be amused by the brilliance of Garfield.")
            break

        url = "https://www.gocomics.com" + nextComic[0].get("href")



if __name__ == '__main__':
    try:
        getComic()
    except KeyboardInterrupt:
        print("You have the aborted the process with Ctrl+C")