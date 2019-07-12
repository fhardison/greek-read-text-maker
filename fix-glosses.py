import re

def read_tab_list(ipath):
    with open(ipath, 'r', encoding='utf-8') as f:
        xs = map(lambda x: x.split('\t'), f.read().strip().split('\n'))
        return xs
        out = {}
        for x in xs:
            if len(x) > 1:
                inf = x[0].lower()
                lemma = x[1].lower()
                if inf in out:
                    out[inf] = out[inf] + "," + lemma 
                else:
                    out[inf] = lemma
            else:
                print(x)

        return out

lemmas = read_tab_list('gloss-dict.tab')

from remove_accents import Remover 
remover = Remover()


noaccents =[]

for l in lemmas:
    if len(l) > 1:
        noaccents.append([l[0].replace(":", "").replace("-",""),l[1]])



out ={}

# add limit check, if glossrs more thsn 4, tske first 3
def nuke_empty(gl):
    parts = re.split(r' :: ', gl)
    out = []
    for p in parts:
        if not(p.strip() == ""):
            out.append(p)
    ret = list(set(out))
    if len(ret) > 3:
        ret = ret[0:2]
    return " | ".join(ret)

for n in noaccents:
    if n[0] in out:
        out[n[0]] = out[n[0]] + nuke_empty(n[1])
    else:
        out[n[0]] = nuke_empty(n[1])




with open('gloss-no-acccents.tab', 'w', encoding='utf-8') as f:
	for l,v in out.items():
		f.write(l + "\t" + v + "\n" )

print("done")	
