import pandas as pd
import pickle


def get_average_parking_df():
    dfs_by_day = pd.read_pickle("data/dataframes_by_day.pkl")
    neighbourhood_list = pd.Index.unique(dfs_by_day[0].index)
    vehicles_list = ["bicycle", "cargo_bicycle", "moped", "scooter"]

    def get_average_one_day(df_day):
        df_avg = pd.DataFrame(
            {
                f"{vehicle}_avg": df_day.groupby("Wijk")[vehicle].mean()
                for vehicle in vehicles_list
            }
        )
        df_avg["day"] = df_day["day"].iloc[0]
        return df_avg

    def get_average_all_days(df_day_list):
        df_all_days = pd.DataFrame()
        for df_day in df_day_list:
            df_all_days = pd.concat([df_all_days, get_average_one_day(df_day)])
        return df_all_days

    return get_average_all_days(dfs_by_day)


def get_list_of_dfs_by_day(df):
    return [item[1] for item in df.groupby(["day"])]


def write_avg_data():
    df = get_average_parking_df()

    with open("data/avg_df.pkl", "wb") as file:
        pickle.dump(df, file)

    with open("data/avg_df_list_by_day.pkl", "wb") as file:
        pickle.dump(get_list_of_dfs_by_day(df), file)


write_avg_data()
