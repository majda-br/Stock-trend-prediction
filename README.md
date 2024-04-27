in the features_collection file we obtain a dataframe that contains 

    'Tesla Stock Price': tesla_historical_stock_prices,
    
    'S&P 500 Variance': sp500_variance_df['S&P 500 Variance'],
    
    'Tesla Wikipedia Page Views': wiki_data_df['Tesla Motors[en]']
    
    Tesla's competitors:
    
      'Ford Stock Price': ford_historical_stock_prices,
      
      'GM Stock Price': gm_historical_stock_prices,
      
      'Toyota Stock Price': toyota_historical_stock_prices,
      
      'Nissan Stock Price': nissan_historical_stock_prices,


In the tweets.py file we read the tweets from the files, and in sentimentanalysis.py we develop the sentiment analysis by using the VADER library, which gives a compund score for each tweet based on the words in it. (https://github.com/cjhutto/vaderSentiment/tree/master/vaderSentiment)

The we add these sentiment scores as a weekly average in the features_collection.py file, where the datframe features contains all the features for each week for the years 2010-2021.
    
