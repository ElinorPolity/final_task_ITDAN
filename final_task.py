import requests
from bs4 import BeautifulSoup
import pandas as ps

url = "https://kualastyle.com/collections/שולחנות-צד-שולחנות-קפה"
response = requests.get(url)
if response.status_code == 200:
    print("Success")
else:
    print("Failure")
    
soup = BeautifulSoup(response.content, 'html.parser')

#df=ps.DataFrame().columns("prodName","category","price","Image_url","description")
category="שולחנות קפה"
another_row=list()
tags = soup.find_all(class_="monserrat")
print(tags)
for tag in tags:
    tag=tag.get('href')
    url_page=url+tag
    response1=requests.get(url_page)
    if not response.status_code == 200:
        results_page = BeautifulSoup(response.content, 'html.parser')
        prodName=results_page.find("h1", class_="page-title monserrat").get_text()
        price=results_page.find().get_text()
        Image_url=results_page.find().get('href')
        description=results_page.find().get_text()
        Size=results_page.find().get_text()
        another_row=[prodName,price,Image_url,description,Size]
        df.append(another.row)