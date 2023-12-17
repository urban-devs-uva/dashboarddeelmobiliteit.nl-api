import pandas as pd

df_gmaps = pd.read_csv("data/neighbourhood_data_new.csv")
df_gmaps.drop("Unnamed: 0", axis=1, inplace=True)
df_gmaps.set_index("Wijk", inplace=True)

df_gmaps.to_pickle("data/clean_gmaps.pkl")
df_gmaps = pd.read_pickle("data/clean_gmaps.pkl")
print(df_gmaps)
