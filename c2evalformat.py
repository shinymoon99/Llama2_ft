import json
import re
import hanlp


def extract_labels(input_text, source_text):
    label_pattern = r'<([^>]+)>(.*?)</\1>'
    label_matches = re.finditer(label_pattern, input_text)

    label_positions = {}
    
    for match in label_matches:
        label_type = match.group(1)
        label_content = match.group(2)
        start_index = source_text.find(label_content)
        end_index = start_index + len(label_content)
        
        if label_type in label_positions:
            label_positions[label_type].append((start_index, end_index))
        else:
            label_positions[label_type] = [(start_index, end_index)]
    
    return label_positions

# input_text = "<条件>在批量配置LDP Keychain认证或LDP MD5认证后</条件>，<操作>指定LDP对等体 **ifname=10.1.1.1** 不进行认证</操作>。"
# source_text = "在批量配置LDP Keychain认证或LDP MD5认证后，指定LDP对等体 **10.1.1.1** 不进行认证。"

# label_positions = extract_labels(input_text, source_text)
# print(label_positions)

def extract_label_positions(input_text, source_text):
    label_pattern = r'<([^>]+)>(.*?)(</\1>)'
    temp_text = input_text
    label_positions = {}
    # 找到第一个命中pattern直到没有为止
    match = re.search(label_pattern,temp_text)
    while(match!=None):
        label_type = match.group(1)
        label_content = match.group(2)
        start,end = (match.start(2)-len(label_type)-2,match.end(2)-len(label_type)-2)
        temp_text = temp_text[:match.start(1)-1]+label_content+temp_text[match.end(3):]
        if source_text[start:end]==label_content:
            # 用标签类型更新位置字典
            if label_type in label_positions:
                label_positions[label_type].append((start, end))
            else:
                label_positions[label_type] = [(start, end)]        
        match = re.search(label_pattern,temp_text)
    return label_positions    
    # 获取pattern位置，文本在源文本位置，删除pattern，修改temp_text
    

def filter_no_signal_cond(locs,text):
    """    
    : param locs = [(),()]
    : param text = str
    """
    flocs = []
    pattern = "(当[^，。]*|[^，。]*后|为[^，。]*|[^，。]*时|[^，。]*前|如果[^,。]|假如[^,。]|在[^，。]*)"
    for loc in locs:
        if re.search(pattern,text[loc[0]:loc[1]]):
            flocs.append(loc)
        else:
            pass
    return flocs
def filter_op(locs,text):
    """    
    : param locs = [(),()]
    : param text = str
    """
    flocs = []
    ttexts = []
    results = []
    HanLP = hanlp.pipeline() \
    .append(hanlp.utils.rules.split_sentence, output_key='sentences') \
    .append(hanlp.load('FINE_ELECTRA_SMALL_ZH'), output_key='tok') \
    .append(hanlp.load('CTB9_CON_ELECTRA_SMALL'), output_key='con', input_key='tok')
    for loc in locs:
        ttext=(text[loc[0]:loc[1]])
        result =HanLP(ttext)["con"][0][0].label()
        results.append(result)
    for i,loc in enumerate(locs):
        if results[i]=="LCP":
            pass
        else:
            flocs.append(loc)
    return flocs
# input_text = "<条件>在批量配置LDP Keychain认证或LDP MD5认证后</条件>，<操作>指定LDP对等体 **ifname=10.1.1.1** 不进行认证</操作>。"
# source_text = "在批量配置LDP Keychain认证或LDP MD5认证后，指定LDP对等体 **10.1.1.1** 不进行认证。"

# label_positions = extract_label_positions(input_text, source_text)
# print(label_positions)
datas = []
texts = []

with open("./output/predictions.json","r",encoding="utf-8") as f:
    prdictions = json.load(f)
for p in prdictions:
    datas.append(p["Output"])
with open("./dataset/ICTPE_v2/ICTPE_test.json","r",encoding="utf-8") as f1:
    procedures = json.load(f1)
for p in procedures:
    texts.append(p["text"])
labels_sentence = []
length = 0
for i,data in enumerate(datas):
    labels =extract_label_positions(data,texts[i])
    labels_sentence.append(labels)
    length_all = [len(v) for k,v in labels.items()]
    length =length+ sum(length_all)
# 使用规则对于子句进行过滤
# 条件
for i,labels in enumerate(labels_sentence):
    if "条件" in labels:
        labels["条件"]=filter_no_signal_cond(labels["条件"],texts[i])
    if "操作" in labels:
        labels["操作"]=filter_op(labels["操作"],texts[i])        
length1 =0
for labels in labels_sentence:
    length_all = [len(v) for k,v in labels.items()]
    length1 =length1+ sum(length_all)
#print(labels_sentence)
print(f"{length} {length1}")
with open("./output/predictions_loc.json","w",encoding="utf-8") as f2:
    json.dump(labels_sentence,f2)   