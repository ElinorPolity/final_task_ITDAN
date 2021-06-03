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
#לפונקציה הזאת נקרא בשביל לקבל את הדטא פריים שלנו
def get_the_df(soup):
    address=list()
    df=ps.DataFrame(columns=["prodName","Category","price","Image_url","description","Size"])
    tag_b =  soup.findAll("figure", class_ = "product-list-item-thumbnail")
    for tag in tag_b:
        children = tag.find("a")
        address.append("https://kualastyle.com" +  children.get("href"))
    #עד לפה זה מה שעשיתם
    #נהפוך את הרשימה של הכתובות לדטא פריים
    address_chart = ps.DataFrame({"address":address})
    #נבצע עליו את הפונקציה של אפלאי - הפונקציה בתוך האפלאי נמצאת בהמשך
    tuple_of_tags=address_chart["address"].apply(find_the_tags)
    #בשורה הקודמת קבלנו טאפל של נתונים בתוך עמודה אחת של דטא פריים. נרצה להפריד את הנתונים בטאפל כדי להכניס אותם לעמודות זה מה שקורה בשורות הבאות
    for row in tuple_of_tags:
        df_length = len(df)
        df.loc[df_length] = row
    return df
#פונקציה זאת אחראית לשלוף את התגיות מהרשת ולשלוף את המידע אותו אנחנו צריכים
def find_the_tags(address):
    response1=requests.get(address)
    Category="שולחנות-צד-שולחנות-קפה"
    if response.status_code == 200:
        results_page = BeautifulSoup(response1.content, 'html.parser')
        prodName=results_page.find("h1", class_="page-title").get_text()
        prodName=prodName[prodName.find("|")+1:]
        price=results_page.find("span", class_="product-price-minimum money").get_text().strip()
        Image_url=results_page.find_all("img")[5].get("src")
        #פה נתקלתי בבעיה מכיוון שכותבי האתר עשו בעיה וכתבו את התגיות שונות עבור כל תיאור. הייתי צריכה לחזור לאב הקדמון ולרדת ממנו לילדים בשביל לגשת לכל התגיות המתאימות
        description_father=results_page.find_all("div" ,class_="easyslider-content-wrapper")
        #הילד הראשון היה תגית התיאור
        description = description_father[0].findChildren()[0].get_text().strip()
        #פה אני מטפלת בתגיות עבור דפים שנכתבו שונה, במקרה זה התיאור היה בתגית 4
        if description=="":
            description=description_father[0].findChildren()[4].get_text()
        Size=description_father[0].findChildren("ul")[0].get_text()
        Size=Size.replace("\n"," ")
        return prodName,Category,price,Image_url,description,Size
    else:
        return "NaN","NaN","NaN","NaN","NaN","NaN"
    
if __name__ == "__main__":
    soup=get_soup()
    address_chart=get_the_df(soup)
    address_chart
