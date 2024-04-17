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

userId = 6731
itemType = 4
rarity = 1  # 0 is all items | 1 is only rares
currentPage = 1 # dont change this

filterType = "Value"  # Filter types: Value (rarity must = 1 to filter by value) and Price
valueFilter = 100 # Change this number to whatever you want. if you dont want a filter, make it = None
priceFilter = 250 # Change this number to whatever you want. if you dont want a filter, make it = None

goodList = [] # A list of items that the script will use to cach item names that meet the value/price requirement. makes the program run faster and saves isaac some money
ignoreList = [] # A list of items that the script will use to cach item names that dont meet the value/price requirement. makes the program run faster and saves isaac some money

inventoryURL = f"https://www.brickplanet.com/profile/{userId}/view-backpack?type={itemType}&page={currentPage}&rare={rarity}"

    
def checkStatusCode(url):
    response = requests.get(url)
    return response.status_code >= 200 and response.status_code <= 400
    
def checkIfUserExists(userId):
    url = f"https://www.brickplanet.com/profile/{userId}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("title").text
    
    return checkStatusCode(url) and not "Players" in title

def filterNumber(num : str):
    filtered = ""
    abbreviationMultiplier = 1

    for char in num.strip():
        if char == "M": abbreviationMultiplier = 1000000
        if char.isdigit() or char == ".": filtered += char

    return float(filtered) * abbreviationMultiplier



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
            itemContent = item.find("a", class_ = "d-block truncate text-decoration-none fw-semibold text-light mb-1")
            itemName = itemContent.text.strip()

            if itemName in ignoreList: continue

            if filterType.lower() == "price":
                price = None

                if itemContent.find("div", class_ = "text-credits") != None:
                    price = filterNumber(item.find("div", class_ = "text-credits").text.strip())
                
                if itemName in goodList:
                    print(f"{itemName} : {price}")
                elif priceFilter == None or price == None:
                    print(f"{itemName} : {price}")
                    goodList.append(itemName)
                elif price <= priceFilter: # Filter can be '<=' or '>='
                    print(f"{itemName} : {price}")
                    goodList.append(itemName)
                else:
                    ignoreList.append(itemName)

            elif (filterType.lower() == "value" or filterType.lower() == "rap") and rarity == 1:
                itemLink = itemContent["href"]
                content = requests.get(itemLink).text
                soup = BeautifulSoup(content, "html.parser")
                divThing = soup.find_all("div", class_ = "text-2xl fw-semibold text-credits mb-1")

                estimatedValue = filterNumber(divThing[0].text.strip())

                if itemName in goodList:
                    print(f"{itemName} : {estimatedValue}")
                elif valueFilter == None:
                    print(f"{itemName} : {estimatedValue}")
                    goodList.append(itemName)
                elif estimatedValue >= valueFilter:
                    print(f"{itemName} : {estimatedValue}")
                    goodList.append(itemName)
                else:
                    ignoreList.append(itemName)

            else:
                print("Invalid item type")
                break
        
        currentPage += 1
    
    print("\nScanning Complete")
    
else:
    print("Player doesn't exist OR you've sent too many requests OR the BP servers are down.")
