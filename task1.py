import pandas as pd
df = pd.read_csv("earthquake_1995-2023.csv")
print("Rows and columns:", df.shape)
df.head()
df.info()
print("Exact duplicate rows:", df.duplicated().sum())
dupe_mask = df.duplicated(subset=["title","date_time"], keep=False)
print("Rows involved in a title+date_time duplicate:",dupe_mask.sum())
df[dupe_mask].sort_values('title')[["title","date_time","magnitude", "country"]]
before =len(df)
df = df.drop_duplicates(subset=["title", "date_time"],keep="first").reset_index(drop=True)
after = len(df)
print(f"Removed {before - after} duplicate row(s)")
print("Rows now:", after)
print("Final dataset shape:", df.shape)

print("Remaining exact duplicate rows:", df.duplicated().sum())

print(
    "Remaining title + date_time duplicates:",
    df.duplicated(
        subset=["title", "date_time"]
    ).sum()
)