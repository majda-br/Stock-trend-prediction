import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from sentimentanalysis import weekly
import sentimentanalysis

# Extract Tesla stock data - tesla_historical_stock_prices
tesla = yf.download(tickers=['TSLA'],start = "2010-06-29",end = "2021-06-01",interval="1d") 

tesla_historical_stock_prices =tesla['Close']
print(tesla_historical_stock_prices.shape)

# Extract S&P 500 stock data variance - sp500_variance
sp500 = yf.download(tickers=['^GSPC'], start="1999-11-12", end="2024-01-01", interval="1d")
sp500_filtered = sp500[sp500.index.isin(tesla.index)]
sp500_extra = yf.download(tickers=['^GSPC'], start="1999-12-3", end="2000-01-01", interval="1d")
sp500_filtered = pd.concat([sp500_extra, sp500_filtered])
def calculate_variance(numbers):
    mean = sum(numbers) / len(numbers)
    squared_diffs = [(x - mean) ** 2 for x in numbers]
    variance = sum(squared_diffs) / len(numbers)
    return variance
sp500_historical_stock_prices = sp500_filtered['Close']
print(sp500_historical_stock_prices.shape)
sp500_variance = []
for i in range(20, len(sp500_historical_stock_prices)):
    sp500_variance.append(calculate_variance(sp500_historical_stock_prices[i-20:i]))

sp500_variance_df = pd.DataFrame({'S&P 500 Variance': sp500_variance}, index=sp500_historical_stock_prices[20:].index)
print('sp500',sp500_variance_df)

#Main competitors: Ford, GM, Toyota, Nissan
# Extract Ford stock data - ford_historical_stock_prices
ford = yf.download(tickers=['F'],start = "2000-01-01",end = "2024-01-01",interval="1d")['Close']
ford_historical_stock_prices = ford[ford.index.isin(tesla.index)]
print(ford_historical_stock_prices.shape)

# Extract General Motors stock data - gm_historical_stock_prices
gm = yf.download(tickers=['GM'],start = "2000-01-01",end = "2024-01-01",interval="1d")['Close']
gm_historical_stock_prices = gm[gm.index.isin(tesla.index)]
print('gm',gm_historical_stock_prices.shape)
#We observe that GM's data is missing for a period of time between 2010 and 2011, we need to fill in the missing data.
#We can use the average of the previous data points to fill in the missing data.
first_value = gm_historical_stock_prices[0]
print(first_value)
#We input the first value we have of General Motors stock price where we have missing data
#We need to add 100 first values to the tensor
addition = [first_value] * 100
gm_historical_stock_prices = pd.concat([pd.Series(addition), gm_historical_stock_prices])
#Now we set its index as Tesla's index
gm_historical_stock_prices.index = tesla_historical_stock_prices.index
print(gm_historical_stock_prices.shape)
print('gm',gm_historical_stock_prices)
plt.plot(gm_historical_stock_prices)
plt.show()


# Extract Toyota stock data - toyota_historical_stock_prices
toyota = yf.download(tickers=['TM'],start = "2000-01-01",end = "2024-01-01",interval="1d")['Close']
toyota_historical_stock_prices = toyota[toyota.index.isin(tesla.index)]
print(toyota_historical_stock_prices.shape)

# Extract Nissan stock data - nissan_historical_stock_prices
nissan = yf.download(tickers=['NSANY'],start = "2000-01-01",end = "2024-01-01",interval="1d")['Close']
nissan_historical_stock_prices = nissan[nissan.index.isin(tesla.index)]
print(nissan_historical_stock_prices.shape)

#Extract Tesla wikipedia page views over time - wiki_data_df['Tesla Motors[en]']
wiki_data = pd.read_excel('wiki.xlsx',header = 1)
wiki_data = wiki_data.set_index('DateTime')
wiki_data = wiki_data[wiki_data.index.isin(tesla.index)]
wiki_data_df = pd.DataFrame(wiki_data, columns=['Tesla Motors[en]'])
print(wiki_data_df)
plt.plot(wiki_data)
plt.show()
#it looks like we do not have data for a period of time between 2016 and 2017, we need to fill in the missing data.
#we can use the average of the previous data points to fill in the missing data
first_value = wiki_data_df['Tesla Motors[en]'][0]
print(first_value)
for i in range(len(wiki_data)):
    if wiki_data_df['Tesla Motors[en]'][i] == 0:
        wiki_data_df['Tesla Motors[en]'][i] = wiki_data_df['Tesla Motors[en]'][:i].mean()
