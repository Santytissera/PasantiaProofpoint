#Leer el archivo .txt
#Normalizar las palabras, contar cuantas veces aparecen en el texto
#y agregar esa frecuencia en una lista "palabra, frecuencias"
#Ordenar por frecuencia mayor a menor
#mostrar

from operator import itemgetter
import unicodedata
import re

def normalize_text(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def read_file(file):
    words_list = []
    with open(file,"r",encoding="utf-8") as f:
        for line in f:
            line = line.strip().lower().split()

            for w in line:
                w = normalize_text(w)
                words_list.append(w)

        words_list = [x for item in words_list for x in item.split(" ")]

    return words_list


def count_frecuency(list):
    frecuency = []
    for w in list:
        frecuency.append(list.count(w))
    return frecuency

def sort_frecuencys(list):
        topFrecuency = sorted(list, key=itemgetter(1),reverse=True)[:10]
        return topFrecuency
def main():
    file = "data/archivo.txt"
    word_list = read_file(file)
    frecuency = count_frecuency(word_list)
    Frecuencys = list(set(zip(word_list,frecuency)))
    topFrecuency = sort_frecuencys(Frecuencys)
    print(topFrecuency)
main()