import pandas as pd

df_gmaps = pd.read_pickle("data/clean_gmaps.pkl")
avg_list = pd.read_pickle("data/avg_df_list_by_day.pkl")
flux_list = pd.read_pickle("data/flux_df_list_by_day.pkl")
min_max_list = pd.read_pickle("data/min_max_df_list_by_day.pkl")


def merge_gmaps_with_df(df):
    for column in df_gmaps.columns:
        df[column] = df_gmaps[column]
    return df


def merge_gmaps_with_all_dfs(df_list):
    return [merge_gmaps_with_df(df) for df in df_list]


test = merge_gmaps_with_all_dfs(avg_list)

print(test)
