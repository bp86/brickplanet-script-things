'''

INSTRUCTIONS:

This was used by me (86) to find the remaining 2-character usernames on Brickplanet.

Running the program is a waste of time. The only thing of value is this: https://www.brickplanet.com/api/register/check-username-availability?username=PlaceHolder

'''


import requests
from bs4 import BeautifulSoup

characters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "_"]
availableUsernames = []

for char1 in characters:
  for char2 in characters:
    url = "https://www.brickplanet.com/api/register/check-username-availability?username="
    username = char1 + char2

    response = requests.get(url + username)
    print(username)

    if response.status_code == 200:
      soup = BeautifulSoup(response.text, "html.parser")
      text = soup.get_text()
      requiredText = 'ken":fal'  # text its looking for: taken":false

      # was shortened to save processing power

      if requiredText in text:
        availableUsernames.append(username)


print(availableUsernames)
print(len(availableUsernames))
