import pandas as pd
import glob

# Get a list of all csv files in the target directory
files = glob.glob('*.csv')


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
