import streamlit as st
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
        json_prompt = f"Voici les données JSON à analyser:\njson\n{json_str}\n\nMerci de fournir une analyse très brève de ces données financières."
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

def main():    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'bedrock_client' not in st.session_state:
        st.session_state.bedrock_client = initialize_bedrock()
    
    if 'json_data' not in st.session_state:
        st.session_state.json_data = None

    # Upload du fichier JSON
    uploaded_file = st.file_uploader("Choisissez un fichier JSON", type=["json"])
    if uploaded_file is not None:
        try:
            st.session_state.json_data = json.loads(uploaded_file.read().decode())

            # Analyser le fichier JSON dès son upload
            with st.chat_message("assistant"):
                with st.spinner("Analyse en cours..."):
                    try:
                        response = get_claude_response(st.session_state.bedrock_client, st.session_state.json_data)
                        st.markdown(response)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response
                        })
                    except Exception as e:
                        st.error(f"Erreur lors de l'analyse: {str(e)}")
        except json.JSONDecodeError:
            st.error("Le fichier n'est pas un JSON valide")
            st.session_state.json_data = None

if __name__ == "__main__":
    st.set_page_config(page_title="Claude", page_icon="🤖")
    main()