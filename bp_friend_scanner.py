'''

INSTRUCTIONS:

Change the "userId" variable = to your desired userId (for brickplanet). 

Then run the program and read the console to view the results.

'''




import requests
from bs4 import BeautifulSoup
import time


userId = 2
numberOfFriends = 0


def checkStatusCode(url):
    response = requests.get(url)
    return response.status_code >= 200 and response.status_code <= 400

def checkIfUserExists(userId):
    profileURL = f"https://www.brickplanet.com/profile/{userId}"

    response = requests.get(profileURL)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("title").text
    
    return checkStatusCode(profileURL) and not "Players" in title


if checkIfUserExists(userId):
    currentPage = 1
    
    friendListURL = f"https://www.brickplanet.com/profile/{userId}/view-friends?page={currentPage}"
    
    response = requests.get(friendListURL)
    soup = BeautifulSoup(response.text, "html.parser")

    friendString = soup.find("div", class_ = "text-2xl fw-semibold mb-2").text # Example string: "BrickPlanet's Friends (0)"
    numberOfFriends = ""
    numberOfPages = 0


    # Finds where the "(" is located in "friendString"
    for i in range(len(friendString) - 2, -1, -1): # length of string - 2 because we dont need the last character ")"
        if friendString[i] == "(": break
        numberOfFriends += friendString[i]

    numberOfFriends = int(numberOfFriends[::-1]) # Reverses the string because the loop was in reverse order.
    numberOfPages = int(numberOfFriends / 18) + 1

    
    for i in range(numberOfPages):
        currentPage = i + 1
        friendListURL = f"https://www.brickplanet.com/profile/{userId}/view-friends?page={currentPage}"

        response = requests.get(friendListURL)
        soup = BeautifulSoup(response.text, "html.parser")
        allFriendsOnPage = soup.find_all("div", class_ = "col-4 col-lg-2 text-center")  # 6x3 players/friends on each page (18 players/friends per page)

        if not allFriendsOnPage and numberOfFriends > 0: # Makes sure that the friends are on the page. If they aren't, its prob b/c bp servers are down or you're rate limited
            print("Connection error. Either BP servers are down or you've sent too many requests. Program will resume in 10 seconds.")
            currentPage -= 1
            time.sleep(10)   
        
        for playerHTML in allFriendsOnPage:
            a_tag = playerHTML.find("a", class_ = "d-block truncate text-light")
            friendURL = a_tag["href"] # its just the URL to the player/friend cuz im too lazy to extract both the username and userid
            print(friendURL)

else:
    print("Player doesn't exist or the BP servers are down.")

print("\nScanning Complete")
