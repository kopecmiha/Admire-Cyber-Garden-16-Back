import shutil
import uuid

from bs4 import BeautifulSoup
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20100101 Firefox/12.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-en,ru;q=0.8,en-us;q=0.5,en;q=0.3'}
req = requests.get("https://uhd.name/54791-zhenskoe-lico-anfas.html", headers=HEADERS)
base_html = req.text
soup = BeautifulSoup(base_html, 'html')
content = soup.find("div", attrs={"vp-desc full-text clearfix"})
image_containers = content.findAll("a")
i=0
for container in image_containers:
    i+=1
    print(i)
    link = container["href"]
    try:
        req = requests.get(link)
        if req.status_code == 200:
            with open("media/avatars/" + str(uuid.uuid4()) + ".jpg", "wb") as f:
                f.write(req.content)
    except:
        pass
