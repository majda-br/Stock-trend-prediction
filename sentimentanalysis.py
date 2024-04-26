from vaderSentiment import SentimentIntensityAnalyzer
from tweets import tweets_df
import pandas as pd
from datetime import datetime, date, timedelta
import math
import matplotlib.pyplot as plt

def split_dates(since, until):
    
    step = timedelta(7)
    start_date = datetime.strptime(since, '%Y-%m-%d').date()
    end_date = datetime.strptime(until, '%Y-%m-%d').date()
    
    dates = []
    while (start_date <= end_date):
        if start_date + step + timedelta(1) > end_date:
            dates.append((str(start_date), str(end_date)))
        else:
            dates.append((str(start_date), str(start_date + step)))
        start_date += step + timedelta(1)
    
    return dates

analyzer = SentimentIntensityAnalyzer()
scores=[]
for sentence in tweets_df['Content']:
    vs = analyzer.polarity_scores(sentence)
    scores.append(vs['compound'])

tweets_df['sentiment'] = scores
tweets_df

#create a new dataframe that contains a column with the 'since' date, another column with the 'until' date, and a third column with the avergae sentiment of tweets in that period
weekly = pd.DataFrame(columns=['since', 'until', 'sentiment'])
s=[]
u=[]
for i in range(len(split_dates('2010-06-29', '2021-06-01'))):
    
    s.append(split_dates('2010-06-29', '2021-06-01')[i][0])
    u.append(split_dates('2010-06-29', '2021-06-01')[i][1])
weekly['since'] = pd.to_datetime(s)
weekly['until'] = pd.to_datetime(u)
weekly_count=[0]*len(weekly['since'])
#Now we average the scores for each week
for i in range(0,len(weekly['since'])):
    weekly_score=[]
    for j in range(0,len(tweets_df['Date'])):
        if tweets_df['Date'][j] >= weekly['since'][i] and tweets_df['Date'][j] < weekly['until'][i]:
            weekly_score.append(tweets_df['sentiment'][j])
            weekly_count[i]=weekly_count[i]+1
    #obtain the average of the scores
    if len(weekly_score) == 0:
        weekly['sentiment'][i] = 0
    else:
        weekly['sentiment'][i] = sum(weekly_score)/len(weekly_score)
#plot a histogram of the sentiment values
plt.plot(weekly['sentiment'])
plt.show
