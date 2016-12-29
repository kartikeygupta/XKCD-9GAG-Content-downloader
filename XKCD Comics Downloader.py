#! python3
import requests, os
from bs4 import BeautifulSoup as bs

# Script asks User to enter a valid pathname. This section of the code will be repeated as long
# as a valid pathname is not entered, or the User doesn't quits
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
####################################################################################################################################################
# Script asks the user for 3 things
# extension: ID of the latest/earliest comic
# toOrFrom: Asks the user whether the above mentioned comic the most recent comic in the
#           consecutive set, or the earliest
# noOfComics: Self-explanatory
home = "http://www.xkcd.com"
extension = '/' + input("Enter the id of the latest comic in the set you wish to download: ")
if extension == '/':
    print("No value entered. Downloading from the most recent comic now...")

toOrFromFlag = False
while not toOrFromFlag:
    toOrFrom = int(input("Is this comic the latest(1) in the consecutive set that you wish to download, or the earliest(2)? "))
    if toOrFrom != 1 and toOrFrom != 2:
        print("Invalid Entry. Try again")
    else:
        toOrFromFlag = True
        if toOrFrom == 2:
            toOrFrom = 3
            
noOfComics  = int(input("Enter the number of comics in the set that you wish to download: "))
ctr = 0
#####################################################################################################################################################

# Going step-by-step...
for i in range(0, noOfComics):
    res = requests.get(home + extension) #Download the source code of the current comic's page
    soup = bs(res.text, 'html.parser')
    middleSection = soup.select("#middleContainer ul li")
    extension = middleSection[toOrFrom].select("a")[0].get("href") #Get the address to next comic which is to be downloaded 

    # Just something I noticed. Trying to get the best possible resolution for a comic.
    if soup.select('#comic img')[0].get("srcset") == None:
        imageRes = requests.get('http:' + soup.select('#comic img')[0].get("src"))
    else:
        length = len(soup.select('#comic img')[0].get("srcset"))
        imageRes = requests.get('http:' + soup.select('#comic img')[0].get("srcset")[:length-3])


    filename = soup.select('#ctitle')[0].getText() + '.png' #Creating a filename using the image's title. Fortunately, they are all in PNG format :D
    if filename in os.listdir():
        print("There is already a file named \"{0}\". ID: {1}".format(filename, extension[1:len(extension)-1])) #Self-explanatory
        pass
    else:
        imageFile = open(filename, 'wb')                    #Python's
        for aChunkOfData in imageRes.iter_content(100000):  #recipe for
            imageFile.write(aChunkOfData)                   #creating a
        imageFile.close()                                   #binary file
        ctr += 1
        print("{0} successfully saved. ID: {1}".format(filename, extension[1:]))

print()
print('{0} comic(s) have been successfully downloaded and saved.'.format(ctr)) #Voila!
