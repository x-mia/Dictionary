import pandas as pd
from bs4 import BeautifulSoup as bs
from tqdm import tqdm


def load_svk_wordnet():
    slovak_wordnet = pd.read_csv("Wordnet/slovak-wordnet.tab", skiprows=1, names=["Number", "Lemma", "Slovak word"], usecols=["Number", "Slovak word"], delimiter="\t")
    return slovak_wordnet

def transform_to_df(estonian_wordnet):
    soup = bs(estonian_wordnet, features="html5lib")
    lexicon_entries = soup.find_all('lexicalentry')
    dict1 = {"Estonian word" : [],"synset_id" : []}
    for entry in tqdm(lexicon_entries):
        form = entry.find("lemma")["writtenform"]
        syns = entry.find_all("sense")
        for syn in syns:
            dict1["Estonian word"].append(form)
            dict1["synset_id"].append(syn['synset'])
    my_form = pd.DataFrame.from_dict(dict1)


    synsets = soup.find_all('synset')
    dict2 = {'syn_id':[],'pwn_id':[]}
    for syn in tqdm(synsets):
        id = syn["id"]
        references = syn.find_all("reference", externalsystem="PWN-3.0", reltype="eq_synonym")
        for ref in references:
            if ref:
                refs = ref.text
            else:
                refs = None
            dict2['syn_id'].append(id)
            dict2['pwn_id'].append(refs)
    my_pwn = pd.DataFrame.from_dict(dict2)
    merged_df = pd.merge(my_form, my_pwn, how="left", left_on="synset_id", right_on="syn_id")
    new_df = merged_df.dropna()
    final_df = new_df.drop(columns=['synset_id', 'syn_id'])
    return final_df

def load_est_wordnet():
    estonian_wordnet = open("Wordnet/estonian-wordnet.xml", encoding="utf8").read()
    estonian_wordnet = transform_to_df(estonian_wordnet)
    return estonian_wordnet

def merge_wordnets(slovak_wordnet, estonian_wordnet):
    est_wordnet = pd.merge(estonian_wordnet, slovak_wordnet, how="left", left_on="pwn_id", right_on="Number")
    est_wordnet = est_wordnet.dropna().drop(columns=['pwn_id', 'Number']).drop_duplicates()
    svk_wordnet= pd.merge(slovak_wordnet, estonian_wordnet, how="left", left_on="Number", right_on="pwn_id")
    svk_wordnet = svk_wordnet.dropna().drop(columns=['pwn_id', 'Number']).drop_duplicates()
    return svk_wordnet, est_wordnet

def get_wordnet():
    print("Loading wordnets")
    slovak_wordnet = load_svk_wordnet()
    estonian_wordnet = load_est_wordnet()
    print("Merging and concatenatening")
    slovak_wordnet, estonian_wordnet = merge_wordnets(slovak_wordnet, estonian_wordnet)
    return slovak_wordnet, estonian_wordnet
