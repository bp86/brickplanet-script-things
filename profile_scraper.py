from bs4 import BeautifulSoup
import requests


userId = 6969 # Change this your desired UserId

url = f"https://www.brickplanet.com/profile/{userId}"


response = requests.get(url)

if response.status_code >= 200 and response.status_code <= 400: 
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    if not "Players" in soup.find("title").text:

        username = soup.find("title").text.split("|")[0].strip()
        bio = "N/A"
        netWorth = "N/A"
        rank = "N/A"

        userStats = []
        level = "N/A"
        lastSeen = "N/A"
        joinDate = "N/A"
        profileViews = "N/A"
        forumPosts = "N/A"


        try: 
            bio = soup.find("div", class_ = "card text-sm card-body mb-4").text.strip()
            valueInfo = soup.find("span", class_ = "text-credits").text.strip().split("#")
            netWorth = valueInfo[0].split("\n")[0]
            rank = valueInfo[1]
        except AttributeError:
            pass
        
        try:
            for stat in soup.find("div", class_ = "d-flex flex-column gap-1 text-sm card card-body mb-4"):
                userStats.append(stat.text.strip())

            level = userStats[1]
            lastSeen = userStats[3]
            joinDate = userStats[5]
            profileViews = userStats[7]
            forumPosts = userStats[9]
        except TypeError:
            print("This user is banned.\n")
            pass
        
        
        print(f"Username: {username} \nBio: {bio} \nNetWorth: {netWorth} \nRank: {rank}")
        print(f"{level} \n{lastSeen} \n{joinDate} \n{profileViews} \n{forumPosts}")

    else:
        print("Player doesn't exist")
    
else:
    print("You've sent too many requests OR the BP servers are down.")
