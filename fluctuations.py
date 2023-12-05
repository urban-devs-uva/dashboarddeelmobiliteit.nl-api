import pandas as pd
import pickle


def get_fluctuations_df():
    dfs_by_day = pd.read_pickle("data/dataframes_by_day.pkl")
    neighbourhood_list = pd.Index.unique(dfs_by_day[0].index)
    vehicles_list = ["bicycle", "cargo_bicycle", "moped", "scooter"]

    # what we are calculating here is the total number of fluctuation in a single day
    # for a neighbourhood and its respective vehicles.
    # e.g., if at hour 1 we have 30 parked vehicles and at hour 2 we have 33 parked
    # vehicles, then that adds 3 to the flux value. We do that for all the hours of the day.
    def calculate_flux(parking_series):
        flux = 0
        last_value = None

        for parking_value in parking_series:
            if last_value is None:
                last_value = parking_value
            else:
                flux += abs(parking_value - last_value)
                last_value = parking_value

        return flux

    def get_flux_one_neighbourhood(df_neighbourhood):
        return {
            vehicle: calculate_flux(df_neighbourhood[vehicle])
            for vehicle in vehicles_list
        }

    def get_flux_one_day(df_day):
        df_flux = pd.DataFrame(
            {
                neighbourhood: get_flux_one_neighbourhood(df_day.loc[neighbourhood])
                for neighbourhood in neighbourhood_list
            }
        ).T
        df_flux["day"] = df_day["day"].iloc[0]
        return df_flux

    def get_flux_all_days(df_day_list):
        df_all_days = pd.DataFrame()
        for df_day in df_day_list:
            df_all_days = pd.concat([df_all_days, get_flux_one_day(df_day)])
        return df_all_days

    return get_flux_all_days(dfs_by_day)


def get_list_of_dfs_by_day(df):
    return [item[1] for item in df.groupby(["day"])]


def write_flux_data():
    df = get_fluctuations_df()

    with open("data/flux_df.pkl", "wb") as file:
        pickle.dump(df, file)

    with open("data/flux_df_list_by_day.pkl", "wb") as file:
        pickle.dump(get_list_of_dfs_by_day(df), file)


write_flux_data()
