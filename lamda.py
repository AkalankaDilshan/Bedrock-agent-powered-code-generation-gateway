import boto3
import botocore.config
import json
from datetime import datetime

def generate_code_using_bedrock(message:str, language:str) -> str:
    promt_text = f'''
    Human: Write {language} code for the following instructions: {message}.
    Assistant: 
    '''
    