import requests
from bs4 import BeautifulSoup
import pandas as ps

def get_soup():    
    url = "https://kualastyle.com/collections/שולחנות-צד-שולחנות-קפה"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    else:
        return "Failure"
    
def get_the_df(soup):
    address=list()
    df=ps.DataFrame(columns=["prodName","Category","price","Image_url","description","Size"])
    tag_b =  soup.findAll("figure", class_ = "product-list-item-thumbnail")
    for tag in tag_b:
        children = tag.find("a")
        address.append("https://kualastyle.com" +  children.get("href"))
    address_chart = ps.DataFrame({"address":address})
    tuple_of_tags=address_chart["address"].apply(find_the_tags)
    for row in tuple_of_tags:
        df_length = len(df)
        df.loc[df_length] = row
    return df

def find_the_tags(address):
    response1=requests.get(address)
    Category="שולחנות-צד-שולחנות-קפה"
    if response.status_code == 200:
        results_page = BeautifulSoup(response1.content, 'html.parser')
        prodName=results_page.find("h1", class_="page-title").get_text()
        prodName=prodName[prodName.find("|")+1:]
        price=results_page.find("span", class_="product-price-minimum money").get_text().strip()
        Image_url=results_page.find_all("img")[5].get("src")
        description_father=results_page.find_all("div" ,class_="easyslider-content-wrapper")
        description = description_father[0].findChildren()[0].get_text().strip()
        if description=="":
            description=description_father[0].findChildren()[4].get_text()
        Size=description_father[0].findChildren("ul")[0].get_text()
        Size=Size.replace("\n"," ")
        #.findChildren("li") 
        return prodName,Category,price,Image_url,description,Size

if __name__ == "__main__":
    soup=get_soup()
    address_chart=get_the_df(soup)
    address_chart
