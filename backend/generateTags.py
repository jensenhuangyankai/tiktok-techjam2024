import transformers
import torch
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

token=os.environ['hf_TOKEN']

model_id = "unsloth/llama-3-8b-Instruct-bnb-4bit"

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    token=token,
    device_map="auto",
)


def generateTagsfromList(tagList):
    messages = [
        {"role": "system", 
        "content": "You are a content creator that will help me figure out the best 6 related hashtags to put on my post. Do not repeat the input hashtags in the output. I have given you a list of input hashtags. Don’t add explanation beyond or before the python list output. Do not format it as a hashtag, rather as a string."
        },
        {"role": "user", 
        "content": str(tagList),
        },
        {"role": "assistant",
        "content": "['apple', 'dog', 'llama']"
        }
    ]

    terminators = [
        pipeline.tokenizer.eos_token_id,
        pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = pipeline(
        messages,
        max_new_tokens=256,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.1,
        top_p=0.9,
    )

    tags = outputs[0]["generated_text"][-1]['content']
    return tags

#print(generateTags(['apple', 'dog', 'llama']))