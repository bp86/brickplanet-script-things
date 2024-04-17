import requests
from bs4 import BeautifulSoup

url = "https://www.brickplanet.com/shop/18443/spectral-egg" # Change this to the link of any RARE

content = requests.get(url).text
soup = BeautifulSoup(content, "html.parser")
divThing = soup.find_all("div", class_ = "text-2xl fw-semibold text-credits mb-1")

estimatedValue = divThing[0].text.strip() # RAP
volume = divThing[1].text.strip()
marketCap = divThing[2].text.strip()
