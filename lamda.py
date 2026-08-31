import boto3
import botocore.config
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# application-specific inference profiles
MODEL_ID = "global.anthropic.claude-haiku-4-5-20251001-v1:0"

def generate_code_using_bedrock(message:str, language:str) -> str:
    
    promt_text = f"Write {language} code for following instructions: {message}."
    body = {
        'anthropic_version': 'bedrock-2023-05-31',
        'max_tokens': 2048,
        'temperature': 0.1,
        'top_k': 250,
        #"top_p": 0.2,
        #"stop_sequences": ["..."]
        'messages': [{ 'role': 'user', 'content': promt_text}]
        
    }
    
    try:
        bedrock = boto3.client("bedrock-runtime",region_name="us-east-1", config = botocore.config.Config(read_timeout=300, retries = {'max_attempts':3}))
        response = bedrock.invoke_model(body=json.dumps(body),modelId= MODEL_ID)
        response_content = response.get('body').read().decode('utf-8')
        response_data = json.loads(response_content)
        code = response_data["content"][0]["text"].strip()
        return code
    
    except Exception as e:
        logger.error(f'Eror Generating code: {e}')
        raise

def save_code_to_s3_bucket(code, s3_bucket, s3_key):
    s3 = boto3.client('s3')
    
    try:
        s3.put_object(Bucket= s3_bucket, Key= s3_key, Body= code)
        print("Code save to s3")
        
    except Exception as e:
        print("Error when saving the code to s3")
        
        
def lambda_handler(event, context):
    event= json.loads(event['body'])
    message = event['message']
    language = event['language']
    print(message, language)
    
    generate_code = generate_code_using_bedrock(message, language)
    
    # if generate_code:
    #     current_time = datetime.now().strftime('%H:%M:%S')
    #     s3_key = f'code-output/{current_time}.py' # meka change krnna oni
    #     s3_bucket = 'bedrock-codegen-bucket-3456' #my bucke name
        
    #     save_code_to_s3_bucket(s3_bucket=s3_bucket,s3_key=s3_key, code= generate_code)
    
    # else:
    #     print("No code was generated")

    return {
        'statusCode':200,
        'body': json.dumps({
            'message': 'Code generation Complete',
            'code': generate_code
            })
    }
        