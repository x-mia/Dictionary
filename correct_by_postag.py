from estnltk import Text
from bs4 import BeautifulSoup
from requests import get
from tqdm import tqdm



def add_estonian_postag(row):
    est = row['Estonian word']
    word = Text(est)
    word.tag_analysis()
    if len(word['words']) > 1:
        return "-"
    postag = word['words'][0]['analysis'][0]['partofspeech']
    return postag

def add_slovak_postag(row):
    slovak = row['Slovak word']
    postags = []
    for el in tqdm(slovak):
        try:
            with get("http://morpholyzer.fiit.stuba.sk:8080/PosTagger/xml/tag/one/" + el) as response:
                if response.ok:
                    soup = BeautifulSoup(response.text)
                    postags.append(soup.find("tag")['pos'][0])
                else:
                    postags.append('-')

        except Exception as ex:
            print(ex)
            postags.append('x')
    return postags

def correcting(df):
    indices_todrop = []
    classes = {"S":"S", "A":"GUAC", "P":"P", "N":"ON", "V":"XV"}
    for i, row in df.iterrows():
        est_postag = row['Estonian postag']
        est_word = row["Estonian word"]
        svk_postag = row['Slovak postag']
        if not est_postag in "".join(classes.values()):
            continue
        if "tud" in str(est_word) and est_postag != "A":
            continue
        if svk_postag == "x" or svk_postag == "-":
            indices_todrop.append(i)
        elif classes[svk_postag] != est_postag:
            indices_todrop.append(i)
    df = df.drop(indices_todrop)
    return df

def correct_by_postag(df):
    df['Estonian postag'] = df.apply(add_estonian_postag, axis=1)
    df['Slovak postag'] = df.apply(add_slovak_postag, axis=1)
    df = correcting(df)
    return df
