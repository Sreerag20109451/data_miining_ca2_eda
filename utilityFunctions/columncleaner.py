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
    # Define conditions for 'All Native', 'All Foreign', and 'At Least One Foreign'
    all_native = (dataframe["ParentA_Born_Country"].str.contains("Native", na=False) &
                  dataframe["ParentB_Born_Country"].str.contains("Native", na=False))

    all_foreign = (dataframe["ParentA_Born_Country"].str.contains("Foreign", na=False) &
                   dataframe["ParentB_Born_Country"].str.contains("Foreign", na=False))

    at_least_one = (dataframe["ParentA_Born_Country"].str.contains("Foreign", na=False) |
                    dataframe["ParentB_Born_Country"].str.contains("Foreign", na=False))

    # Initialize the 'Parental_Origin' column as "NA"
    dataframe["Parental_Origin"] = "NA"

    # Assign labels based on conditions
    dataframe.loc[all_native, "Parental_Origin"] = "All Native"
    dataframe.loc[all_foreign, "Parental_Origin"] = "All Foreign"
    dataframe.loc[at_least_one & (dataframe["Parental_Origin"] == "NA"), "Parental_Origin"] = "At least One"

    return dataframe

