import requests
from bs4 import BeautifulSoup

either = requests.get("https://either.io/")
either_html = either.text
either_soup = BeautifulSoup(either_html, "html.parser")

print(either_soup.find("h3", {"class": "preface"}).string)
print(either_soup.find_all("span", {"class": "option-text"})[0].string)
print(either_soup.find_all("span", {"class": "option-text"})[1].string)