plt.plot(wiki_data_df['Tesla Motors[en]'])
plt.show()

#now we create the df that contains all features
# Create a dataframe with all features
df = pd.DataFrame({
    'Tesla Stock Price': tesla_historical_stock_prices,
    'S&P 500 Variance': sp500_variance_df['S&P 500 Variance'],
    'Ford Stock Price': ford_historical_stock_prices,
    'GM Stock Price': gm_historical_stock_prices,
    'Toyota Stock Price': toyota_historical_stock_prices,
    'Nissan Stock Price': nissan_historical_stock_prices,
    'Tesla Wikipedia Page Views': wiki_data_df['Tesla Motors[en]']
})

print(df.head())
plt.plot(gm_historical_stock_prices)
plt.plot(ford_historical_stock_prices)
plt.plot(toyota_historical_stock_prices)
plt.plot(nissan_historical_stock_prices)
plt.plot(tesla_historical_stock_prices)
plt.plot(sp500_variance_df['S&P 500 Variance'])
plt.legend(['GM', 'Ford', 'Toyota', 'Nissan', 'Tesla', 'S&P 500 Variance'])
plt.show()


#Restructure these data into weekly data
features = pd.DataFrame(columns=['since', 'until', 'Tesla Stock Price', 'S&P 500 Variance', 'Ford Stock Price', 'GM Stock Price', 'Toyota Stock Price', 'Nissan Stock Price', 'Tesla Wikipedia Page Views','Sentiment'])
features['since'] = weekly['since']
features['until'] = weekly['until']
features['Sentiment'] = weekly['sentiment']
features['Previous Sentiment'] = features['Sentiment'].shift(1)


for i in range(0,len(features['since'])):
    weekly_tesla=[]
    weekly_sp500=[]
    weekly_ford=[]
    weekly_gm=[]
    weekly_toyota=[]
    weekly_nissan=[]
    weekly_wiki=[]
    for j in range(0,len(df['Tesla Stock Price'])):
        if df.index[j] >= features['since'][i] and df.index[j] < features['until'][i]:
            weekly_tesla.append(df['Tesla Stock Price'][j])
            weekly_sp500.append(df['S&P 500 Variance'][j])
            weekly_ford.append(df['Ford Stock Price'][j])
            weekly_gm.append(df['GM Stock Price'][j])
            weekly_toyota.append(df['Toyota Stock Price'][j])
            weekly_nissan.append(df['Nissan Stock Price'][j])
            weekly_wiki.append(df['Tesla Wikipedia Page Views'][j])
    
   

    #obtain the average of the scores
    if len(weekly_tesla) == 0:
        features['Tesla Stock Price'][i] = 0
    else:
        features['Tesla Stock Price'][i] = sum(weekly_tesla)/len(weekly_tesla)

    if len(weekly_sp500) == 0:
        features['S&P 500 Variance'][i] = 0
    else:
        features['S&P 500 Variance'][i] = sum(weekly_sp500)/len(weekly_sp500)
    
    if len(weekly_ford) == 0:
        features['Ford Stock Price'][i] = 0
    else:
        features['Ford Stock Price'][i] = sum(weekly_ford)/len(weekly_ford)
    
    if len(weekly_gm) == 0:
        features['GM Stock Price'][i] = 0
    else:
        features['GM Stock Price'][i] = sum(weekly_gm)/len(weekly_gm)
    
    if len(weekly_toyota) == 0:
        features['Toyota Stock Price'][i] = 0
    else:
        features['Toyota Stock Price'][i] = sum(weekly_toyota)/len(weekly_toyota)

    if len(weekly_nissan) == 0:
        features['Nissan Stock Price'][i] = 0
    else:
        features['Nissan Stock Price'][i] = sum(weekly_nissan)/len(weekly_nissan)

    if len(weekly_wiki) == 0:
        features['Tesla Wikipedia Page Views'][i] = 0
    else:
        features['Tesla Wikipedia Page Views'][i] = sum(weekly_wiki)/len(weekly_wiki)


# Add previous week's price as a feature
features['Previous Week Tesla Stock Price'] = features['Tesla Stock Price'].shift(1)
#eliminate the first row of data
features = features[2:]
#Divide the data into training and testing data
features_train = features[features['since'] < '2020-01-01']
features_test = features[features['since'] >= '2020-01-01']
#Convert the data into csv files
features_train.drop(columns=['since', 'until']).to_csv('features_train.csv')
features_test.drop(columns=['since', 'until']).to_csv('features_test.csv')
print(features)

