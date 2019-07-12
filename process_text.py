import sys
from cltk.lemmatize.greek.backoff import BackoffGreekLemmatizer
from remove_accents import Remover 
import re
import betacode.conv
from greek_normalisation.utils import strip_last_accent_if_two
from greek_normalisation.normalise import Normaliser

normer = Normaliser().normalise

def collapse_lemmas(x):
    if "," in x:
        return set(map(lambda x: re.sub(r'[0-9]', '', x.strip()) ,x.split(',')))
    else:
        return [re.sub(r'[0-9]', '', x.strip())]
    

def replaceShorts(w):
    return w.replace('ᾰ', 'α').replace('ῐ', 'ι').replace('ῠ', 'υ')

def read_tab_list(ipath):
    with open(ipath, 'r', encoding='utf-8') as f:
        xs = map(lambda x: x.split('\t'), f.read().strip().split('\n'))
        out = {}
        for x in xs:
            if len(x) > 1:
                inf = replaceShorts(normer(x[0].lower())[0])
                lemma = x[1].lower()
                if not(inf in out):
                    out[inf] = lemma
                else:
                    out[inf] = out[inf] + ","  + lemma
            else:
                print(x)

        return out




remover = Remover()

lemmatizer = BackoffGreekLemmatizer()

args = sys.argv[1:]

infile = args[0]

t = None

with open(infile, "r", encoding="utf-8") as f:
    t = f.read()

# get text and tokrnize
# 

from greek_tokenizer import tokenize_with_accents

def check_unknown_lemmas_in_p(p, extras):
    para = []
    for w in p:
        token = w[0]
        lemma = w[1]
        if token == lemma:
            if token.lower() in extras:
                para.append((token, extras[token.lower()]))
            else:
                para.append((token, lemma))
        else:
            para.append((token, lemma))
    return para

MANUAL_LEMMAS = read_tab_list('manual-lemmas.tab')

#paragraphs = t.split("\n\n")
paragraphs = []

for p in t.split("\n\n"):
    p = tokenize_with_accents(p)
    p = map(lambda x: strip_last_accent_if_two(x), p)
    p = lemmatizer.lemmatize(list(p))
    p = check_unknown_lemmas_in_p(p, MANUAL_LEMMAS)
    paragraphs.append(p)


glosses = read_tab_list("gloss-no-acccents.tab")

paras = []
for p in paragraphs:
    pnew = []
    for w in p:
        try:
            lemma = re.sub(r'[0-9]','', w[1]).lower()
            if lemma in glosses:
                pnew.append((w[0], w[1], glosses[lemma]))
            else:
                print(w[0] + " : " + w[1]) 
                pnew.append((w[0], w[1], "?" ))
        except:
            print(w)
    paras.append(pnew)


# get lemmas for unknown words
#from perseus_getter import get_unknown_words, format_output

#results = get_unknown_words(unknowns)
#if len(results) > 0: #this needs to check if the words are in the lemma list before blindly adding them
#    with open('no-accents.tab', 'a', encoding='utf-8') as f:
#        f.write("\n")
#        f.write(format_output(results))
#    for k,v in results.items():
#        results[remover.transformWord(k)] = ",".join(v)
#    lemmas.update(results)


import xml.etree.ElementTree as ET 

text = ET.Element("text")

tree = ET.ElementTree(text)

def processP(words, p): 
    for w in words:
        e = ET.SubElement(p, "w")
        info = ET.SubElement(e, "info")
        #for i in w[2]:
        data = ET.SubElement(info, "l")
        data.text = w[1] + ": " + w[2]
        form = ET.SubElement(e, "form")
        form.text = w[0]

#for p in textTups:
for p in paras:
    xmlp = ET.SubElement(text, "p")
    processP(p, xmlp)

tree.write(args[1], encoding="utf-8")

print("text xml written to " + args[1])
# xslt to transform into html inside vue componemt

# each chaoter has own data file witj book file.lisitng links to chapters. book.file.might be json spec
