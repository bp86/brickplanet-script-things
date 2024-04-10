from bs4 import BeautifulSoup
import requests
import time

pageNumber = 1
url = f"https://www.brickplanet.com/shop/search?featured=0&rare=1&type=0&search=&sort_by=5&page={pageNumber}"

priceFilter = 20 # Filters out items that are selling above this number. Feel free to change this number


def numberFilter(num : str):
    filtered = ""
    abbreviationMultiplier = 1

    for char in num.strip():
        if char == "M": abbreviationMultiplier = 1000000
        if char.isdigit(): filtered += char

    return int(filtered) * abbreviationMultiplier


response = requests.get(url)

if response.status_code >= 200 and response.status_code <= 400:
    while True:
        url = f"https://www.brickplanet.com/shop/search?featured=0&rare=1&type=0&search=&sort_by=5&page={pageNumber}"
        
        content = requests.get(url).text
        soup = BeautifulSoup(content, "html.parser")

        allItemsOnPage = soup.find_all("div", class_ = "col-6 col-md-3")

        if not allItemsOnPage:
            response = requests.get(url)
            if not (response.status_code >= 200 and response.status_code <= 400):
                print("Connection error. Either BP servers are down or you've sent too many requests. Program will resume in 10 seconds.")
                pageNumber -= 1
                time.sleep(10)

            else: # If there arent any items on the page and the connection is fine, then break because you've scanned every item
                break


        print(f"\nCurrent Page: {pageNumber}")

        for item in allItemsOnPage:
            itemName = item.find("a", class_ = "d-block truncate text-decoration-none fw-semibold text-light mb-1").text.strip()

            if item.find("span", class_ = "text-muted text-sm"):
                #print(f"{itemName} has no sellers") # Comment this line out if you want to
                continue

            bestPrice = numberFilter(item.find("div", class_ = "text-credits").text.strip())

            if bestPrice > priceFilter: continue

            print(f"{itemName} selling for {bestPrice}")

        pageNumber += 1

else:
     print("You've sent too many requests OR the BP servers are down.")


print("\nScanning complete")
