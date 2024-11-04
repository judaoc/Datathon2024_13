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

def get_claude_response(bedrock_client, data, ticker, temperature=0.0):
    if isinstance(data, dict):
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        json_prompt = (
            f"Voici les données JSON à analyser pour l'entreprise avec le ticker {ticker}:\n"
            f"```json\n{json_str}\n```\n"
            "Merci de fournir une analyse très brève de ces données financières. "
            "Utilise une police uniforme sous forme de texte normal, sans annoncer ce que tu fais."
        )
    else:
        json_prompt = data
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": json_prompt}],
        "temperature": temperature
    })
    response = bedrock_client.invoke_model(modelId='anthropic.claude-3-5-sonnet-20240620-v1:0', body=body)
    response_body = json.loads(response.get('body').read())
    return response_body['content'][0]['text']

def analyze_json_data(data, ticker):
    bedrock_client = initialize_bedrock()
    return get_claude_response(bedrock_client, data, ticker)

def get_claude_response_articles(bedrock_client, data, ticker, temperature=0.0):
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    json_prompt = (
        f"Voici des articles à propose de l'entreprise {ticker}:\n"
        f"```json\n{json_str}\n```\n"
        "Retourne moi les 3 articles les plus pertinents d'un point de vu financier, séparer par un espace et en commençant l'indexisation par la position 0."
        "Tu ne peux pas envoyer de lettres ou de texte. Si rien de convient retourne rien."
    )
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": json_prompt}],
        "temperature": temperature
    })
    response = bedrock_client.invoke_model(modelId='anthropic.claude-3-5-sonnet-20240620-v1:0', body=body)
    response_body = json.loads(response.get('body').read())
    return response_body['content'][0]['text']

def get_claude_response_all_articles(bedrock_client, data, temperature=0.0):
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    json_prompt = (
        f"Voici des articles à propos de la finance:\n"
        f"```json\n{json_str}\n```\n"
        "Retourne moi les 5 articles les plus pertinents d'un point de vu financier, séparer par un espace et en commençant l'indexisation par 0."
        "Tu ne peux pas envoyer de lettres ou de texte. Si rien ne te convient retourne rien."
    )
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": json_prompt}],
        "temperature": temperature
    })
    response = bedrock_client.invoke_model(modelId='anthropic.claude-3-5-sonnet-20240620-v1:0', body=body)
    response_body = json.loads(response.get('body').read())
    return response_body['content'][0]['text']

def analyzeSpecificArticles(data, ticker):
    bedrock_client = initialize_bedrock()
    return get_claude_response_articles(bedrock_client, data, ticker).split()

def analyzeArticles(data):
    bedrock_client = initialize_bedrock()
    return get_claude_response_all_articles(bedrock_client, data).split()