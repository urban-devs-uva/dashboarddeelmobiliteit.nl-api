import pandas as pd
import math
import pickle


def get_merged_parking_data():
    neighbourhood_list = pd.read_csv("INDELING_WIJK.csv", sep=";")["Wijk"]

    # this just returns a list of all 746 scraped dataframes, each one for each hour from
    # 2023/10/01 0:00:00 until 2023/11/01 0:00:00
    def get_list_parking_data():
        num_of_files = 746
        return [
            hour_data
            for hour_data in [
                pd.read_csv(f"aggregated/aggregated_data_{file_num}.csv")
                for file_num in range(1, num_of_files + 1)
            ]
        ]

    def normalise_parking_data(df):
        # fill in the missing neighbourhoods in each hourly dataframe
        # and replace nans with 0 (missing neighbourhood == 0 parked vehicles)
        return (
            df.set_index("Wijk")
            .reindex(neighbourhood_list)
            .fillna(0)
            .sort_values(by="Wijk")
        )

    def get_merged_parking_data(df_list):
        df_merged_data = pd.DataFrame()
        for hour, df in enumerate(df_list):
            df = normalise_parking_data(df)
            df["hour"] = hour
            df["day"] = math.floor(hour / 24)
            df_merged_data = pd.concat([df_merged_data, df])
        return df_merged_data

    parking_data_list = get_list_parking_data()
    df = get_merged_parking_data(parking_data_list)
    return df


with open("data/merged_dataframe.pkl", "wb") as file:
    pickle.dump(get_merged_parking_data(), file)
