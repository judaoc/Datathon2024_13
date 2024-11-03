import boto3
import json
from botocore.config import Config

def initialize_bedrock():
    config = Config(
        region_name='us-west-2',
        retries={'max_attempts': 9, 'mode': 'standard'}
    )
    bedrock = boto3.client(service_name='bedrock-runtime', config=config)
    return bedrock

def get_claude_response(bedrock_client, data, temperature=0.0):
    if isinstance(data, dict):
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        json_prompt = f"Voici les données JSON à analyser:\n```json\n{json_str}\n```\nMerci de fournir une analyse très brève de ces données financières. Utilise une police uniforme sous forme de texte normal, sans annoncer ce que tu fais."
    else:
        json_prompt = data
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": json_prompt}],
        "temperature": temperature
    })
    response = bedrock_client.invoke_model(modelId='anthropic.claude-3-sonnet-20240229-v1:0', body=body)
    response_body = json.loads(response.get('body').read())
    return response_body['content'][0]['text']

def load_json_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def analyze_json(filepath):
    json_data = load_json_from_file(filepath)
    bedrock_client = initialize_bedrock()
    return get_claude_response(bedrock_client, json_data)
