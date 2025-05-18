import pandas as pd
import json
# https://stackoverflow.com/questions/66831999/how-to-import-csv-as-a-pandas-dataframe
import os

csv_file = os.path.join('data','superstore_final_dataset (1).csv')

df = pd.read_csv(csv_file, encoding='ISO-8859-1')  # alternative encoding with special characters

print(df.head())