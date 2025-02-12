import requests
from bs4 import BeautifulSoup
from time import sleep

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

userID = 0  # Change to your desired UserID
itemType = 0  # Filters to only display items of this type. Number to item type above
rarity = 0  # 0 is all items | 1 is only rares

filterType = "Value"  # Filter types: Price and Value (for rares only)
valueFilter = 20 # Change this number to whatever you want. If you dont want a filter, make it = None
priceFilter = 100 # Change this number to whatever you want. If you dont want a filter, make it = None

userInventory = {} # The user's inventory
ignoreList = {} # List that caches items that dont meet the value/price requirement

inventoryURL = f"https://www.brickplanet.com/profile/{userID}/view-backpack?type={itemType}&page=1&rare={rarity}"


def StatusCode(url):
    response = requests.get(url)
    return response.status_code >= 200 and response.status_code <= 400

def UserExists(userID):
    url = f"https://www.brickplanet.com/profile/{userID}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("title").text

    return StatusCode(url) and "Players" not in title

def FilterNumber(num : str):
    filtered = ""
    abbreviationMultiplier = 1

    for char in num.strip():
        if char == "M":
            abbreviationMultiplier = 1000000

        if char.isdigit() or char == ".":
            filtered += char

    return float(filtered) * abbreviationMultiplier


if UserExists(userID):
    print("Scanning inventory")
    currentPage = 1

    while True:

        inventoryURL = f"https://www.brickplanet.com/profile/{userID}/view-backpack?type={itemType}&page={currentPage}&rare={rarity}"

        content = requests.get(inventoryURL).text
        soup = BeautifulSoup(content, "html.parser")

        allItemsOnPage = soup.find_all("div", class_ = "col-6 col-md-3")

        if soup.find_all("div", class_ = "faded"): # If no items found on the page
            break

        if not allItemsOnPage:
            print("Connection error. Either BP servers are down or you've sent too many requests. Program will resume in 10 seconds.")
            currentPage -= 1
            sleep(10)        

        for item in allItemsOnPage:
            itemContent = item.find("a", class_ = "d-block truncate text-decoration-none fw-semibold text-light mb-1")
            itemName = itemContent.text.strip()

            if itemName in ignoreList:
                continue

            if itemName in userInventory:
                userInventory[itemName][0] += 1 # Increment the quantity
                continue

            if filterType.lower() == "price":
                price = None

                if itemContent.find("div", class_ = "text-credits") != None:
                    price = FilterNumber(item.find("div", class_ = "text-credits").text.strip())

                if (priceFilter == None) or (price == None) or (price <= priceFilter): # priceFilter can be '<=' or '>='
                    userInventory[itemName] = [1, price] # [Quantity, price]
                else:
                    ignoreList[itemName] = True

            elif (filterType.lower() == "value" or filterType.lower() == "rap") and (rarity == 1):
                itemLink = itemContent["href"]
                content = requests.get(itemLink).text
                soup = BeautifulSoup(content, "html.parser")
                divThing = soup.find_all("div", class_ = "text-2xl fw-semibold text-credits mb-1")

                estimatedValue = FilterNumber(divThing[0].text.strip())

                if (valueFilter == None) or (estimatedValue >= valueFilter): # valueFilter can be '<=' or '>='
                   userInventory[itemName] = [1, estimatedValue] # [Quantity, estiimatedValue]
                else:
                    ignoreList[itemName] = True

            else:
                print("Invalid item type")
                break

        currentPage += 1

    print("\n")

    for item in userInventory:
        print(f"{item} x{userInventory[item][0]}    {filterType} = {userInventory[item][1]}")

else:
    print("Player doesn't exist OR you've sent too many requests OR the BP servers are down.")
