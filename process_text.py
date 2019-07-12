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
    print(list(p))
    p = check_unknown_lemmas_in_p(p, MANUAL_LEMMAS)
    paragraphs.append(p)

#paragraphs = list(map(lambda x: map(lambda y: strip_last_accent_if_two(y), tokenize_with_accents(x)), paragraphs))
#paragraphs  = list(map(lambda x: check_unknown_lemmas_in_p(lemmatizer.lemmatize(x), MANUAL_LEMMAS), paragraphs))

#print(list(paragraphs))

# tokens to set

#tokenset = set([w.lower() for p in paragraphs for w in p])


# load lemma dict

#lemmas = read_tab_list("no-accents.tab")
glosses = read_tab_list("gloss-no-acccents.tab")
#glosses = read_tab_list("gloss-dict.tab")
paras = []
for p in paragraphs:
    pnew = []
    for w in p:
        try:
            if w[1] in glosses:
                pnew.append((w[0], w[1], glosses[w[1].lower()]))
            else:
                print(w[0] + " : " + w[1]) 
                pnew.append((w[0], w[1], "?" ))
        except:
            print(w)
    paras.append(pnew)

#glosses = {}

#for k,v in glss.items():
#    glosses[remover.transformWord(k)] = v    


# check for unkniwn words
from unknown_words_checker import find_unknown

#removeNums = lambda z: not(all(x in "1234567890" for x in z))
        

#unknowns = list(filter(removeNums, find_unknown(lemmas, tokenset)))


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

# get lemmas
#tlemmas = {}

        
        
            

#for token in tokenset:
#    t = remover.transformWord(token)
#    if t in lemmas:
#        tlemmas[token] = collapse_lemmas(lemmas[t])
#    else:
#        tlemmas[token] = ["?"]
# get glosses for lemmas


#tglosses = {}


#for k,ls in tlemmas.items():
#    l = remover.transformWord(lemma)
#    gls_for_lemma = []
#    for l in ls:
#        if l in glosses:
#            gls_for_lemma.append(l + ": " + glosses[l])
#        else:
#            gls_for_lemma.append(l + ": ?")
#    
#    if k in tglosses:
#        tglosses[k] = list(set(tglosses[k] + gls_for_lemma))
#    else: 
#        tglosses[k] = gls_for_lemma

# attach lemma and gloss to markuo for text.
# Figure out how to loop through lemmas and glosses for each one and attache to 
#def buildTextTupsForP(p, gl, tl):
#    out = []
#    print(tl)
#    for w in p:
#        lemma = tl[w.lower()]
#        print(lemma)
#        glosses = gl[w.lower()]
#        out.append((w, lemma, glosses))
#    return out
    
#textTups = map(lambda x: buildTextTupsForP(x, tglosses, tlemmas), paragraphs)

# <w lemma="" gloss="">WORD</w> with <p></p>
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
