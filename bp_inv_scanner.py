'''
INSTRUCTIONS:

Change the "userId" variable to the UserId of your choice.
Then, filter the items that you want to be shown by changing the "itemType" variable. 
    - 0 = All Items will be scanned
    - 1 = Only hats will be scanned
    - 2 = Only Crates will be scanned
    - The entire list can be found below in the "itemTypes" dictionary.

Change the "rarity" variable to either 0 or 1.  0 means that all items will be scanned, regardless of rarity.  1 means that only rares will be scanned.  2 >= will break the script.

Run the program and read the console to view the results.

'''



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
currentPage = 1 # DO NOT CHANGE THIS VARIABLE

inventoryURL = "https://www.brickplanet.com/profile/" + str(userId) + "/view-backpack?type=" + str(itemType) + "&page=" + str(currentPage) + "&rare=" + str(rarity)

# Functions
    
def checkStatusCode(url):
    response = requests.get(url)
    return response.status_code >= 200 and response.status_code <= 400
    
def checkIfUserExists(userId):
    url = "https://www.brickplanet.com/profile/" + str(userId)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("title").text
    
    return checkStatusCode(url) and not "Players" in title
    
def getItemValue(item):
    print()
    # idk how to get the estimated value. if you manage to do it, edit the script

    
def getNameFromUserId(userId):
    print()
    # If you know how to do this and/or get the userId when you input a username, please add that into the code
    # This isnt as important but the code for this function could be useful for future projects
    
    
    
# Main    

if checkIfUserExists(userId):
    
    while True:
        
        inventoryURL = "https://www.brickplanet.com/profile/" + str(userId) + "/view-backpack?type=" + str(itemType) + "&page=" + str(currentPage) + "&rare=" + str(rarity)
        
        content = requests.get(inventoryURL).text
        soup = BeautifulSoup(content, "html.parser")
        
        allItemsOnPage = soup.find_all("a", class_ = "d-block truncate text-decoration-none fw-semibold text-light mb-1")

        if soup.find_all("div", class_ = "faded"): break # If no items found on the page
        
        if not allItemsOnPage:
            print("Connection error. Either BP servers are down or you've sent too many requests. Program will resume in 10 seconds.")
            currentPage -= 1
            time.sleep(10)        
        
        print("\nCurrent Page:", currentPage)
        
        for item in allItemsOnPage:
            itemName = item.text.strip()
            #estimatedValue = getItemValue(item)
            #print(itemName, "| Estimated Value:", estimatedValue)
            print(itemName)
        
        currentPage += 1

    print("\nScanning Complete")
    
else:
    
    print("Player doesn't exist OR you've sent too many requests OR the BP servers are down.")
