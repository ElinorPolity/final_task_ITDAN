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
#שאלה 2
#עשיתי אנקודינג לפי יוטיאף כי במה שאלינור עשתה יצא לי הרבה ג'יבריש#
data_users = pd.read_csv("users_metrics.csv",encoding = "utf-8")

data_users["Num_words_in_desc"] = data_users["description"].apply(lambda row: str(row))
data_users["Num_words_in_desc"] = data_users["Num_words_in_desc"].apply(lambda row: 0 if row == "nan" else len(row.split(" ")))
#במטלה כתוב להוסיף איז-סלב אם יש לו מעל מספר עוקבים ואני הוספתי סטרינג ריק אם לא . אני לא בטוח שזה עונה לדרישה
data_users["is_celeb"] = data_users["followers_count"].apply(lambda row : 1 if row>100000 else 0)
#מפה החלק של אלינור
data_users["user_id"]=data_users["user_id"].apply(lambda row : np.float64(row))
def number_of_tweets_collected(user_id):
    
    index=data_tweets["user_id"]==user_id
    return index.value_counts()[1]

data_users["collected_tweets"]=data_users["user_id"].apply(lambda row : number_of_tweets_collected(row))
data_users["collected_tweets_percent"]=data_users.apply(lambda row : (row.collected_tweets/row.statuses_count)*100 ,axis=1)

#שאלה 3
#בשאלה 3 נתקלתי בקושי שלא הצלחתי לפתור. צריך לעשות דטא פריים חדש של הקבצים. את כל החיבור לקבוצות עשיתי על הטבלה המקורית של הציוצים. חשבתי שאולי אחר כך יהיה אפשר לחלץ את המידע בצורה מסודרת
tweets_monthly_summery=pd.DataFrame(columns = ["user_id","Year","Month","Tweet_count","Hashtag_count","Percent_mobile","Retweet_count","Location_sharing_count","Quote_count"])
tweets_monthly_summery["user_id"]=data_tweets["user_id"]

# הקוד של אביב לתחילת שאלה 3
data_tweets["user_id"]=data_tweets["user_id"].apply(lambda row : str(row)) #change user_id column to str
data_tweets["user_year_month"]=data_tweets[['user_id', 'Year', 'Month']].agg('-'.join, axis=1) #join the columns user_id,Year,Month together in 0ne column in the data_tweets table

data_tweets["monthly_tweet_count"]=data_tweets.groupby(by="user_year_month")["user_year_month"].transform('count') #count the tweets by the "user_year_month" column

data_tweets["user_id"]=data_tweets["user_id"].apply(lambda row : np.float64(row)) #change back the user_id to float64
data_tweets.loc[(data_tweets['user_id'] == 13679) & (data_tweets['Month'] == 'Aug')].head(56)# check the table to see if the clomun "monthly_tweet_count" is ok

data_tweets.groupby(['user_id','Year','Month'])['Month'].count() # using the groupby function to see if the data is correct

data_tweets["monthly_hashtag_count"]=data_tweets.groupby(by="user_year_month")["hashtag_count"].transform('sum')  #sum the hashtags by the "user_year_month" column

data_tweets.loc[(data_tweets['user_id'] == 13679) & (data_tweets['Month'] == 'Nov')].head(20) # check the table to see if the clomun "monthly_hashtag_count" is ok

data_tweets.groupby(['user_id','Year','Month'])['hashtag_count'].sum() # using the groupby function to see if the data is correct
data_tweets["created at"]=data_tweets["created at"].apply(lambda row : str(row))
data_tweets["Year"]=data_tweets["created at"].apply(lambda row : "" if row == "nan" else row[len(row)-5:])
data_tweets["Month"]=data_tweets["created at"].apply(lambda row : "" if row == "nan" else row[4:7])
data_tweets["Year"]=data_tweets["created at"].apply(lambda row : "" if row == "nan" else row[len(row)-5:])
data_tweets["Tweet_count"]=data_tweets.groupby("user_id")["Month"].transform("count")

#אני לא יודעת אם השלב הבא צריך לבדוק את זה
data_tweets["Hashtag_count"]=data_tweets.groupby("user_id")["Month","hashtag_count"].transform("sum")["hashtag_count"]
