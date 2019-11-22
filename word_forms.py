from estnltk import synthesize
import pandas


def word_shapes(row):
    word = row["Estonian word"]
    postag = row["Estonian postag"]
    if postag == "S" or postag == "A" or postag == "N" or postag == "O" or postag == "P" or postag == "H" or postag == "C":
        shape1 = synthesize(word, "sg g")
        shape2 = synthesize(word, "sg p")
        shape3 = synthesize(word, "pl p")
        shape4 = synthesize(word, "adt")
        return shape1 + shape2 + shape3 + shape4
    if postag == "V":
        verb_shape1 = synthesize(word, "ma")
        verb_shape2 = synthesize(word, "da")
        verb_shape3 = synthesize(word, "n")
        verb_shape4 = synthesize(word, "takse")
        return verb_shape1 + verb_shape2 + verb_shape3 + verb_shape4
    else:
        return "-"

def add_shape(df):
    df['Shapes'] = df.apply(word_shapes, axis=1)
    # df.to_csv("with-shapes.csv", index=False)
    return df
