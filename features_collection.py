import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Extract Tesla stock data - tesla_historical_stock_prices
tesla = yf.download(tickers=['TSLA'],start = "2000-01-01",end = "2024-01-01",interval="1d") 

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
print(gm_historical_stock_prices.shape)

# Extract Toyota stock data - toyota_historical_stock_prices
toyota = yf.download(tickers=['TM'],start = "2000-01-01",end = "2024-01-01",interval="1d")['Close']
toyota_historical_stock_prices = toyota[toyota.index.isin(tesla.index)]
print(toyota_historical_stock_prices.shape)

# Extract Nissan stock data - nissan_historical_stock_prices
nissan = yf.download(tickers=['NSANY'],start = "2000-01-01",end = "2024-01-01",interval="1d")['Close']
nissan_historical_stock_prices = nissan[nissan.index.isin(tesla.index)]
print(nissan_historical_stock_prices.shape)

#Extract Tesla wikipedia page views over time - wiki_data_df['Tesla Motors[en]']
wiki_data = pd.read_excel(r"D:\iCloudDrive\Documents\BERKELEY\242MACHINELEARNING\Project\wiki.xlsx",header = 1)
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
