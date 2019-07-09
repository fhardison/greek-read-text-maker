import re
from remove_accents import Remover 
remover = Remover()

PUNCTREGEX1 = r'\b([;,.?\'"·])'
REP1 = r' \1'

PUNCTREGEX2 = r'([;,.?\'"·])(\S)'
REP2 = r'\1 \2'

def tokenize(text):
    #add spaces around punct
    x = re.sub(PUNCTREGEX2, REP2, re.sub(PUNCTREGEX1, REP1, text.replace("\n", " \n ")))
    xs = x.split(' ')
    #remove empty elements
    return list(map(lambda z: remover.transformWord(z.lower()), filter(lambda x: x, filter(lambda y: not(y in ";,.?\'\"·\n"),xs))))


def tokenize_with_accents(text):
    #add spaces around punct
    x = re.sub(PUNCTREGEX2, REP2, re.sub(PUNCTREGEX1, REP1, text.replace("\n", " \n ")))
    xs = x.split(' ')
    #remove empty elements
    return list(filter(lambda x: x, filter(lambda y: not(y in ";,.?\'\"·\n"),xs)))


