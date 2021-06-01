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

tag_b =  soup.findAll("figure", class_ = "product-list-item-thumbnail")
i = 0
df=ps.DataFrame(columns=["prodName","price","Image_url"])
another_row=list()
for tag in tag_b:
    children = tag_b[i].find("a")
    address =  "https://kualastyle.com" +  children.get("href") 
    response1=requests.get(address)
    if response.status_code == 200:
        results_page = BeautifulSoup(response1.content, 'html.parser')
        prodName=results_page.find_all("h1", class_="page-title")[0].get_text()
        prodName=prodName[prodName.find("|")+1:]
        price=results_page.find_all("span", class_="product-price-minimum money")[0].get_text().strip()
        Image_url=soup.find_all("img",class_="only-image")[i*2].get("src").strip()
        description=results_page.find_all("span" ,style="text-align: right;")
        another_row=[prodName,price,Image_url]
        df_length = len(df)
        df.loc[df_length] = another_row
    i = i + 1
print(df)
