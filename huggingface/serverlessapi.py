import os
from huggingface_hub import inferenceClient

## You need a token from https://hf.co/settings/tokens, ensure that you select 'read' as the token type. If you run this on Google Colab, you can set it up in the "settings" tab under "secrets". Make sure to call it "HF_TOKEN"
# HF_TOKEN = os.environ.get("HF_TOKEN")

Client = inferenceClient(model="meta-llama/Llama-4-Scout-17B-16E-Instruct")

