import boto3
import uuid  # To generate a unique session ID
import logging
from botocore.config import Config
from botocore.exceptions import ClientError

# Set up logging for error handling
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def initialize_bedrock_agent_runtime():
    config = Config(
        region_name='us-west-2',
        retries={'max_attempts': 10000, 'mode': 'standard'}
    )
    return boto3.client('bedrock-agent-runtime', config=config)

def invoke_agent(agent_id, agent_alias_id, session_id, prompt):
    client = initialize_bedrock_agent_runtime()
    try:
        response = client.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            inputText=prompt,
        )
        
        completion = ""
        
        for event in response.get("completion", []):
            chunk = event["chunk"]
            completion += chunk["bytes"].decode()
        
        return completion if completion else "No response from the agent."

    except ClientError as e:
        logger.error(f"Couldn't invoke agent. {e}")
        return f"Error invoking agent: {e}"

def communicate_with_martha(user_message):
    agent_id = "EONIHWCKGF"
    alias_id = "DPCGGIXP5L"
    session_id = str(uuid.uuid4())
    return invoke_agent(agent_id, alias_id, session_id, user_message)
