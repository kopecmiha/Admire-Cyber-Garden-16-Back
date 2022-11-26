import shutil
import uuid

from bs4 import BeautifulSoup
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20100101 Firefox/12.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-en,ru;q=0.8,en-us;q=0.5,en;q=0.3'}
req = requests.get("https://novyefoto.ru/fotos/Foto-Muzhchin-50-Let-Na-Prirode.html", headers=HEADERS)
base_html = req.text
soup = BeautifulSoup(base_html, 'html')
content = soup.find("div", attrs={"class": "post-content-inner"})
image_containers = content.findAll("center")
images_links = []
for container in image_containers:
    link = container.find("a").find("img")["src"]
    images_links.append(link)
final_links = []
for i in range(25):
    try:
        req = requests.get(images_links[i])
        if req.status_code == 200:
            with open("media/avatars/" + str(uuid.uuid4()) + ".jpg", "wb") as f:
                f.write(req.content)
    except:
        pass
