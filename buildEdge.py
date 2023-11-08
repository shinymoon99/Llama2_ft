# text
# id_locs
import json
import re
def getids(sentence):
    pattern=r'<(.*?)>'
    results = re.findall(pattern,sentence)

    return results
def buildedges(text,id_locs):
    edges = []
    sentences = text.split("。")
    for s in sentences:
        ids =getids(s)
        for i in range(len(ids)-1):
            edge = (id_locs[ids[i]],id_locs[ids[i+1]])
            edges.append(edge)
    return edges
with open("./output/atext.json","r",encoding="utf-8") as f1:
    datas = json.load(f1)

sedges=[]
for data in datas:
    tedges = buildedges(data["atext"],data["id_loc"])
    sedges.append(tedges)
print(sedges)
with open("./output/Edge_predictions.json","w") as f:
    json.dump(sedges,f)