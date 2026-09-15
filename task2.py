import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv("earthquake_1995-2023.csv")
print("Rows and columns:", df.shape)

df = (
    df.drop_duplicates(
        subset=["title", "date_time"],
        keep="first"
    )
    .reset_index(drop=True)
)

print("\n========== AFTER DUPLICATE REMOVAL ==========")
print("Rows and columns:", df.shape)




print("\n========== MISSING VALUE REPORT ==========")

missing_count = df.isnull().sum()

missing_percentage = (
    df.isnull().mean() * 100
)

missing_report = pd.DataFrame({
    "Missing Count": missing_count,
    "Missing Percentage": missing_percentage.round(2)
})

print(missing_report)




print("\n========== ZERO VALUES ==========")

# Columns where 0 means "not measured"
zero_as_missing = [
    "cdi",
    "gap",
    "nst",
    "dmin"
]

for col in zero_as_missing:

    if col in df.columns:

        zero_count = (df[col] == 0).sum()

        print(
            f"{col}: {zero_count} zero values converted to NaN"
        )

        df[col] = df[col].replace(0, np.nan)




print("\n========== MISSING VALUES AFTER ZERO CONVERSION ==========")

missing_count = df.isnull().sum()

missing_percentage = (
    df.isnull().mean() * 100
)

missing_report = pd.DataFrame({
    "Missing Count": missing_count,
    "Missing Percentage": missing_percentage.round(2)
})

print(missing_report)




if "cdi" in df.columns:

    print("\n========== CDI ANALYSIS ==========")

    cdi_skewness = df["cdi"].skew()

    print("CDI skewness:", round(cdi_skewness, 3))

    plt.figure(figsize=(8, 5))

    plt.hist(
        df["cdi"].dropna(),
        bins=30
    )

    plt.xlabel("CDI")
    plt.ylabel("Frequency")
    plt.title("Distribution of CDI")

    plt.show()




if "gap" in df.columns:

    print("\n========== GAP ANALYSIS ==========")

    gap_skewness = df["gap"].skew()

    print("GAP skewness:", round(gap_skewness, 3))

    plt.figure(figsize=(8, 5))

    plt.hist(
        df["gap"].dropna(),
        bins=30
    )

    plt.xlabel("Gap")
    plt.ylabel("Frequency")
    plt.title("Distribution of Gap")

    plt.show()



print("\n========== IMPUTATION ==========")

# CDI
if "cdi" in df.columns:

    cdi_skewness = df["cdi"].skew()

    if abs(cdi_skewness) < 0.5:

        # Relatively symmetric distribution
        cdi_value = df["cdi"].mean()

        df["cdi"] = df["cdi"].fillna(cdi_value)

        print(
            f"CDI: Mean used because the distribution is "
            f"relatively symmetric. Mean = {cdi_value:.2f}"
        )

    else:

        # Skewed distribution
        cdi_value = df["cdi"].median()

        df["cdi"] = df["cdi"].fillna(cdi_value)

        print(
            f"CDI: Median used because the distribution is "
            f"skewed or contains strong outliers. "
            f"Median = {cdi_value:.2f}"
        )


# GAP
if "gap" in df.columns:

    gap_skewness = df["gap"].skew()

    if abs(gap_skewness) < 0.5:

        # Relatively symmetric distribution
        gap_value = df["gap"].mean()

        df["gap"] = df["gap"].fillna(gap_value)

        print(
            f"GAP: Mean used because the distribution is "
            f"relatively symmetric. Mean = {gap_value:.2f}"
        )

    else:

        # Skewed distribution
        gap_value = df["gap"].median()

        df["gap"] = df["gap"].fillna(gap_value)

        print(
            f"GAP: Median used because the distribution is "
            f"skewed or contains strong outliers. "
            f"Median = {gap_value:.2f}"
        )




print("\n========== OTHER NUMERIC COLUMNS ==========")

numeric_columns = df.select_dtypes(
    include=np.number
).columns

for col in numeric_columns:

    if df[col].isnull().sum() > 0:

        
        median_value = df[col].median()

        df[col] = df[col].fillna(median_value)

        print(
            f"{col}: Missing values filled with median "
            f"({median_value:.2f})"
        )




print("\n========== CATEGORICAL COLUMNS ==========")

categorical_columns = df.select_dtypes(
    include=["object"]
).columns

for col in categorical_columns:

    if df[col].isnull().sum() > 0:

        # Special handling for alert
        if col == "alert":

            mode_value = df[col].mode()[0]

            df[col] = df[col].fillna(mode_value)

            print(
                f"{col}: Missing values filled with mode "
                f"'{mode_value}'"
            )

        else:

            # Unknown is used for missing text/place values
            df[col] = df[col].fillna("Unknown")

            print(
                f"{col}: Missing values filled with 'Unknown'"
            )




print("\n========== FINAL MISSING VALUE CHECK ==========")

final_missing = df.isnull().sum()

print(final_missing)



total_missing = df.isnull().sum().sum()

print("\nTotal remaining missing values:", total_missing)

if total_missing == 0:

    print("SUCCESS: No missing values remain.")

else:

    print("WARNING: Some missing values still remain.")




print("\n========== FINAL VISUALIZATION ==========")

plt.figure(figsize=(8, 5))

plt.hist(
    df["magnitude"].dropna(),
    bins=30
)

plt.xlabel("Magnitude")
plt.ylabel("Number of Earthquakes")
plt.title("Distribution of Earthquake Magnitudes")

plt.show()




df.to_csv(
    "earthquake_cleaned.csv",
    index=False
)

print("\nCleaned dataset saved as:")
print("earthquake_cleaned.csv")