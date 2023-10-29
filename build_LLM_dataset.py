import json
with open("./datasets/LLM_fine_tune/instruction.txt","r") as f:
    instruction = f.read()
with open("./datasets/LLM_fine_tune/output.json","r") as f1:
    outputs = f1.readlines()
with open("./datasets/LLM_fine_tune/ICTPE_train.json","r") as f2:
    data = json.load(f2)
texts = [x["text"] for x in data]
dataset = []
for i in range(len(texts)):
    adata = {"instruction":instruction,"input":texts[i],"output":outputs[i]}
    dataset.append(adata)
with open("./datasets/LLM_fine_tune/LLM_sft_dataset.json","w") as f3:
    json.dump(dataset,f3)