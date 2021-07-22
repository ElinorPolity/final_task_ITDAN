import pandas as pd
import numpy as np
import json
from bs4 import BeautifulSoup

data_tweets = pd.read_csv("tweets_metrics.csv",encoding = "ISO-8859-1")

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

data_tweets["created at"]=data_tweets["created at"].apply(lambda row : str(row))
data_tweets["Year"]=data_tweets["created at"].apply(lambda row : "" if row == "nan" else row[len(row)-5:])
data_tweets["Month"]=data_tweets["created at"].apply(lambda row : "" if row == "nan" else row[4:7])

data_tweets["user_id"]=data_tweets["user_id"].apply(lambda row : str(row)) #change user_id column to str
data_tweets["user_year_month"]=data_tweets[['user_id', 'Year', 'Month']].agg('-'.join, axis=1) #join the columns user_id,Year,Month together in 0ne column in the data_tweets table
data_tweets["monthly_tweet_count"]=data_tweets.groupby(by="user_year_month")["user_year_month"].transform('count') #count the tweets by the "user_year_month" column
data_tweets["user_id"]=data_tweets["user_id"].apply(lambda row : np.float64(row)) #change back the user_id to float64
data_tweets["monthly_hashtag_count"]=data_tweets.groupby(by="user_year_month")["hashtag_count"].transform('sum')  #sum the hashtags by the "user_year_month" column
#elinor code for question 3 
data_tweets["device"]=data_tweets["device"].apply(lambda row :1 if row=="mobile" else 0)#change mobile to one
data_tweets["monthly_moblie_percent_tweets"]=data_tweets.groupby(by="user_year_month")["device"].transform('sum')#count by mounth and year
data_tweets["monthly_moblie_percent_tweets"]=data_tweets.apply(lambda row: (row.monthly_moblie_percent_tweets/row.monthly_tweet_count)*100 ,axis=1)#ture to precent
data_tweets["device"]=data_tweets["device"].apply(lambda row :"mobile" if row==1 else "pc")#change the rows back to pc and mobile

data_tweets["monthly_retweets_count"]=data_tweets.groupby(by="user_year_month")["retweet_count"].transform('sum')

data_tweets["monthly_location_sharing_count"]=data_tweets.groupby(by="user_year_month")["shared_geo_location"].transform('sum')#sum

data_tweets["is_quote_status"] = data_tweets["is_quote_status"].apply(lambda row :1 if row else 0)
data_tweets["monthly_quote_count"]=data_tweets.groupby(by="user_year_month")["is_quote_status"].transform('sum')
data_tweets["is_quote_status"] = data_tweets["is_quote_status"].apply(lambda row :True if row==1 else False)

data_tweets["number_of_total_tweets"]=data_tweets.groupby("user_id")["tweet_id"].transform('count')
data_tweets["monthly_percent_tweets_from_total"]=data_tweets.apply(lambda row: (row.monthly_tweet_count/row.number_of_total_tweets)*100,axis=1)
data_tweets.drop("number_of_total_tweets",axis=1)

#incerst all the coulmns that we need from data tweets to our new data frame and drop all the duplicated rows.
tweets_monthly_summery[["user_id","Year","Month","Tweet_count","Hashtag_count","Percent_mobile","Retweet_count","Location_sharing_count","Quote_count","Monthly_tweets_percent"]]=data_tweets[["user_id","Year","Month","monthly_tweet_count","monthly_hashtag_count","monthly_moblie_percent_tweets","monthly_retweets_count","monthly_location_sharing_count","monthly_quote_count","monthly_percent_tweets_from_total"]]
tweets_monthly_summery=tweets_monthly_summery.drop_duplicates()
tweets_monthly_summery=tweets_monthly_summery.reset_index()

#hists and plots
data_tweets["number_of_tweets"]=data_tweets.groupby("user_id")["user_id"].transform("count")
data_tweets.head(20)
data_temp=pd.DataFrame(columns=["user_id","number_of_tweets"])
data_temp[["user_id","number_of_tweets"]]=data_tweets[["user_id","number_of_tweets"]]
data_temp=data_temp.drop_duplicates().reset_index()
data_temp["number_of_tweets"].hist()

#units of followers showing in thousdns
x=data_users["followers_count"]/1000
x.hist()

#units of followers shown is in miliions
data_users.sort_values('followers_count',ascending = False).head(10).plot(x="name",y="followers_count",kind="bar")

data_users.plot(x='followers_count',y="statuses_count",kind="scatter")

X = data_users["followers_count"].values.reshape(-1, 1) # values converts it into a numpy array
Y = data_users["statuses_count"].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(X, Y)  # perform linear regression
Y_pred = linear_regressor.predict(X)
plt.scatter(X, Y)
plt.plot(X, Y_pred, color='red')
plt.show()

data_users.plot(x='friends_count',y="statuses_count",kind="scatter")

X = data_users['friends_count'].values.reshape(-1, 1) # values converts it into a numpy array
Y = data_users["statuses_count"].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(X, Y)  # perform linear regression
Y_pred = linear_regressor.predict(X)
plt.scatter(X, Y)
plt.plot(X, Y_pred, color='red')
plt.show()








