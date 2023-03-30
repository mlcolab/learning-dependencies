# This scripts sends a test request to the Bloom language model

from transformers import AutoTokenizer,AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("bigscience/bloom-1b7")
tokenizer = AutoTokenizer.from_pretrained("bigscience/bloom-1b7", device_map="auto")

text_prompt ="What should I know to understand singular value decomposition?"
inputs = tokenizer(text_prompt, return_tensors="pt").input_ids.to("cuda")
result = model.generate(inputs,max_length=200,top_k=0,temperature=0.5)
print(tokenizer.decode(result[0], truncate_before_pattern=[r"\n\n^#","^'''","\n\n\n"]))