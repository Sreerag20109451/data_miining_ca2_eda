import pandas as pad

def removeNullAttributes(dataframe):

    columns_to_drop = []
    for feature in dataframe.columns:
        if dataframe[feature].isnull().sum() >3000:
            columns_to_drop.append(feature)

    cleaned_df = dataframe.drop(columns_to_drop)
    return cleaned_df