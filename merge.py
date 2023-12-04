import pandas as pd


# merge all the CSVs in the aggregated folder into one big dataframe
# (I told Dima to do it that way instead of just pickling it right away, my bad -sari)
def get_merged_csvs():
    num_of_files = 746
    for file_num in range(1, num_of_files + 1):
        file = pd.read_csv(f"aggregated/aggregated_data_{file_num}.csv")
        if file_num == 20:
            print(file)


get_merged_csvs()
