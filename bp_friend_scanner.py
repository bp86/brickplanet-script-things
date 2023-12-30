import requests
from bs4 import BeautifulSoup
import time


userId = 6731


def checkStatusCode(url):
    response = requests.get(url)
    return response.status_code >= 200 and response.status_code <= 400

def checkIfUserExists(userId):
    profileURL = "https://www.brickplanet.com/profile/" + str(userId)

    response = requests.get(profileURL)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("title").text
    
    return checkStatusCode(profileURL) and not "Players" in title


if checkIfUserExists(userId):
    currentPage = 1
    
    friendListURL = "https://www.brickplanet.com/profile/" + str(userId) + "/view-friends?page=" + str(currentPage)
    
    response = requests.get(friendListURL)
    soup = BeautifulSoup(response.text, "html.parser")

    friendString = soup.find("div", class_ = "text-2xl fw-semibold mb-2").text # Example string: "86's Friends (57)"
    characterPosition = 0 # The position of the "(" in "friendString"
    numberOfFriends = ""

    numberOfPages = 0


    # Finds the number between the parethesis in "friendString"
    for i in range(len(friendString) - 2, -1, -1): # length of string - 2 because we dont need the last charcter ")"
        if friendString[i] == "(":
            characterPosition = i
            break

    # Isolates the numbers between the parenthesis in "friendString"
    for i in range(characterPosition + 1, len(friendString) - 1, 1):
        numberOfFriends += friendString[i]

    numberOfPages = int(int(numberOfFriends) / 18) + 1

    
    for i in range(numberOfPages):
        currentPage = i + 1
        friendListURL = "https://www.brickplanet.com/profile/" + str(userId) + "/view-friends?page=" + str(currentPage)

        response = requests.get(friendListURL)
        soup = BeautifulSoup(response.text, "html.parser")
        allFriendsOnPage = soup.find_all("div", class_ = "col-4 col-lg-2 text-center")  # 6x3 players/friends on each page (18 players/friends per page)
        
        for playerHTML in allFriendsOnPage:
            a_tag = playerHTML.find("a", class_ = "d-block truncate text-light")
            friendURL = a_tag["href"] # its just the URL to the player/friend cuz im too lazy to extract both the username and userid
            print(friendURL)
