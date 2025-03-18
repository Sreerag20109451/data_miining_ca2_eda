import matplotlib.pyplot as plt
import seaborn as sns
from soupsieve.util import lower


def getrelatedFields(dataframe, substring):
    mask = dataframe.columns.str.contains(substring)
    return dataframe[dataframe.columns[mask]]


def genderBasedGroupings(dataframe, column):
    filtered = dataframe[dataframe[column].str.contains("Yes")]
    grpupedByGender = filtered.groupby("Gender_Student", observed=False)[column].count()
    return grpupedByGender



def getBadPerformersByGender(dataframe, column):
    tenth_percentile = dataframe[column].quantile(0.10)
    bad_performers = dataframe[dataframe[column] <= tenth_percentile]
    grouped_performance_by_gender = bad_performers.groupby("Gender_Student",observed=False)["Gender_Student"]
    fig, ax = plt.subplots(1, 2, figsize=(10, 6))
    sns.histplot(data=bad_performers, x="Gender_Student", y=column, ax=ax[0])
    ax[0].set_xlabel("Gender")
    sns.countplot(data=bad_performers, x="Gender_Student", color="b", ax=ax[1])
    ax[1].set_xlabel("Gender")
    plt.tight_layout()
    plt.show()
    return bad_performers, grouped_performance_by_gender

def performanceDistributioninIQRbyGender(dataframe, column):
    upper = dataframe[column].quantile(0.90)
    lowerBound = dataframe[column].quantile(0.10)
    iqr_performance = dataframe[(dataframe[column] > lowerBound )& (dataframe[column] < upper)]
    grouped_performance_by_gender = iqr_performance.groupby("Gender_Student",observed=False)["Gender_Student"]
    fig, ax = plt.subplots(1, 2, figsize=(10, 6))
    sns.histplot(data=iqr_performance, x="Gender_Student", y=column, ax=ax[0])
    ax[0].set_xlabel("Gender")
    sns.countplot(data=iqr_performance, x="Gender_Student", color="b", ax=ax[1])
    ax[1].set_xlabel("Gender")
    plt.tight_layout()
    plt.show()
    return iqr_performance, grouped_performance_by_gender



