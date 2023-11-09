path_to_original_llama_2_hf_dir="/root/autodl-tmp/LLM/llama2-7b-zh-ict_pretrained"
path_to_chinese_llama2_or_alpaca2_lora="/root/autodl-tmp/LLM/llama2-7b_ft_EE/sft_lora_model"
path_to_predictions="/root/autodl-tmp/Llama2_ft/output/EE_predictions.json"
path_to_input_data="/root/autodl-tmp/Llama2_ft/dataset/LLM_infer/EE_input.txt"
gpus="0"

python scripts/inference/inference_hf.py \
    --base_model "${path_to_original_llama_2_hf_dir}" \
    --lora_model "${path_to_chinese_llama2_or_alpaca2_lora}" \
    --tokenizer_path "${path_to_original_llama_2_hf_dir}" \
    --with_prompt \
    --predictions_file "${path_to_predictions}" \
    --data_file "${path_to_input_data}" \
    --gpus="${gpus}"