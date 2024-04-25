import pandas as pd
import glob

# Get a list of all csv files in the target directory
files = glob.glob('tweets/*.csv')

# Create a list to hold all the dataframes
dfs = []

# Loop through the list of filepaths & read each one into a dataframe
for file in files:
    df = pd.read_csv(file)
    dfs.append(df)