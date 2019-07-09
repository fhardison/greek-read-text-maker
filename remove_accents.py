from greek_accentuation.characters import base

import betacode.conv
import string

def removeNoAscii(w):
    return ''.join(filter(lambda x: not(x in "*abcdefghijklmnopqrstuvwxyz"), w))

class Remover:
    def transformWord(self, w):
        return "".join(map(lambda x: base(x), w))
    def removeWithBeta(self, w):
        return betacode.conv.beta_to_uni(removeNoAscii(betacode.conv.uni_to_beta(w)))

if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    remover = Remover()
    raw = ''
    with open(args[0], 'r', encoding='utf-8') as f:
        raw = f.read()
    with open(args[1], 'w', encoding='utf-8') as f:
        f.write(remover.transformWord(raw))
