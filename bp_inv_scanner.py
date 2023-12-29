# Initialization

import requests
from bs4 import BeautifulSoup
import time


itemTypes = {
    0 : "AllItems",
    1 : "Hats",
    2 : "Crates",
    3 : "Faces",
    4 : "Accessories",
    5 : "Bundles",
    6 : "Shirts",
    7 : "Pants",
    8 : "3D Objects",
    9 : "Scripts",
    10 : "Textures",
    11: "Sounds",
    12 : "Models"
}

userId = 1
itemType = 0
currentPage = 1
rarity = 0

inventoryURL = "https://www.brickplanet.com/profile/" + str(userId) + "/view-backpack?type=" + str(itemType) + "&page=" + str(currentPage) + "&rare=" + str(rarity)


####################################################


# Functions
    
def checkStatusCode(url):
    response = requests.get(url)
    return response.status_code >= 200 and response.status_code <= 400
    
def checkIfUserExists(userId):
    url = "https://www.brickplanet.com/profile/" + str(userId)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("title").text
        
    #return response.status_code >= 200 and response.status_code <= 400 and not '<meta property="og:url" content="https://www.brickplanet.com/players">' inresponse.text
        
    return checkStatusCode(url) and not "Players" in title
    
def getItemValue(item):
    itemURL = item.get("href")

    
def getNameFromUserId(userId):
    print()
    
    
    
# Main    

if checkIfUserExists(userId):
    
    while True:
        
        inventoryURL = "https://www.brickplanet.com/profile/" + str(userId) + "/view-backpack?type=" + str(itemType) + "&page=" + str(currentPage) + "&rare=" + str(rarity)
        
        content = requests.get(inventoryURL).text
        
        soup = BeautifulSoup(content, "html.parser")
        
        allItemsOnPage = soup.find_all("a", class_ = "d-block truncate text-decoration-none fw-semibold text-light mb-1")
        
        if not allItemsOnPage:
            print("Connection error. Either BP servers are down or you've sent too many requests. Program will resume in 10 seconds.")
            currentPage -= 1
            time.sleep(10)        
        
        if soup.find_all("div", class_ = "faded"): 
            break        
        
        print("\nCurrent Page:", currentPage)
        
        for item in allItemsOnPage:
            itemName = item.text.strip()
            #estimatedValue = getItemValue(item)
            #print(itemName, "| Estimated Value:", estimatedValue)
            print(itemName)
        
        currentPage += 1

    print("Scanning Complete")
    
else:
    
    print("Player doesn't exist OR you've sent too many requests")

