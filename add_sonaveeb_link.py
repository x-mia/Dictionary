from requests import get
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import time
from random import randrange

user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/70.0"

def get_website(word):
    # numb = randrange(2,10)
    try:
        # time.sleep(numb)
        with get("https://sonaveeb.ee/search/est-est/detail/" + word + "/1", headers={'User-Agent': user_agent}) as response:
            if response.ok:
                soup = BeautifulSoup(response.text)
                contain = soup.find("div", {'class':'col offset-1 lg-max-noneset'})
                if contain:
                    span = contain.find('span')
                    if span:
                        if span.text == "Ei leidnud midagi. Proovi otsida":
                            return "-"
                        else:
                            website = "https://sonaveeb.ee/search/est-est/detail/" + word + "/1"
                            return website
            else:
                return "-"
    except Exception as ex:
        print(ex)
        print(word)

def add_sonaveeb_link(df):
    websites = []
    tqdm.pandas()
    for _, row in tqdm(df.iterrows(), total=df.shape[0],position=0, leave=True):
        word = row["Estonian word"]
        websites.append(get_website(word))
    df["Sõnaveeb"] = websites
    # df.to_csv("with-sonaveeb-link.csv", index=False)
    return df
