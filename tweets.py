import pandas as pd
import glob

# Get a list of all csv files in the target directory
files = glob.glob('tweets/*.csv')


# Create an empty list to store the dataframes
dfs = []
# Loop through the list of filepaths & read each one into a dataframe
for file in files:
    i=0
    df = pd.read_csv(file)
    dfs.append(df)

business_df = dfs[0]
cnbc_df = dfs[1]
elonmusk_df = dfs[2]
ft_df = dfs[3]
teslageneral_df = dfs[4]
reuters_df = dfs[5]
tesla_df = dfs[6]
wsj_df = dfs[7]

# Concatenate all data into one DataFrame
tweets_df = pd.concat(dfs, ignore_index=True)

#Print highest date in the df
#print(tweets_df['Date'])

#Check if every element in the 'Date' column is a datetime object
#print(tweets_df['Date'].apply(type).eq(pd.Timestamp).all())
#We have some elements that are not datetime objects
#We want to check which indexes they are located in

#check which indexes do not have the format "%Y-%m-%d"

sentences = []
for i in range(len(tweets_df['Date'])):
    if type(tweets_df['Date'][i]) != str:
        distintos.append(tweets_df['Date'][i])
    elif type(tweets_df['Date'][i]) == str:
        if tweets_df['Date'][i][4] != '-':
            sentences.append(i)
        elif tweets_df['Date'][i][7] != '-':
            sentences.append(i)

#obtain a dataframe with the indexes that have the wrong format stored in sentences
wrong_dates = tweets_df.loc[sentences]

#We see that these tweets are part of the previous ones, containing only a youtube link and the same hashtags. For this reason, we wliminate fro the complete dataset these indexes which do not add any value to the sentiment analysis
tweets_df = tweets_df.drop(sentences)
#Restablish the indexes
tweets_df = tweets_df.reset_index(drop=True)

#We convert the 'Date' column to datetime objects
tweets_df['Date'] = pd.to_datetime(tweets_df['Date'])
#We sort the dataframe by date
tweets_df = tweets_df.sort_values(by='Date')
#We reset the indexes
#Delete the rows that have the same text and date
tweets_df = tweets_df.drop_duplicates(subset=['Content', 'Date'])
tweets_df = tweets_df.reset_index(drop=True)

#I calculate how many tweets per each day are in the dataset
#print(tweets_df['Date'].value_counts().sort_index())



###CLEANING THE CONTENT OF THE TWEETS ###
tweets_df
from bs4 import BeautifulSoup

for i in range(len(tweets_df['Content'])):
    html_doc = tweets_df['Content'][i]
    soup = BeautifulSoup(html_doc, 'html.parser')
    text = soup.get_text()
    tweets_df['Content'][i]=text
#Manually cleaned up newline tag \n and tab tag \t.
tweets_df.replace(to_replace=['<r>','<', '>','\n','<p>','\t','#'], value=' ', regex=True, inplace=True) 
#eliminate the urls in the tweets
import re
def remove_urls(text, replacement_text=' '):
    # Define a regex pattern to match URLs
    url_pattern = re.compile(r'http?://\S+|www\.\S+')
 
    # Use the sub() method to replace URLs with the specified replacement text
    text_without_urls = url_pattern.sub(replacement_text, text)
 
    return text_without_urls

def remove_mentions(text,replacement_text = ' '):
    
    pattern = re.compile(r'@\S+')
    text_without_mentions = pattern.sub(replacement_text, text)
    return text_without_mentions
#we remove the urls from each tweet
tweets_df['Content'][0]
tweets_df['Content'] = tweets_df['Content'].apply(remove_urls)
tweets_df['Content'] = tweets_df['Content'].apply(remove_mentions)
#tweets_df['Content'] = tweets_df['Content'].str.replace('http\S+|www.\S+', '', case=False)
tweets_df['Content'][0]
