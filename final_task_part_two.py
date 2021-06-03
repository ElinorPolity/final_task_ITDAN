import pandas as pd
import numpy as np
import json
from bs4 import BeautifulSoup

data_tweets = pd.read_csv("tweets_metrics.csv",encoding = "ISO-8859-1")
data_tweets
data_tweets["hashtag_count"]=data_tweets["hashtags"].apply(lambda row: json.loads(row))
data_tweets["hashtag_count"]=data_tweets["hashtag_count"].apply(lambda row: len(row))
data_tweets["shared_geo_location"]=data_tweets["geo"].apply(lambda row: 0 if row!=row else 1)

#אפשר לעשות בצורת פונקציה והלכניס את הפונקציה זה יקצר משתי שורות לשורה 
data_tweets["device"]=data_tweets["source"].apply(lambda row : BeautifulSoup(row, 'html.parser').get_text())
data_tweets["device"]=data_tweets["device"].apply(lambda row : "pc" if row=="Twitter Web Client" else "mobile")

#לא מספיק טוב - צריך לכתוב פונקציה יותר מסודרת שתוריד את שאר הדברים הבעייתיים כמו "-" או סמיילי וכו 
data_tweets["word_count"]=data_tweets["text"].apply(lambda row : row.split(" "))
data_tweets["word_count"]=data_tweets["word_count"].apply(lambda row : len(row))
data_tweets["word_count"]