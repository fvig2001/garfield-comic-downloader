import requests, bs4, os
from datetime import date

def prerequesites():
    os.makedirs('comics', exist_ok=True)
    return "https://www.gocomics.com/garfield/" + date.today().strftime("%Y/%m/%d")


def getComic():

    url = prerequesites()
    while not url.endswith('#'):
        page = requests.get(url)
        page.raise_for_status()

        html = bs4.BeautifulSoup(page.text, 'html.parser')
        comicElement = html.select('a > picture > img[class="lazyload img-fluid"]')

        if len(comicElement)==0:
            print("An error occurred, the comic wasn't found.")
        else:
            comicUrl = comicElement[0].get('src')
            comicFile = requests.get(comicUrl)
            imageFile = open(f"comics/{url[34:38]}-{url[39:41]}-{url[42:44]}.jpg", 'wb')
            print("Downloading from", url)
            for i in comicFile.iter_content(100000):
                imageFile.write(i)
            imageFile.close()
  
        prevComic = html.select('a[class="fa btn btn-outline-secondary btn-circle fa-caret-left sm js-previous-comic"]')
        if len(prevComic)==0:
            print("Previous comic not found!")
            break
        url = "https://www.gocomics.com" + prevComic[0].get("href")


if __name__ == '__main__':
    getComic()