
from greek_tokenizer import tokenize

def read_forms_list(ipath):
    with open(ipath, 'r', encoding='utf-8') as f:
        xs = map(lambda x: x.split('\t'), f.read().split('\n'))
        out = {}
        for x in xs:
            inf = x[0].lower()
            lemma = x[1].lower()
            out[inf] = lemma
        return out


import betacode.conv

def find_unknown(known, tokens):
    return list(set(map(lambda y: betacode.conv.uni_to_beta(y), filter(lambda x: not(x in known), tokens))))

def main(tpath, forms_path):
    forms = read_forms_list(forms_path)
    text = ''
    with open(tpath, 'r', encoding='utf-8') as f:
        text = f.read()
    tokens = tokenize(text)
    print(len(tokens))
    unknowns = find_unknown(forms, tokens)
    print(len(unknowns))
    with open('unknown.txt', 'w', encoding = 'utf-8') as f:
        f.write("\n".join(unknowns))
    print("done!")

import sys

if __name__ == '__main__':
    args = sys.argv[1:]
    main(args[0], args[1])
        

