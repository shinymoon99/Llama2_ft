import json
output_datas =[]
input_file_path = "./dataset/LLM_fine_tune_SL/ICTPE_test.json"
output_file_path = "./output/output.txt"
with open(input_file_path,"r",encoding="utf-8") as f:
    datas = json.load(f)
for data in datas:
    text = data["instruction"].replace("\n","")+data["input"]
    output_datas.append(text)
# File path to write to

# Open the file in write mode
with open(output_file_path, 'w',encoding="utf-8") as file:
    for item in output_datas:
        file.write(item + '\n')
