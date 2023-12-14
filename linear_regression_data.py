import pandas as pd

flux_df = pd.read_pickle("data/flux_df.pkl")
min_max_df = pd.read_pickle("data/min_max_df.pkl")
avg_df = pd.read_pickle("data/avg_df.pkl")

# flux_df has generic column names, let's fix that
flux_df = flux_df.rename(
    columns=lambda column: column + "_flux" if column != "day" else column
)


# This gives each observation a unique key which makes merging the dataframes easier
def get_id_column(df):
    return flux_df.index + "_" + flux_df["day"].astype(str)


flux_df["id"] = get_id_column(flux_df)
min_max_df["id"] = get_id_column(min_max_df)
avg_df["id"] = get_id_column(avg_df)

df_merged = pd.merge(flux_df, min_max_df, on=["id", "day"])
df_merged = df_merged.merge(avg_df, on=["id", "day"])

# our "day" variable is an independent variable, let's move it back to the left
column_to_move = df_merged.pop("day")
df_merged.insert(0, "day", column_to_move)


# let's add the day of the week as data by using our "day" variable
def get_week_day(day):
    day = day % 7
    # 01/10/23 was a Sunday, therefore day 0 is Sunday, day 1 Monday and so forth.
    return (
        "sunday"
        if day == 0
        else "monday"
        if day == 1
        else "tuesday"
        if day == 2
        else "wednesday"
        if day == 3
        else "thursday"
        if day == 4
        else "friday"
        if day == 5
        else "saturday"
    )


# using .insert to have the column on the left
df_merged.insert(0, "week_day", df_merged["day"].apply(get_week_day))


df_day = pd.read_pickle("data/dataframes_by_day.pkl")[0]

print(df_merged)
