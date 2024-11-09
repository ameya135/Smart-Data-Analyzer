from vllm import LLM, SamplingParams
from huggingface_hub import snapshot_download
from vllm.lora.request import LoRARequest

lora_path = snapshot_download(repo_id="Kyo135/llama3_1text2sql")
llm = LLM(model="unsloth/Llama-3.2-3B-Instruct", enable_lora=True)

sampling_params = SamplingParams(
    temperature=0,
    max_tokens=256,
    stop_token_ids=["### Response:"]
)

prompts = [
    "<|begin_of_text|><|start_header_id|>user<|end_header_id|> Below are sql tables schemas paired with instruction that describes a task. Using valid SQL, write a response that appropriately completes the request for the provided tables. ### Instruction: Name the home team for carlton away team ### Input: CREATE TABLE table_name_77 ( home_team VARCHAR, away_team VARCHAR ) ### Response:"
]

outputs = llm.generate(
    prompts,
    sampling_params,
    lora_request=LoRARequest("sql_adapter", 1, lora_path)
)

print(outputs)