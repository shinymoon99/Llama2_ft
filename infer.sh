path_to_original_llama_2_hf_dir = /root/autodl-tmp/LLM/llama2-7b-zh-ict_pretrained
path_to_chinese_llama2_or_alpaca2_lora = /root/autodl-tmp/LLM/llama2-7b_pft/sft_lora_model
path_to_predictions = /root/autodl-tmp/LLAMA2_FT/output/predictions.json
path_to_input_data = /root/autodl-tmp/LLAMA2_FT/dataset/LLM_infer/input.txt
gpus ="0"
torchrun --nnodes 1 --nproc_per_node 1 python scripts/inference/inference_hf.py \
    --base_model ${path_to_original_llama_2_hf_dir} \
    --lora_model ${path_to_chinese_llama2_or_alpaca2_lora} \
    --tokenizer_path ${path_to_original_llama_2_hf_dir} \
    --with_prompt \
    --predictions_file ${path_to_predictions} \
    --data_file ${path_to_input_data} \
    --gpus ${gpus}