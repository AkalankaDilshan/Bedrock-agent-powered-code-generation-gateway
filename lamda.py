import boto3
#from botocore.config import Config
import botocore.config
import json
from datetime import datetime

def generate_code_using_bedrock(message:str, language:str) -> str:
    promt_text = f'''
    Human: Write {language} code for the following instructions: {message}.
    Assistant: 
    '''
    body = {
        "prompt": promt_text,
        "max_tokens_to_sample": 2048,
        "temperature": 0.1,
        "top_k": 250,
        "top_p": 0.2,
        "stop_sequence": ["\n\nHuman:"]
    }
    
    try:
        bedrock = boto3.client("bedrock-runtime",region_name="eu-north-1", config = botocore.config.Config(read_timeout=300, retires = {'max_attempts':3}))
        response = bedrock.invoke_model(body=json.dump(body),modelId="qwen.qwen3-coder-30b-a3b-instruct")
        response_content = response.get('body').read().decode('utf-8')
        response_data = json.load(response_content)
        code = response_data["completion"].strip()
        return code
    
    except Exception as e:
        print("Error generating the code")
        return ""