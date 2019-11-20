from creating import create
from wordnet import add_wordnet


def write_data(data, filename):
    with open(filename, "w", encoding="utf8") as f:
        for key, value in sorted(data.items()):
            f.writelines(key+"\t"+", ".join(value)+"\n")

def main():
    slovak_estonian, estonian_slovak = create()
    # write_data(estonian_slovak, "estonian_slovak.txt")
    slovak_estonian_df, estonian_slovak_df = add_wordnet(slovak_estonian, estonian_slovak)
    estonian_slovak_df.to_csv("estonian_slovak_dict.csv", index=False)

main()
