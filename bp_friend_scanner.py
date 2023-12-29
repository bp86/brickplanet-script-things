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
    pageNumber = 1
    
    friendListURL = "https://www.brickplanet.com/profile/" + str(userId) + "/view-friends?page=" + str(pageNumber)
    
    response = requests.get(friendListURL)
    soup = BeautifulSoup(response.text, "html.parser")
    
    allFriendsOnPage = soup.find_all("div", class_ = "col-4 col-lg-2 text-center")
    #numberOfFriends = soup.find("div", class_ = "text-2xl fw-semibold mb-2").text
    
    for i in range(len(allFriendsOnPage)):
        if i == 17: pageNumber += 1
            
    
    
    #col-4 col-lg-2 text-center
    #truncate  text-light 