import requests, bs4, os
from datetime import date

message = "Go check out /comics to find the downloaded comic strips!"

def prerequesites():
    top_url = "https://www.gocomics.com/garfield/"
    startDate = input(
        "Enter date from when you need the comic strips(YYYY/MM/DD):  ")
    endDate = input("Enter end date(YYYY/MM/DD): ")
    os.makedirs('comics', exist_ok=True)
    return top_url + startDate, top_url + endDate


def get_html():
    page = requests.get()
    page.raise_for_status()
    html = bs4.BeautifulSoup(page.text, 'html.parser')
    return html


def download_comic():
    comicElement = get_html().select('img')
    comicUrl = comicElement[4].get('src')
    comicFile = requests.get(comicUrl)
    imageFile = open(
        f"comics/{url[34:38]}-{url[39:41]}-{url[42:44]}.jpg", 'wb')
    print("Downloading from", url)
    for i in comicFile.iter_content(100000):
        imageFile.write(i)
    imageFile.close()


def next_comic():
    nextComic = get_html().select(
        'a[class="fa btn btn-outline-secondary btn-circle fa-caret-right sm"]')
    global url
    url = "https://www.gocomics.com" + nextComic[0].get("href")


def get_all_comics():
    while not url.endswith('#'):
        try:
            download_comic()
        except IndexError:
            print("An error occurred, the comic wasn't found.")

        if url == endurl:
            print(message)
            break
        try:
            next_comic()
        except IndexError:
            print("The comic on that date doesn't exist! ")
            print(message)
            break


if __name__ == '__main__':
    try:
        get_all_comics()
    except KeyboardInterrupt:
        print("You have the aborted the process with Ctrl+C")