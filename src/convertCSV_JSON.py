import csv
import json
import pandas as pd


df = pd.read_csv('../data/inflation.csv')
df.to_json('../data/inflation.json', orient='records', indent=4)



