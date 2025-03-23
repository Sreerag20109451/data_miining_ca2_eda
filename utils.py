
import matplotlib.pyplot as plt
import seaborn as sns
from fontTools.misc.cython import returns
from soupsieve.util import lower
import pandas as pd
import  scipy.stats as stats


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

def getOverallBestorWorst(dataframe, percentile):
    columns_having_avg = dataframe.columns.str.contains("AVERAGE_PV")
    pv_columns = dataframe.columns[columns_having_avg].tolist()
    for col in pv_columns:
        if(percentile > 0.10):
            percentile_val = dataframe[col].quantile(percentile)
            dataframe = dataframe[dataframe[col] >= percentile_val]
        else:
            percentile_val = dataframe[col].quantile(percentile)
            dataframe = dataframe[dataframe[col] <= percentile_val]

    sns.histplot(data=dataframe, x="Gender_Student",)
    plt.tight_layout()
    plt.show()
    plt.show()


    return dataframe

def getDisorderlyBehaviourPerGender(dataframe, topic, behaviour):
    filtered = dataframe[dataframe[f"Disorderly_Behavior_during_{topic}_Lessons"].str.contains(behaviour)]
    grouped = filtered.groupby("Gender_Student", observed=False)["Gender_Student"]
    fig, ax = plt.subplots(1, 2, figsize=(10, 6))
    sns.histplot(data=filtered, x="Gender_Student", y=f"Disorderly_Behavior_during_{topic}_Lessons", ax=ax[0])
    ax[0].set_xlabel("Gender")
    sns.countplot(data=filtered, x="Gender_Student", color="b", ax=ax[1])
    ax[1].set_xlabel("Gender")
    plt.tight_layout()
    plt.show()
    return filtered  , grouped


def subjectLikeness(dataframe, topic, behaviour):
    filtered = dataframe[dataframe[f"Students_Like_Learning_{topic}"].str.contains(behaviour)]
    grouped = filtered.groupby("Gender_Student", observed=False)["Gender_Student"]
    fig, ax = plt.subplots(1, 2, figsize=(10, 6))
    sns.histplot(data=filtered, x="Gender_Student", y=f"Students_Like_Learning_{topic}", ax=ax[0])
    ax[0].set_xlabel("Gender")
    sns.countplot(data=filtered, x="Gender_Student", color="b", ax=ax[1])
    ax[1].set_xlabel("Gender")
    plt.tight_layout()
    plt.show()
    return filtered  , grouped


def getPercentageByGender(dataframe, ref_dataframe, gender):
    perc_g = dataframe[dataframe["Gender_Student"].str.contains(gender)]["Gender_Student"].count() / \
                ref_dataframe[ref_dataframe["Gender_Student"].str.contains(gender)]["Gender_Student"].count()
    print(perc_g)




def getDissorderlyBehaviourGrouped(dataframe,group_col, topic,behaviour):
    filtered = dataframe[dataframe[f"Disorderly_Behavior_during_{topic}_Lessons"].str.contains(behaviour)]
    grouped = filtered.groupby(group_col, observed=False)[group_col]
    sns.countplot(data=filtered, x=group_col, hue=group_col)
    plt.tight_layout()
    plt.show()
    return filtered, grouped



def refillParentalEducation(dataframe):
    df_edu_mask = dataframe.columns.str.contains('Edu_Level')
    columns = dataframe.columns[df_edu_mask]
    for col in columns:
        dataframe[col] = dataframe[col].apply(lambda x: "Not Available" if "i don’t know" in str(x).lower() else x)
        dataframe[col] = dataframe[col].apply(lambda x: "Not Available" if "not applicable" in str(x).lower() else x)
        dataframe[col] = dataframe[col].apply(lambda x: "Postgraduate" if "postgraduate" in str(x).lower() else x)
        dataframe[col] = dataframe[col].apply(lambda x: "Upper Secondary" if "upper secondary" in str(x).lower() else x)
        dataframe[col] = dataframe[col].apply(lambda x: "Tertiary" if "tertiary" in str(x).lower() else x)
        dataframe[col] = dataframe[col].apply(lambda x: "Undergraduate" if "bachelor" in str(x).lower() else x)
        dataframe[col] = dataframe[col].apply(
            lambda x: "primary" if "primary education" in str(x).lower() else x)

        dataframe[col] = dataframe[col].apply(
            lambda x: "primary" if "lower secondary" in str(x).lower() else x)
        dataframe[col] = dataframe[col].apply(
            lambda x: "Post - secondary" if "post - secondary" in str(x).lower() else x)

    return dataframe

def secondaryCleaning(dataframe):
    df_edu_mask = dataframe.columns.str.contains('Edu_Level')
    columns = dataframe.columns[df_edu_mask]
    for col in columns:
        dataframe[col] = dataframe[col].apply(lambda x: "Postgraduate" if "Postgraduate" in str(x) else x)
        dataframe[col] = dataframe[col].apply(lambda x: "Tertiary" if "Tertiary" in str(x) else x)
        dataframe[col] = dataframe[col].apply(lambda x: "Undergraduate" if "Undergraduate" in str(x) else x)
        dataframe[col] = dataframe[col].apply(lambda x: "Not Available" if "Not Available" in str(x) else x)
        dataframe[col] = dataframe[col].apply(lambda x: "Upper Secondary" if "Upper Secondary" in str(x) else x)
        dataframe[col] = dataframe[col].apply(lambda x: "Primary" if "primary" in str(x)else x)


    return dataframe

def getPercentageFromReferCol(dataframe,refer_datafreame,col):
    return dataframe[col].count()/refer_datafreame[col].count() *  100


