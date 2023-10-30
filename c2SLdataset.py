import json
def annotate_text_with_tags(text, tag_spans):
    result = ""
    for i in range(len(text)):
        
        for tag, spans in tag_spans.items():
            for span in spans:
                if i == span[0]:
                    result += f"<{tag}>"
                if i == span[1]:
                    result += f"</{tag}>"
        result += text[i]
    
    return result
# TODO: check if the tag_span has intersection
 
# text = "This is a sample text for tagging."
# tag_spans = {"status": [(2, 3), (4, 5)], "operation": [(6, 8), (9, 10)]}

# output = annotate_text_with_tags(text, tag_spans)
# print(output)
# input  
# output ["状态"：{(a,b),(c,d)},"操作":{(e,f),..}]
def convert_to_tag_span(node_list):
    tag_spans = {"操作":[],"状态":[],"条件":[],"判断":[]}
    t2c ={"operate":"操作","status":"状态","condition":"条件","check":"判断"}
    for node in node_list:
        type_tag = node["type"]
        text_span = node["text_span"]
        start = node["start"]
        end = node["end"]

        #print(type_tag)
        tag_spans[t2c[type_tag]].append((start, end))

    return tag_spans
input_dataset_file_path = "./dataset/ICTPE_v2/ICTPE_v2_editbefore.json"
output_dataset_file_path = "./dataset/LLM_fine_tune_SL/SL.json"

instruction_path = "./dataset/LLM_fine_tune_SL/instruction.txt"
with open("./dataset/LLM_fine_tune_SL/instruction.txt","r",encoding="utf-8") as f2:
    instruction = f2.read()

texts =[]
output_dataset = []
with open(input_dataset_file_path,"r",encoding="utf-8") as f:
    datas = json.load(f)
for data in datas:
    text = data["text"]
    tag_span=convert_to_tag_span(data["node_list"])
    output_data = annotate_text_with_tags(text,tag_spans=tag_span)
    output_dataset.append({"instruction":instruction,"input":text,"output":output_data})



with open(output_dataset_file_path,"w",encoding="utf-8") as f1:
    json.dump(output_dataset,f1,ensure_ascii=False)