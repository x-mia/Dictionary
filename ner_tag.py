# ! polyglot download embeddings2.et ner2.et
# ! polyglot download embeddings2.sk ner2.sk
from estnltk import Text as tx
from polyglot.text import Text
import pandas as pd


def add_est_ner(row):
    word = row["Estonian word"]
    text = tx(word)
    ner = text.named_entity_labels
    for el in ner:
        return el

def add_estPolyglot_ner(row):
    word = row["Estonian word"]
    text = Text(word, hint_language_code='et')
    ner = text.entities
    if ner:
        ner = ner[0].tag
    else:
        ner = None
    return ner

def add_svkPolyglot_ner(row):
    word = row["Slovak word"]
    text = Text(word, hint_language_code='sk')
    ner = text.entities
    if ner:
        ner = ner[0].tag
    else:
        ner = None
    return ner

def add_ner(df):
    df['EstNLTK NER'] = df.apply(add_est_ner, axis=1)
    df['EST Polyglot NER'] = df.apply(add_estPolyglot_ner, axis=1)
    df['EST Polyglot NER'] = df['EST Polyglot NER'].str.replace("I-", "")
    df['SVK Polyglot NER'] = df.apply(add_svkPolyglot_ner, axis=1)
    df['SVK Polyglot NER'] = df['SVK Polyglot NER'].str.replace("I-", "")
    df = df.fillna("-")
    # df.to_csv("with-ner-tag.csv", index=False)
    return df
