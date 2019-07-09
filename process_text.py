import sys
from remove_accents import Remover 
remover = Remover()


args = sys.argv[1:]

infile = args[0]

t = None

with open(infile, "r", encoding="utf-8") as f:
    t = f.read()

# get text and tokrnize
# 

from greek_tokenizer import tokenize_with_accents

paragraphs = t.split("\n\n")
paragraphs = list(map(lambda x: tokenize_with_accents(x), paragraphs))

#print(list(paragraphs))

# tokens to set

tokenset = set([w.lower() for p in paragraphs for w in p])


# load lemma dict

def read_tab_list(ipath):
    with open(ipath, 'r', encoding='utf-8') as f:
        xs = map(lambda x: x.split('\t'), f.read().strip().split('\n'))
        out = {}
        for x in xs:
            if len(x) > 1:
                inf = x[0].lower()
                lemma = x[1].lower()
                if not(inf in out):
                    out[inf] = lemma
                else:
                    out[inf] = out[inf] + ","  + lemma
            else:
                print(x)

        return out
lemmas = read_tab_list("no-accents.tab")
glss = read_tab_list("gloss-no-acccents.tab")

glosses = {}

for k,v in glss.items():
    glosses[remover.transformWord(k)] = v    


# check for unkniwn words
from unknown_words_checker import find_unknown

removeNums = lambda z: not(all(x in "1234567890" for x in z))
        

unknowns = list(filter(removeNums, find_unknown(lemmas, tokenset)))


# get lemmas for unknown words
from perseus_getter import get_unknown_words, format_output

results = get_unknown_words(unknowns)
if len(results) > 0: #this needs to check if the words are in the lemma list before blindly adding them
    with open('no-accents.tab', 'a', encoding='utf-8') as f:
        f.write("\n")
        f.write(format_output(results))
    for k,v in results.items():
        results[remover.transformWord(k)] = ",".join(v)
    lemmas.update(results)

# get lemmas
tlemmas = {}

import re

def collapse_lemmas(x):
    if "," in x:
        return set(map(lambda x: re.sub(r'[0-9]', '', x.strip()) ,x.split(',')))
    else:
        return [re.sub(r'[0-9]', '', x.strip())]
    
        
        
            

for token in tokenset:
    t = remover.transformWord(token)
    if t in lemmas:
        tlemmas[token] = collapse_lemmas(lemmas[t])
    else:
        tlemmas[token] = ["?"]
# get glosses for lemmas


tglosses = {}


for k,ls in tlemmas.items():
#    l = remover.transformWord(lemma)
    gls_for_lemma = []
    for l in ls:
        if l in glosses:
            gls_for_lemma.append(l + ": " + glosses[l])
        else:
            gls_for_lemma.append(l + ": ?")
    
    if k in tglosses:
        tglosses[k] = list(set(tglosses[k] + gls_for_lemma))
    else: 
        tglosses[k] = gls_for_lemma

# attach lemma and gloss to markuo for text.
# Figure out how to loop through lemmas and glosses for each one and attache to 
def buildTextTupsForP(p, gl, tl):
    out = []
    print(tl)
    for w in p:
        lemma = tl[w.lower()]
        print(lemma)
        glosses = gl[w.lower()]
        out.append((w, lemma, glosses))
    return out
    
textTups = map(lambda x: buildTextTupsForP(x, tglosses, tlemmas), paragraphs)

# <w lemma="" gloss="">WORD</w> with <p></p>
import xml.etree.ElementTree as ET 

text = ET.Element("text")

tree = ET.ElementTree(text)

def processP(words, p): 
    for w in words:
        e = ET.SubElement(p, "w")
        info = ET.SubElement(e, "info")
        for i in w[2]:
            data = ET.SubElement(info, "l")
            data.text = i
        form = ET.SubElement(e, "form")
        form.text = w[0]

for p in textTups:
    xmlp = ET.SubElement(text, "p")
    processP(p, xmlp)

tree.write(args[1], encoding="utf-8")

print("text xml written to " + args[1])
# xslt to transform into html inside vue componemt

# each chaoter has own data file witj book file.lisitng links to chapters. book.file.might be json spec
