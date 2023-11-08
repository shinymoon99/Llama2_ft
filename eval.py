import numpy as np
from scipy.optimize import linear_sum_assignment
import json
def span_similarity(span1, span2):
    # Define a similarity score between two spans.
    # You can use various metrics such as Jaccard similarity, overlap ratio, etc.
    # For example, you can calculate Jaccard similarity:
    intersection = len(set(span1) & set(span2))
    union = len(set(span1) | set(span2))
    return intersection / union if union > 0 else 0

def calculate_similarity_matrix(test_list, gold_list):
    # Calculate a similarity matrix where each cell (i, j) represents
    # the similarity score between test_list[i] and gold_list[j].
    similarity_matrix = np.zeros((len(test_list), len(gold_list)))
    for i, test_span in enumerate(test_list):
        for j, gold_span in enumerate(gold_list):
            similarity_matrix[i][j] = span_similarity(test_span, gold_span)
    return similarity_matrix
def find_best_matching(test_list, gold_list):
    # Example usage with different lengths:
    # test_list = [(0, 5), (10, 15), (20, 25)]
    # gold_list = [(2, 7), (11, 16)]

    # best_matching, match_rate = find_best_matching(test_list, gold_list)
    # print("Best Matching:", best_matching)
    # print("Overall Match Rate:", match_rate)


    # Calculate the similarity matrix.
    similarity_matrix = calculate_similarity_matrix(test_list, gold_list)
    
    # Use the Hungarian algorithm to find the optimal assignment that maximizes the overall match rate.
    row_indices, col_indices = linear_sum_assignment(-similarity_matrix)
    
    # Calculate the overall match rate.
    if len(test_list)>0:
        match_rate = similarity_matrix[row_indices, col_indices].sum()/len(test_list)
    else:
        match_rate = 0
    # Create a dictionary to represent the best matching.
    best_matching = {}
    for i, j in zip(row_indices, col_indices):
        if i < len(test_list) and j < len(gold_list):
            best_matching[test_list[i]] = gold_list[j]
    
    return best_matching, match_rate
def getSpanAccuracy4Span(gold_list,test_list):
    '''
    :param gold_list [[(start,end),(3,4)]...[]]
    :return no_average_acc,num_of_prediction
    '''
    # gold_list: [(span_text,span)]
    correct_rate = 0
    total = 0
    for test_span, gold_span in zip(test_list, gold_list):
        #rate,num=calculate_span_accuracy(pred_sent,gold_sent)

        best_match,match_rate = find_best_matching(test_span,gold_span)

        correct_rate+=match_rate*len(best_match)
        total+=len(best_match)
    if total!=0:
        accuracy = correct_rate/total
    else :
        accuracy = 0
    return accuracy,total   
def getTypeLoc(typestr,typelocs):
    locs = []
    for typeloc in typelocs:
        loc4example = []
        if typestr in typeloc:
            loc4example.extend([tuple(sublist) for sublist in typeloc[typestr]])
        locs.append(loc4example)
    return locs

def buildTypeLocFromICTPE(gdata):
    labels = ["status","operate","check","condition"]
    e2c = {"status":"状态","operate":"操作","check":"判断","condition":"条件"}
    typelocs = {}
    for l in labels:
        locs4label= []
        for data in gdata:
            locs4data = []
            for node in data["node_list"]:
                if node["type"]==l:
                    locs4data.append((node["start"],node["end"]))
            locs4label.append(locs4data)
        typelocs[e2c[l]]=locs4label
    return typelocs
def calculate_overall(accs):
    nums=0
    acc_all=0
    for acc,num in accs:
        nums=nums+num
        acc_all=acc_all+num*acc
    acc_overall= acc_all/nums
    return acc_overall
with open("./dataset/ICTPE_v2/ICTPE_test.json",encoding="utf-8") as f:
    gdata =json.load(f)
with open("./output/predictions_loc.json",encoding="utf-8") as f1:
    typelocs = json.load(f1)

goldtypelocs = buildTypeLocFromICTPE(gdata)
class_labels = ["状态","操作","判断","条件"]

print(goldtypelocs)
# get predictions

locs = {}
for c in class_labels:
    loc =getTypeLoc(c,typelocs)
    locs[c]=loc
print(locs)
acc = []
for c in class_labels:
    accuracy =getSpanAccuracy4Span(goldtypelocs[c],test_list=locs[c])
    acc.append(accuracy)
overall = calculate_overall(acc)
print(acc)
print(overall)


