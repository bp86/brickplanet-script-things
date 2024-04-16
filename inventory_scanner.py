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
itemType = 1
rarity = 1  # 0 is all items | 1 is only rares
currentPage = 1 # dont change this
priceFilter = 250 # Change this number to whatever you want. if you dont want a filter, make it = None

inventoryURL = f"https://www.brickplanet.com/profile/{userId}/view-backpack?type={itemType}&page={currentPage}&rare={rarity}"

# Functions
    
def checkStatusCode(url):
    response = requests.get(url)
    return response.status_code >= 200 and response.status_code <= 400
    
def checkIfUserExists(userId):
    url = f"https://www.brickplanet.com/profile/{userId}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("title").text
    
    return checkStatusCode(url) and not "Players" in title
    
def getItemValue(item):
    pass # idk how to remotely load a dynamically loaded page thing

    
def getNameFromUserId(userId):
    pass # too lazy to figure this out

def filterNumber(num : str):
    filtered = ""
    abbreviationMultiplier = 1

    for char in num.strip():
        if char == "M": abbreviationMultiplier = 1000000
        if char.isdigit() or char == ".": filtered += char

    return float(filtered) * abbreviationMultiplier
    
    
    
# Main    

if checkIfUserExists(userId):
    
    while True:
        
        inventoryURL = f"https://www.brickplanet.com/profile/{userId}/view-backpack?type={itemType}&page={currentPage}&rare={rarity}"
        
        content = requests.get(inventoryURL).text
        soup = BeautifulSoup(content, "html.parser")
        
        allItemsOnPage = soup.find_all("div", class_ = "col-6 col-md-3")

        if soup.find_all("div", class_ = "faded"): break # If no items found on the page
        
        if not allItemsOnPage:
            print("Connection error. Either BP servers are down or you've sent too many requests. Program will resume in 10 seconds.")
            currentPage -= 1
            time.sleep(10)        
        
        print("\nCurrent Page:", currentPage)
        
        for item in allItemsOnPage:
            itemName = item.find("a", class_ = "d-block truncate text-decoration-none fw-semibold text-light mb-1").text.strip()
            price = None

            if item.find("div", class_ = "text-credits") != None:
                price = filterNumber(item.find("div", class_ = "text-credits").text.strip())
            
            if priceFilter == None or price == None:
                print(f"{itemName} : {price}")
            elif price <= priceFilter: # Filter can be '<=' or '>='
                print(f"{itemName} : {price}")
        
        currentPage += 1

    print("\nScanning Complete")
    
else:
    
    print("Player doesn't exist OR you've sent too many requests OR the BP servers are down.")