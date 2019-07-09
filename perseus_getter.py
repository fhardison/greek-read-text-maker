import requests
import xml.etree.ElementTree as ET

URL = "http://www.perseus.tufts.edu/hopper/xmlmorph?lang=greek&lookup={0}"

def doRequest(w):
    r = requests.get(URL.format(w))
    xml = ET.fromstring(r.text)
    forms = {}
    for x in xml.iter('analysis'):
        lemma = x.find('lemma').text
        expanded = x.find('expandedForm').text
        form = x.find('form').text
        if form in forms:
            if not(lemma in forms[form]): 
                forms[form].append(lemma)
        else:
            forms[form] = [lemma]
    return forms

def get_unknown_words(ws):
    out = {}
    for w in ws:
        print('getting: ' + w)
        res = doRequest(w)
        print("recieved data")
        for k, v in res.items():
            if k in out:
                out[k] = list(set(out[k] + v))
            else:
                out[k] = v
    return out

def format_output(data):
    out = [x + "\t" + ",".join(y) for x,y in data.items()]
    return "\n".join(out)



if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    print("input file should be in beta codes, one word per line")
    words = None
    with open(args[0], 'r') as f:
        words = map(lambda x: x.strip(), f.read().split("\n"))
    output = format_output(get_unknown_words(words))
    with open(args[1], 'w', encoding = 'utf-8') as f:
        f.write(output)
    print("done")
