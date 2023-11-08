import json
import re

def buildAText(id_loc,text):
    id_loc_sorted = dict(sorted(id_loc.items(), key=lambda item: item[1][0]))
    text_pivot = 0
    atext =""
    ids = []
    locs = []
    for k,v in id_loc_sorted.items():
        ids.append(k)
        locs.append(v)
    pre_start =0
    for i,x in enumerate(ids):
        
        atext=atext+text[pre_start:locs[i][0]]
        atext=atext+f'<{x}>'
        pre_start=locs[i][1]
    atext=atext+text[pre_start:]
    return atext
def buildID(labels,text):
    """
    :param label {"条件":[(),()],"操作":}
    return
    :param text
    :param id_loc {"条件i":(),..}
    """    
    id_loc = {}
    for k,v in labels.items():
        if len(v)==0:
            pass
        for i,loc in enumerate(v):
            tid = k+str(i)
            id_loc[tid]=tuple(loc)
    return id_loc
texts = []
labels = []
atexts = []
id_locs = []
with open("./dataset/ICTPE_v2/ICTPE_test.json","r",encoding="utf-8") as f:
    data = json.load(f)
texts= [x["text"] for x in data]
with open("./output/predictions_loc.json","r",encoding="utf-8") as f2:
    labels = json.load(f2)
for i,text in enumerate(texts):
    id_loc =buildID(labels[i],text)
    atext =buildAText(id_loc,text)
    atexts.append(atext)
    id_locs.append(id_loc)
json_atexts = []
for i,t in enumerate(atexts):
    json_atexts.append({"text":texts[i],"atext":t,"id_loc":id_locs[i]})
with open("./output/atext.json","w",encoding="utf-8") as f1:
    json.dump(json_atexts,f1)