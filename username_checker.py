import requests
from bs4 import BeautifulSoup
from time import sleep

characters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "_"]
availableUsernames = []
usernameLength = 2

if usernameLength < 2:
    usernameLength = 2

if usernameLength > 20:
    usernameLength = 20


def addCharacter(username: str) -> str:
    usernames = []
    
    for char in characters:
        if len(username) == usernameLength - 1:
            usernames.append(username + char)
        else:
            usernames += addCharacter(username + char)

    return usernames
    

for char in characters:
    url = "https://www.brickplanet.com/api/register/check-username-availability?username="
    usernames = addCharacter(char)
    
    for username in usernames:
        response = requests.get(url + username)
        print(username)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text()

            if "taken:false" in text:
                availableUsernames.append(username)
        
        else:
            print("Error, likely timeout.\nScan will resume in 30 seconds.")
            sleep(30)

print(availableUsernames)
print(len(availableUsernames))
