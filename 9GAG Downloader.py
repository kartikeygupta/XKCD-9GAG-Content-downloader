#! python3
import requests, os
from bs4 import BeautifulSoup as bs

def filterTitle(title):
    unwantedChar = ['?', '<', '>', ':', '/', '\\', "\"", "*", "|"]
    for char in unwantedChar:
        if char in title:
            print("'" + title + "' - This title has some unwanted characters.")
            title = input("Enter a valid title name : ")
            return title
    return title        
pathFlag = False
while not pathFlag:
    pathname = input("Enter the path to the directory where you want to save the downloaded comics (Enter 'E' to exit): ")
    if pathname.upper() == 'E':
        exit()
    else:
        try:
            os.chdir(pathname)
        except OSError:
            print("You have entered an incorrect path. Try again.")
        else:
            pathFlag = True
            
os.chdir(pathname)

home = "http://www.9gag.com"

res = requests.get(home)
soup = bs(res.text, 'html.parser')

linkElems = soup.select('div article')

for i in range(0, len(linkElems)):
    mediaPageRes = requests.get(linkElems[i].get('data-entry-url'))
    mediaSoup = bs(mediaPageRes.text, 'html.parser')
    title = filterTitle(mediaSoup.select('header h2')[0].getText())

    if len(linkElems[i].select("video")) == 0:
        videoFlag = False
        if mediaSoup.select('img[class="badge-item-img"]')[0].get('src').endswith('.jpg'):
            title += '.jpg'
        elif mediaSoup.select('img[class="badge-item-img"]')[0].get('src').endswith('.png'):
            title += '.png'
    else:
        videoFlag = True
        title += '.mp4'    

    if title in os.listdir():
        print("There is already a file named \"{0}\". Not saving this file".format(title))
        pass
    else:
        if videoFlag:
            mediaRes = requests.get(mediaSoup.select('source')[0].get('src'))
        else:
            mediaRes = requests.get(mediaSoup.select('img[class="badge-item-img"]')[0].get('src'))       
        
        mediaFile = open(title, 'wb')
        for aChunkOfData in mediaRes.iter_content(10000):
            mediaFile.write(aChunkOfData)
        mediaFile.close()
        print("Saved {0}".format(title))

print("That's it!")