def originOfParents(dataframe):
    # Default category: "NA"
    dataframe["Parental_Origin"] = "NA"

    # Define conditions
    all_native = (dataframe["ParentA_Born_Country"].str.contains("Native", na=False) &
                  dataframe["ParentB_Born_Country"].str.contains("Native", na=False))

    all_foreign = (dataframe["ParentA_Born_Country"].str.contains("Foreign", na=False) &
                   dataframe["ParentB_Born_Country"].str.contains("Foreign", na=False))

    at_least_one_foreign = ((dataframe["ParentA_Born_Country"].str.contains("Foreign", na=False) |
                             dataframe["ParentB_Born_Country"].str.contains("Foreign", na=False)) &
                            ~all_foreign)  # Ensure it's not already categorized as "All Foreign"

    # Assign categories
    dataframe.loc[all_native, "Parental_Origin"] = "All Native"
    dataframe.loc[all_foreign, "Parental_Origin"] = "All Foreign"
    dataframe.loc[at_least_one_foreign, "Parental_Origin"] = "At least One"

    return dataframe




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

def getOverallBestorWorst(dataframe, percentile):
    columns_having_avg = dataframe.columns.str.contains("AVERAGE_PV")
    pv_columns = dataframe.columns[columns_having_avg].tolist()
    for col in pv_columns:
        if(percentile > 0.10):
            percentile_val = dataframe[col].quantile(percentile)
            dataframe = dataframe[dataframe[col] >= percentile_val]
        else:
            percentile_val = dataframe[col].quantile(percentile)
            dataframe = dataframe[dataframe[col] <= percentile_val]

    sns.histplot(data=dataframe, x="Gender_Student",)
    plt.tight_layout()
    plt.show()
    plt.show()


    return dataframe

def getDisorderlyBehaviourPerGender(dataframe, topic, behaviour):
    filtered = dataframe[dataframe[f"Disorderly_Behavior_during_{topic}_Lessons"].str.contains(behaviour)]
    grouped = filtered.groupby("Gender_Student", observed=False)["Gender_Student"]
    fig, ax = plt.subplots(1, 2, figsize=(10, 6))
    sns.histplot(data=filtered, x="Gender_Student", y=f"Disorderly_Behavior_during_{topic}_Lessons", ax=ax[0])
    ax[0].set_xlabel("Gender")
    ax[0].set_title(f"Gender and Disorderly Behaviour during {topic} classes")
    sns.countplot(data=filtered, x="Gender_Student", color="b", ax=ax[1])
    ax[1].set_xlabel("Gender")
    ax[1].set_title(f"Gender and Disorderly Behaviour during {topic} classes")
    plt.tight_layout()
    plt.show()
    return filtered  , grouped


def subjectLikeness(dataframe, topic, behaviour):
    filtered = dataframe[dataframe[f"Students_Like_Learning_{topic}"].str.contains(behaviour)]
    grouped = filtered.groupby("Gender_Student", observed=False)["Gender_Student"]
    fig, ax = plt.subplots(1, 2, figsize=(10, 6))
    sns.histplot(data=filtered, x="Gender_Student", y=f"Students_Like_Learning_{topic}", ax=ax[0])
    ax[0].set_xlabel("Gender")
    sns.countplot(data=filtered, x="Gender_Student", color="b", ax=ax[1])
    ax[1].set_xlabel("Gender")
    plt.tight_layout()
    plt.show()
    return filtered  , grouped


def getPercentageByGender(dataframe, ref_dataframe, gender):
    perc_g = dataframe[dataframe["Gender_Student"].str.contains(gender)]["Gender_Student"].count() / \
                ref_dataframe[ref_dataframe["Gender_Student"].str.contains(gender)]["Gender_Student"].count()
    print(perc_g)





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


import matplotlib.pyplot as plt
import seaborn as sns


def distributionOfFacilities(dataframe,column):
    column_names = ["Books_Home", "Own_Computer", "Shared_Computer", "Smartphone", "Internet_Access", "Study_Desk",
                    "Own_Room"]
    fig, axes = plt.subplots(len(column_names), 1, figsize=(10, 20))
    for index, col in enumerate(column_names):
        sns.countplot(data=dataframe, hue=column, x=col, ax=axes[index])  # Correct axes indexing
        axes[index].set_xlabel(f"{col}")
        axes[index].set_ylabel("Frequency")
        axes[index].set_title(f"{col}")

    # Adjust layout to avoid overlap
    plt.tight_layout()
    plt.show()  # Display the plot


def getPercentageOfBulliedStudents(dataframe, conditionstr, columnToGroup):
    condition = dataframe["Student_Bullying"].str.contains(conditionstr)
    filtered = dataframe[condition]
    origin_grouped = filtered.groupby(columnToGroup, observed=False)[columnToGroup]
    grouped_percentage = origin_grouped.count() / filtered[columnToGroup].count()
    percentageFromTotal =  origin_grouped.count() / dataframe[columnToGroup].count()
    return  grouped_percentage , percentageFromTotal


def getPercentageOfSenseOfBelonging(dataframe, conditionstr, columnToGroup):
    condition = dataframe["Sense_of_School_Belonging"].str.contains(conditionstr)
    filtered = dataframe[condition]
    origin_grouped = filtered.groupby(columnToGroup, observed=False)[columnToGroup]
    grouped_percentage = origin_grouped.count() / filtered[columnToGroup].count()
    percentageFromTotal =  origin_grouped.count() / dataframe[columnToGroup].count()
    return  grouped_percentage , percentageFromTotal


def chisquqared(dataframe,col1,col2):
    contingency_table = pd.crosstab(dataframe[col1], dataframe[col2])

    # Perform chi-square test
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)

    print(f"Chi-square statistic of {col1}: {chi2}")
    print(f"P-value of {col1}: {p}")
