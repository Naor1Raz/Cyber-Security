import requests
from bs4 import BeautifulSoup
import os
import time
import random


cookies = {
    'CookieName1': '0f5Lkv7IkMtQsHBq59BjxDCF0wljh4dUfL6usUvJ',
    'CookieName2': 'a8460eec8766cac411c4',
    'CookieName3': '8ba2e7623f0425856c13',
    'CookieName4': 'd736866268505562e82d1b4d02c95ba8e1613031669',
    'CookieName5': 'bk70726024e8f51aab9',
    'CookieName6': 'bb103743c00d60809d7cf24f46cf15f9'
}

def getBooksLinkAndTitle(homeURL, directory_path):
    req = requests.get(homeURL, cookies=cookies)
    soup = BeautifulSoup(req.text, "html.parser")
    for ultag in soup.find_all('ul', class_="list-unstyled"):
        for litag in ultag.find_all('li'):
            for a in litag.find_all('a'):
                try:
                    chapter_name = a.text
                    chapter_path = os.path.join(directory_path,chapter_name)
                    os.mkdir(chapter_path)
                    os.chdir(chapter_path)
                    bookURL = a['href']
                    countImagesForName = 1
                    getChaptersLinks(bookURL, chapter_path, chapter_name, countImagesForName)


                except Exception as e:
                    print(e)
                # print(a.text + "-->" + a['href'])


def getChaptersLinks(bookURL, chapter_path, chapter_name, countImagesForName):
    req = requests.get(bookURL, cookies=cookies)
    soup = BeautifulSoup(req.text, "html.parser")
    for a in soup.find_all('a', class_="subject-item "):
        print("Found the URL: ", a['href'])

        downloading(a['href'], chapter_path, chapter_name , countImagesForName)

def downloading(url, chapter_path, chapter_name, countImagesForName):

    req = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(req.text, "html.parser")
    for search in soup.findAll('img'):
        link = search.get('src')
        if "beyond" in link and link.endswith(".png"):
            print(link)
            parameters = link.split("/")

            new_parametr = parameters[len(parameters) - 1]
            date, name = new_parametr.split('-', 1)

            img_name = name
            print("Downloading Image --> ", img_name)
            f = open(chapter_path+r"\{}".format(img_name), "wb")
            f.write(requests.get(link).content)
            f.close
            print(("Done"))
            countImagesForName += 1
            # time.sleep(2)


def main():
    global cookies
    directory_path = r"C:\MyFolder"

    url = ""
    getBooksLinkAndTitle(url, directory_path)


if __name__ == '__main__':
    main()


