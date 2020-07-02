from bs4 import BeautifulSoup
import requests

kanto_routes = ["Kanto_Route_{}".format(i + 1) for i in range(30)]
for i in kanto_routes:
    page = requests.get("https://bulbapedia.bulbagarden.net/wiki/{}".format(i))
    soup = BeautifulSoup(page.content, "html.parser")
    a = soup.find("span", id = "Pok.C3.A9mon").find_next("table")
    b = a.find_all("tr")
    for i in b:
        c = i.find_all("span")
        for j in c:
            d = j.get_text()
            print(d)
    # c = b.find_all("tr")
    # print(c)
    # d = c.find_all("td")
    # print(d)
    break
