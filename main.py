from sys import stdin
from pprint import pprint
import pymorphy3
import sqlite3

# pip install pymorphy3
# pip install -U pymorphy3-dicts-ru


morph = pymorphy3.MorphAnalyzer()

text = ""
for i in stdin:
    text += i.rstrip("\n")

sentences = (text.replace("глубкна", "глубина").replace(",", '.').replace("\xa0", " ").
             replace("-", "—").replace("\n", "").replace(". к", ".к").
             replace("-", "").replace("г. ", "").split('. '))

if sentences[-1] == "":
    sentences.pop(-1)

# print(text)
# pprint(sentences)


def get_digits(sentence: list) -> float:
    for number in sentence:
        try:
            return float(number)
        except ValueError:
            continue


table = {}


for el in sentences:
    el = el.split()
    if el[1][0].isupper():
        name = morph.parse(el[1])[0].normal_form.capitalize().replace("ий", "ое").replace("ого", "ое")
        if name not in table.keys():
            table[name] = {}
        if el[0] not in table[name].keys():
            table[name][el[0]] = get_digits(el)

    else:
        for i in range(len(el)):
            if el[i + 1][0].isupper():
                name = morph.parse(el[i + 1])[0].normal_form.capitalize().replace("ий", "ое").replace("ого", "ое")
                if name not in table.keys():
                    table[name] = {}
                if " ".join(el[:i + 1]) not in table[name].keys():
                    table[name][" ".join(el[:i + 1])] = get_digits(el)
                break

pprint(table)

# with sqlite3.connect("table_test.db") as db:
#     cursor = db.cursor()
#     cursor.execute("DROP TABLE IF EXISTS sorted_text")
#     cursor.execute("""CREATE TABLE IF NOT EXISTS sorted_text (name TEXT)""")
