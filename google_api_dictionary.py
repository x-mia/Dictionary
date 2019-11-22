# pip install --upgrade google-cloud-translate

import os
import pandas as pd
from tqdm import tqdm
# from google.cloud import translate_v3beta1 as translate


def get_google(estonian_slovak_df, alternative=True):
    if alternative:
        google_dictionary = pd.read_csv("Google-dictionary/googletrans.csv")
    else:
        estonian_slovak_df = estonain_slovak_df[["Estonian word"]].drop_duplicates()
        google_dictionary = google_dictionary(estonian_slovak_df)
    return google_dictionary

def google_dictionary(estonian_wordlist):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="filename.json"
    client = translate.TranslationServiceClient()

    project_id = "your-project-id"
    location = 'global'
    parent = client.location_path(project_id, location)

    trans = {'Estonian word':[], 'Slovak word':[]}
    try:
        for _, word in tqdm(estonian_wordlist.iterrows(), total=estonian_wordlist.shape[0],position=0, leave=True):
            word = word["Estonian word"]
            response = client.translate_text(
            parent=parent,
            contents=[word],
            mime_type='text/plain',
            source_language_code='et',
            target_language_code='sk')
            for translation in response.translations:
                trans['Estonian word'].append(word)
                trans['Slovak word'].append(translation.translated_text)

    except Exception as ex:
      trans[word] = "-"

    finally:
        google_dictionary = pd.DataFrame(trans)
        # google_dictionary.to_csv("googletrans.csv", index=False)
        return google_dictionary
