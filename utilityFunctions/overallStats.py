import  matplotlib.pyplot as plt
import seaborn as sns


def getrelatedFields(dataframe, substring):
    mask = dataframe.columns.str.contains(substring)
    return dataframe[dataframe.columns[mask]]


def genderBasedGroupings(dataframe, column):
    filtered = dataframe[dataframe[column].str.contains("Yes")]
    grpupedByGender = filtered.groupby("Gender_Student", observed=False)[column].count()
    return grpupedByGender



def OverallDistributionOfPVScores(dataframe):
    columns_having_avg = dataframe.columns.str.contains("AVERAGE_PV")
    pv_columns = dataframe.columns[columns_having_avg].tolist()
    fig, axes = plt.subplots(len(pv_columns), 1 , figsize=(10, 20 ))
    for index, col in enumerate(pv_columns):
        filtered = dataframe[col]
        sns.histplot(dataframe[col], kde=True, color="b", ax=axes[index])
        plt.xlabel(f"{col}")
        plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()




def getStatisticsAndDistribution(dataframe, column):
    filter_mask = dataframe.columns.str.contains(f"AVERAGE_PV_{column}")
    filtered = dataframe[dataframe.columns[filter_mask]]
    first_quartile = filtered.quantile(0.25)
    third_quartile = filtered.quantile(0.75)
    iqr = third_quartile - first_quartile
    lbound = first_quartile - (1.5 * iqr)
    ubound = third_quartile + (1.5 * iqr)
    fig = plt.figure(figsize=(10, 6))
    sns.histplot(filtered ,kde=True, color="b")
    plt.axvline(lbound[f"AVERAGE_PV_{column}"], color="r", linestyle="--", label="Lower Bound (Q1 - 1.5*IQR)")
    plt.axvline(ubound[f"AVERAGE_PV_{column}"], color="r", linestyle="--", label="Upper Bound (Q3 + 1.5*IQR)")
    plt.axvline(first_quartile[f"AVERAGE_PV_{column}"], color="g", linestyle="--", label="First Quartile")
    plt.axvline(third_quartile[f"AVERAGE_PV_{column}"], color="g", linestyle="--", label="Third Quartile")
    plt.xlabel(f"AVERAGE_PV_{column}")
    plt.ylabel("Frequency")
    plt.legend()
    return filtered


def findNoInIQRandOutLierCount(dataframe, column):
    filtered = dataframe[f"AVERAGE_PV_{column}"]
    first_quartile = filtered.quantile(0.25)
    third_quartile = filtered.quantile(0.75)
    iqr = third_quartile - first_quartile  # Compute IQR
    lower_bound = first_quartile - 1.5 * iqr
    upper_bound = third_quartile + 1.5 * iqr

    # Count values within IQR
    numberInIQR = filtered[(filtered >= lower_bound) & (filtered <= upper_bound)].count()

    # Count outliers
    outlierCount = filtered[(filtered < lower_bound) | (filtered > upper_bound)].count()

    return numberInIQR, outlierCount

