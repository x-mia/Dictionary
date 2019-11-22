from creating import create
from wordnet import get_wordnet
from google_api_dictionary import get_google
from add_score import add_score
from correct_by_postag import correct_by_postag
from ner_tag import add_ner
from word_forms import add_shape
from add_sonaveeb_link import add_sonaveeb_link
import pandas as pd


def add_smth(dict_df1, dict_df2, alternative=True):
    if alternative:
        main_language = "Estonian"
    else:
        main_language = "Slovak"
    concatenated_df = pd.concat([dict_df1, dict_df2], ignore_index=True, sort=False).drop_duplicates().dropna()
    concatenated_df = concatenated_df.sort_values(by=[main_language + " word"])
    return concatenated_df


def main():
    slovak_estonian, estonian_slovak = create()
    # estonian_slovak = pd.read_csv("estonian-slovak.csv")
    slovak_wordnet, estonian_wordnet = get_wordnet()
    # estonian_wordnet.to_csv("estonian_wordnet.csv", index=False)
    estonian_wordnet = pd.read_csv("estonian_wordnet.csv")
    estonian_slovak_df = add_smth(estonian_slovak, estonian_wordnet)
    google_dictionary = get_google(estonian_slovak_df)
    estonian_slovak_df = add_smth(estonian_slovak_df, google_dictionary)
    # estonian_slovak_df.to_csv("estonian_slovak_dict.csv", index=False)
    score_df = add_score(estonian_slovak_df, estonian_slovak, estonian_wordnet, google_dictionary)
    # score_df.to_csv("score.csv", index=False)
    estonian_slovak_df = correct_by_postag(estonian_slovak_df)
    estonian_slovak_df = add_ner(estonian_slovak_df)
    estonian_slovak_df = add_shape(estonian_slovak_df)
    estonian_slovak_df = add_sonaveeb_link(estonian_slovak_df)

main()
