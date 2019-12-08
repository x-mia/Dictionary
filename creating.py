import re
import pandas


def load_data1():
    data = []
    for i in range(1, 616):
        filename = "English-Slovak/directory"
        with open(filename + str(i) + ".csv", 'r', encoding="utf8") as f:
            content = f.readlines()
            for el in content:
                data.append(el)
    return data


def clean_data(data):
    cleaned_data = []
    for el in data:
        cleaned_el = el.split("\t")
        cleaned_data.append(cleaned_el[0])
    return cleaned_data

def load_data2():
    with open("English-Slovak/eng-svk.txt", "r", encoding="utf8") as f:
        data = f.readlines()
    return data[9:]


def clean_data2(data):
    cleaned_data = []
    for el in data:
        cleaned_el = el.split("\t")[0]
        new_cleaned_el = cleaned_el.split(" ")
        new_data = []
        for word in new_cleaned_el:
            if word[0] not in ".,[{(<" and word[-1] not in ",]})>":
                new_data.append(word)
        new_data = " ".join(new_data)
        cleaned_data.append(new_data)
    return cleaned_data

def get_english_wordlist():
    data1 = load_data1()
    cleaned_data = clean_data(data1)
    data2 = load_data2()
    cleaned_data2 = clean_data2(data2)
    dataset = list(set(cleaned_data + cleaned_data2))
    return sorted(dataset)

#########################################################

def load_data(filename):
    with open(filename, "r", encoding="utf8") as f:
        data = f.readlines()
    return data

def compare_data(read_data1, read_data2):
    same_words = []
    for el in read_data1:
        if el[:-1] in read_data2:
            same_words.append(el[:-1])
    return same_words

def get_intersection():
    data1 = load_data("English-wordlist-from-estonian/english_est.txt")
    data2 = get_english_wordlist()
    same_words = compare_data(data1, data2)
    return same_words

#########################################################

def process_data1(data):
    processed_data = {}
    for el in data:
        english, slovak = el.split("\t")[:2]
        if english not in processed_data.keys():
            processed_data[english] = []
        processed_data[english].append(slovak[:-1])
    return processed_data


def process_data2(data):
    processed_data = {}
    for el in data:
        english, slovak = el.split("\t")[:2]
        english = clean(english)
        slovak = clean(slovak)
        if english not in processed_data.keys():
            processed_data[english] = []
        processed_data[english].append(slovak)
    return processed_data


def clean(phrase):
    words = phrase.split(" ")
    cleaned_words = []
    for word in words:
        if word[0] not in ".,<{([" and word[-1] not in ",>)}]":
            cleaned_words.append(word)
    return " ".join(cleaned_words)


def joining_dicts(data1, data2):
    for key, value in data2.items():
        if key not in data1.keys():
            data1[key] = value
        else:
            for word in value:
                if word not in data1[key]:
                    data1[key].append(word)
    return data1

def get_slovak_dict():
    data1 = load_data1()
    data2 = load_data2()
    result1 = process_data1(data1)
    result2 = process_data2(data2)
    result = joining_dicts(result1, result2)
    return result
#########################################################

def load_eng_est():
    with open("English-Estonian/english-estonian.txt", "r", encoding="utf8") as f:
        data = f.readlines()
    return data


def clean_eng_est(data):
    processed_data = {}
    new_data = []
    for el in data:
        if el != '\n':
            new_data.append(el)
    english_word = True
    for word in new_data:
        if english_word:
            english = word
            english_word = False
        else:
            estonian = word
            english_word = True
            if english not in processed_data.keys():
                processed_data[english[:-1]] = []
            processed_data[english[:-1]].append(estonian[:-1])
    return processed_data

def get_est_dict():
    data = load_eng_est()
    result = clean_eng_est(data)
    return result
#########################################################

def clean_content(content):
    final_list = {}
    for key in content.keys():
        clean_key = key.split("; ")
        for new_key in clean_key:
            if new_key in final_list.keys():
                final_list[new_key] = final_list[new_key] + content[key]
            final_list[new_key] = content[key]

    return final_list


def remove_parenthesis(final_list):
    fixed_words = {}
    for el in final_list.keys():
        old_el = el
        el = re.sub(r"\(.*?\)", "", el)
        fixed_words[el] = final_list[old_el]
    return fixed_words


def other_cleaning(fixed_words):
    nice_words = {}
    for el in fixed_words.keys():
        new_clean_el = el.split(", ")
        for new_el in new_clean_el:
            if new_el in nice_words.keys():
                nice_words[new_el] = nice_words[new_el] + fixed_words[el]
            nice_words[new_el.strip()] = fixed_words[el]
    return nice_words

def correct(estonian_slovak):
    result = clean_content(estonian_slovak)
    result2 = remove_parenthesis(result)
    result3 = other_cleaning(result2)
    return result3

#########################################################

def write_data(data, filename):
    with open(filename, "w", encoding="utf8") as f:
        for key, value in sorted(data.items()):
            f.writelines(key+"\t"+", ".join(value)+"\n")

#########################################################

def create_df(dictionary, source, target):
    temp_dict = {source: [], target: []}
    for key, values in dictionary.items():
        for value in values:
            temp_dict[source].append(key)
            temp_dict[target].append(value)


    return pandas.DataFrame.from_dict(temp_dict)

#########################################################

def create():
    print("Getting common list")
    common_list = get_intersection()
    print("Getting slovak dict")
    slovak_dict = get_slovak_dict()
    print("Getting eesti dict")
    eesti_dict = get_est_dict()
    print("Making dict")
    slovak_estonian = {}
    estonian_slovak = {}
    for el in common_list:
        slovak_words = slovak_dict[el]
        estonian_words = eesti_dict[el]
        for slovak_word in slovak_words:
            slovak_estonian[slovak_word] = estonian_words
        for estonian_word in estonian_words:
            estonian_slovak[estonian_word] = slovak_words

    estonian_slovak = correct(estonian_slovak)
    # write_data(estonian_slovak, "estonian_slovak.txt")

    slovak_estonian_df = create_df(slovak_estonian, "Slovak word", "Estonian word")
    slovak_estonian_df = slovak_estonian_df.sort_values(by=["Slovak word"])
    estonian_slovak_df = create_df(estonian_slovak, "Estonian word", "Slovak word")
    estonian_slovak_df = estonian_slovak_df.sort_values(by=["Estonian word"])
    # estonian_slovak_df.to_csv("estonian-slovak.csv", index=False)

    return (slovak_estonian_df, estonian_slovak_df)

# create()
#########################################################
