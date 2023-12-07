import pandas as pd
import pickle


def get_min_max_vehicles_df():
    dfs_by_day = pd.read_pickle("data/dataframes_by_day.pkl")
    neighbourhood_list = pd.Index.unique(dfs_by_day[0].index)
    vehicles_list = ["bicycle", "cargo_bicycle", "moped", "scooter"]

    def get_min_max_one_neighbourhood(df_neighbourhood):
        min_max_dict = {}
        for vehicle in vehicles_list:
            min_value = df_neighbourhood[vehicle].min()
            max_value = df_neighbourhood[vehicle].max()
            min_max_dict[f"{vehicle}_min"] = min_value
            min_max_dict[f"{vehicle}_max"] = max_value
            min_max_dict[f"{vehicle}_diff"] = max_value - min_value

        return min_max_dict

    def get_min_max_one_day(df_day):
        min_max_data = {
            neighbourhood: get_min_max_one_neighbourhood(df_day.loc[neighbourhood])
            for neighbourhood in neighbourhood_list
        }
        min_max_df = pd.DataFrame(min_max_data).T
        min_max_df["day"] = df_day["day"].iloc[0]
        return min_max_df

    def get_min_max_all_days(df_day_list):
        min_max_all_days = pd.DataFrame()
        for df_day in df_day_list:
            min_max_all_days = pd.concat(
                [min_max_all_days, get_min_max_one_day(df_day)]
            )
        return min_max_all_days

    return get_min_max_all_days(dfs_by_day)


def get_list_of_dfs_by_day(df):
    return [item[1] for item in df.groupby(["day"])]


def write_min_max_data():
    min_max_df = get_min_max_vehicles_df()

    with open("data/min_max_df.pkl", "wb") as file:
        pickle.dump(min_max_df, file)

    with open("data/min_max_df_list_by_day.pkl", "wb") as file:
        pickle.dump(get_list_of_dfs_by_day(min_max_df), file)


write_min_max_data()
