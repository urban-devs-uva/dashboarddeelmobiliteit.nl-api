# I need this for google maps data
import pandas as pd

df = pd.read_pickle("data/flux_df_list_by_day.pkl")[0]
neighbourhood_list = list(df.index)
pd.to_pickle(neighbourhood_list, "data/neighbourhood_list.pkl")
