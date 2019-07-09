from remove_accents import Remover 
remover = Remover()



def read_tab_list(ipath):
    with open(ipath, 'r', encoding='utf-8') as f:
        xs = map(lambda x: x.split('\t'), f.read().strip().split('\n'))
        out = {}
        for x in xs:
            if len(x) > 1:
                inf = remover.transformWord(x[0].lower())
                lemma = x[1].lower()
                if inf in out:
                    if not(lemma in out[inf]):
    	                out[inf] = out[inf] + "," + lemma
                else:
                    out[inf] = lemma
            else:
                print(x)

        return out

lemmas = read_tab_list('no-accents.tab')

NU = '(ν)'
out = {}
for l,v in lemmas.items():
	if l.endswith(NU):
		nonu = l.replace(NU, '')
		out[nonu] = v
		out[nonu + 'ν'] = v
	else:
		out[l] = v

with open('no-accents.tab', 'w', encoding='utf-8') as f:
	for l,v in out.items():
		f.write(l + "\t" + v + "\n" )

print("done")	
