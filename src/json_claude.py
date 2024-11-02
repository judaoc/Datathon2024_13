import boto3
import json
from botocore.config import Config

def initialize_bedrock():
    config = Config(
        region_name='us-west-2',
        retries={
            'max_attempts': 3,
            'mode': 'standard'
        }
    )
    
    bedrock = boto3.client(
        service_name='bedrock-runtime',
        config=config
    )
    return bedrock

def get_claude_response(bedrock_client, data, temperature=0.7):
    if isinstance(data, dict):
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        json_prompt = f"Voici les données JSON à analyser:\n```json\n{json_str}\n```\nMerci de fournir une analyse très brève de ces données financières. Assure toi aussi de soigner ta mise en page."
    else:
        json_prompt = data

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 200000,
        "messages": [
            {
                "role": "user",
                "content": json_prompt
            }
        ],
        "temperature": temperature
    })
    
    response = bedrock_client.invoke_model(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        body=body
    )
    
    response_body = json.loads(response.get('body').read())
    return response_body['content'][0]['text']

def load_json_from_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        return json_data
    except FileNotFoundError:
        print(f"Erreur : Le fichier {filepath} n'a pas été trouvé.")
        return None
    except json.JSONDecodeError:
        print("Le contenu du fichier n'est pas un JSON valide")
        return None

def analyze_json(filepath = '..\data\AAPL_AnnualFinancialReport.json'):
    json_data = load_json_from_file(filepath)
    
    if json_data is not None:
        bedrock_client = initialize_bedrock()
        try:
            response = get_claude_response(bedrock_client, json_data)
            return response  # Retourne la réponse au lieu de l'imprimer
        except Exception as e:
            return f"Erreur lors de l'analyse : {str(e)}"
    else:
        return "Aucune donnée JSON valide n'a été chargée."