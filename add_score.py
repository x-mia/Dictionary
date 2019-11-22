import pandas as pd
import numpy as np


def add_score(estonian_slovak_df, estonian_slovak, estonian_wordnet, google_dictionary):
    print("Adding score")
    df_basic = add_single_score(estonian_slovak_df, estonian_slovak, 0.25, "Score-basic")
    df_wordnet = add_single_score(df_basic, estonian_wordnet, 0.5, "Score-wordnet")
    df_google = add_single_score(df_wordnet, google_dictionary, 0.25, "Score-google")

    df_google["Score"] = df_google["Score-basic"] + df_google["Score-wordnet"] + df_google["Score-google"]
    df = df_google.drop(columns=['Score-basic', "Score-wordnet", "Score-google"])
    return df

def add_single_score(df1, df2, score, indicator):
    df = pd.merge(df1, df2, on=['Estonian word','Slovak word'], how='left', indicator=indicator)
    df[indicator] = np.where(df[indicator] == 'both', score, 0)
    return df
