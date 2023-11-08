from utils.evalEdge import find_best_matching
import json

def getIDLocs(node_list):
    ID_locs = {}
    for node in node_list:
        loc =[node["start"],node["end"]]
        ID = node["type_id"]
        ID_locs[ID]=loc
    return ID_locs
def buildEdge(edge_list,IDLocs):
    edges = []
    for edge in edge_list:
        start = IDLocs[edge[0]]
        end = IDLocs[edge[1]]
        edges.append((start,end))
    return edges
def getSpanAccuracy4Span(gold_list,test_list):
    '''
    :param gold_list [[(start,end),(3,4)]...[]]
    :return no_average_acc,num_of_prediction
    '''
    # gold_list: [(span_text,span)]
    correct_rate = 0
    total = 0
    macro_correct = 0
    for test_span, gold_span in zip(test_list, gold_list):
        #rate,num=calculate_span_accuracy(pred_sent,gold_sent)

        best_match,match_rate = find_best_matching(test_span,gold_span)

        correct_rate+=match_rate*len(best_match)
        total+=len(best_match)
    if total!=0:
        accuracy = correct_rate/total
    else :
        accuracy = 1
        
    return accuracy,total
datas = []
goldEdges = []   
with open("./dataset/ICTPE_v2/ICTPE_test.json","r",encoding="utf-8") as f1:
    datas=json.load(f1)
with open("./output/Edge_predictions.json","r",encoding="utf-8") as f:
    testEdges=json.load(f)
for data in datas:
    IDlocs=getIDLocs(data["node_list"])
    edges = buildEdge(data["edge_list"],IDlocs)
    goldEdges.append(edges)
rate_overall=getSpanAccuracy4Span(goldEdges,testEdges)
print(rate_overall)
