import boto3
import os
import json
import streamlit as st
from dotenv import load_dotenv
import base64
import time
import random

# Load environment variables
load_dotenv()

def get_bedrock_client(service_name="bedrock-runtime"):
    """
    Initialize and return a Bedrock client.
    
    Args:
        service_name (str): The AWS service name to connect to
                           ("bedrock-runtime" or "bedrock-agent-runtime")
    
    Returns:
        boto3.client: The initialized Bedrock client
    """
    try:
        session = boto3.Session(
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )
        client = session.client(service_name=service_name)
        return client
    except Exception as e:
        st.error(f"Error initializing {service_name} client: {str(e)}")
        return None

def get_secret():
    """
    Retrieve agent configuration from AWS Secrets Manager.
    
    Returns:
        dict: The secret containing agent configurations
    """
    secret_name = os.getenv("AWS_SECRET_NAME")
    region_name = os.getenv("AWS_REGION", "us-east-1")
    
    if not secret_name:
        return None
    
    try:
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        
        # Get the secret value
        response = client.get_secret_value(SecretId=secret_name)
        
        # Decode the secret if it's binary
        if 'SecretString' in response:
            secret = response['SecretString']
            secret_data = json.loads(secret)
            return secret_data
        else:
            decoded_binary_secret = base64.b64decode(response['SecretBinary'])
            secret_data = json.loads(decoded_binary_secret)
            return secret_data
            
    except Exception as e:
        print(f"Error retrieving secret: {str(e)}")
        return None

def load_agent_config():
    """
    Load agent configuration from AWS Secrets Manager.
    
    Returns:
        list: List of agent configurations
    """
    # Try to get configuration from Secrets Manager
    secret = get_secret()
    
    if secret:
        # Check if the secret has the original 'agents' key format
        if 'agents' in secret:
            agents = secret['agents']
            return agents
        
        # Handle the new flat key-value format
        agents = []
        
        # Define the agent names based on the keys in the secret
        agent_mapping = {
            'single_agent': 'Single Agent',
            'multi_agent': 'Multi Agent'
        }
        
        # Create agent entries from the flat structure
        for base_name, display_name in agent_mapping.items():
            id_key = f"{base_name}_id"
            alias_key = f"{base_name}_alias"
            
            if id_key in secret and alias_key in secret:
                agents.append({
                    "id": secret[id_key],
                    "alias_id": secret[alias_key],
                    "name": display_name
                })
        
        if agents:
            return agents
        else:
            print("Secret retrieved but couldn't extract agent configurations")
    
    # If no agents found in Secrets Manager, use demo values
    agents = [
        {"id": "agent1", "alias_id": "TSTALIASID", "name": "General Assistant"},
        {"id": "agent2", "alias_id": "TSTALIASID", "name": "Data Analyst"},
        {"id": "agent3", "alias_id": "TSTALIASID", "name": "Code Helper"}
    ]
    
    return agents

def list_bedrock_agents():
    """
    List all available Bedrock agents in the account.
    
    Returns:
        list: List of agent information
    """
    try:
        client = boto3.client('bedrock-agent', region_name=os.getenv("AWS_REGION", "us-east-1"))
        response = client.list_agents()
        
        agents = []
        for agent in response.get('agents', []):
            # Get aliases for this agent
            alias_response = client.list_agent_aliases(
                agentId=agent['agentId']
            )
            
            agent_info = {
                'id': agent['agentId'],
                'name': agent['agentName'],
                'aliases': [{'id': alias['agentAliasId'], 'name': alias['agentAliasName']} 
                           for alias in alias_response.get('agentAliases', [])]
            }
            agents.append(agent_info)
            
        return agents
    except Exception as e:
        # Don't show error in UI since this is optional functionality
        # Just log to console for debugging
        print(f"Error listing agents: {str(e)}")
        return []

def invoke_bedrock_agent(agent_id, agent_alias_id, prompt, session_id=None, enable_trace=True):
    """
    Invoke a Bedrock agent with the given prompt.
    
    Args:
        agent_id (str): The ID of the Bedrock agent
        agent_alias_id (str): The alias ID of the Bedrock agent
        prompt (str): The user prompt to send to the agent
        session_id (str, optional): Session ID for conversation context
        enable_trace (bool, optional): Whether to enable trace information
    
    Returns:
        dict: Contains the agent's response and trace information if enabled
    """
    max_retries = 3
    retry_count = 0
    base_delay = 2  # Base delay in seconds
    
    try:
        client = get_bedrock_client("bedrock-agent-runtime")
        if not client:
            return {"completion": "Error: Could not initialize Bedrock client"}
        
        if not session_id:
            session_id = f"streamlit-session-{hash(prompt)}"
        
        while retry_count <= max_retries:
            try:
                with st.spinner("Waiting for agent response..."):
                    # Enable trace information if requested
                    invoke_params = {
                        "agentId": agent_id,
                        "agentAliasId": agent_alias_id,
                        "sessionId": session_id,
                        "inputText": prompt
                    }
                    
                    if enable_trace:
                        invoke_params["enableTrace"] = True
                    
                    # Log the parameters being sent
                    print(f"DEBUG - Invoking agent with params: {json.dumps(invoke_params, default=str)}")
                    
                    response = client.invoke_agent(**invoke_params)
                    
                    # Log the entire raw response structure (with limited depth for readability)
                    print("DEBUG - Beginning of full response dump")
                    print("=" * 80)
                    
                    # Create a custom JSON encoder to handle non-serializable objects
                    class CustomEncoder(json.JSONEncoder):
                        def default(self, obj):
                            try:
                                return super().default(obj)
                            except TypeError:
                                return str(obj)
                    
                    # Function to recursively process the response with depth limit
                    def process_response(obj, current_depth=0, max_depth=3):
                        if current_depth >= max_depth:
                            if isinstance(obj, dict):
                                return {k: "..." for k in obj.keys()}
                            elif isinstance(obj, list):
                                return ["..."] if obj else []
                            else:
                                return obj
                        
                        if isinstance(obj, dict):
                            return {k: process_response(v, current_depth + 1, max_depth) for k, v in obj.items()}
                        elif isinstance(obj, list):
                            return [process_response(item, current_depth + 1, max_depth) for item in obj[:5]]  # Limit to first 5 items
                        else:
                            return obj
                    
                    # Process and print the response
                    processed_response = process_response(response)
                    print(json.dumps(processed_response, indent=2, cls=CustomEncoder))
                    print("=" * 80)
                    print("DEBUG - End of full response dump")
                    
                    # Log the raw response keys
                    print(f"DEBUG - Response keys: {list(response.keys())}")
                    
                    # Extract the completion from the response
                    completion = ""
                    
                    # The response contains an EventStream in the 'completion' field
                    # We need to iterate through it to get all chunks
                    completion_events = []
                    for event in response.get("completion", []):
                        completion_events.append(event)  # Store for later analysis
                        print(f"DEBUG - Event keys: {list(event.keys() if isinstance(event, dict) else [])}")
                        
                        # Check if this event contains a chunk
                        if "chunk" in event:
                            chunk = event["chunk"]
                            if "bytes" in chunk:
                                completion += chunk["bytes"].decode("utf-8")
                        
                        # Check if this event contains trace information
                        if "trace" in event:
                            print(f"DEBUG - Found trace in event")
                            trace_data = event["trace"]
                            print(f"DEBUG - Trace keys: {list(trace_data.keys() if isinstance(trace_data, dict) else [])}")
                    
                    # Log all completion events for analysis
                    print(f"DEBUG - Found {len(completion_events)} completion events")
                    for i, event in enumerate(completion_events):
                        print(f"DEBUG - Completion event {i} keys: {list(event.keys() if isinstance(event, dict) else [])}")
                        processed_event = process_response(event)
                        print(f"DEBUG - Completion event {i} content: {json.dumps(processed_event, indent=2, cls=CustomEncoder)}")
                
                if not completion:
                    # Try alternative response format
                    completion = response.get("output", {}).get("text", "No response from agent")
                
                # Prepare the result with completion
                result = {
                    "completion": completion
                }
                
                # Extract and combine trace information from all events
                combined_trace = {}
                
                # Process all trace events to build a comprehensive trace structure
                for event in completion_events:
                    if "trace" in event:
                        trace_data = event["trace"]
                        
                        # Extract the inner trace if it exists
                        if "trace" in trace_data:
                            inner_trace = trace_data["trace"]
                            
                            # Process different trace types
                            for key, value in inner_trace.items():
                                # Initialize the key in combined_trace if it doesn't exist
                                if key not in combined_trace:
                                    combined_trace[key] = value
                                elif isinstance(combined_trace[key], dict) and isinstance(value, dict):
                                    # Merge dictionaries for the same trace type
                                    combined_trace[key].update(value)
                        
                        # Process collaborator information
                        if "collaboratorName" in trace_data:
                            if "collaborators" not in combined_trace:
                                combined_trace["collaborators"] = {}
                            
                            collab_name = trace_data["collaboratorName"]
                            if collab_name not in combined_trace["collaborators"]:
                                combined_trace["collaborators"][collab_name] = []
                            
                            # Add this trace to the collaborator's traces
                            if "trace" in trace_data:
                                combined_trace["collaborators"][collab_name].append(trace_data["trace"])
                
                # Add orchestration trace if available
                for event in completion_events:
                    if "trace" in event and "trace" in event["trace"]:
                        inner_trace = event["trace"]["trace"]
                        if "orchestrationTrace" in inner_trace:
                            if "orchestrationTrace" not in combined_trace:
                                combined_trace["orchestrationTrace"] = inner_trace["orchestrationTrace"]
                            elif isinstance(combined_trace["orchestrationTrace"], dict) and isinstance(inner_trace["orchestrationTrace"], dict):
                                combined_trace["orchestrationTrace"].update(inner_trace["orchestrationTrace"])
                
                # Add routing classifier trace if available
                for event in completion_events:
                    if "trace" in event and "trace" in event["trace"]:
                        inner_trace = event["trace"]["trace"]
                        if "routingClassifierTrace" in inner_trace:
                            if "routingClassifierTrace" not in combined_trace:
                                combined_trace["routingClassifierTrace"] = inner_trace["routingClassifierTrace"]
                            elif isinstance(combined_trace["routingClassifierTrace"], dict) and isinstance(inner_trace["routingClassifierTrace"], dict):
                                combined_trace["routingClassifierTrace"].update(inner_trace["routingClassifierTrace"])
                
                # Add the combined trace to the result if we found any trace data
                if combined_trace:
                    result["trace"] = combined_trace
                    print(f"DEBUG - Added combined trace to result with keys: {list(combined_trace.keys())}")
                    
                    # Log specific trace components for debugging
                    if "orchestrationTrace" in combined_trace:
                        print(f"DEBUG - OrchestrationTrace keys: {list(combined_trace['orchestrationTrace'].keys())}")
                    if "routingClassifierTrace" in combined_trace:
                        print(f"DEBUG - RoutingClassifierTrace keys: {list(combined_trace['routingClassifierTrace'].keys())}")
                    if "collaborators" in combined_trace:
                        print(f"DEBUG - Found traces for collaborators: {list(combined_trace['collaborators'].keys())}")
                else:
                    print(f"DEBUG - No trace data found in response")
                
                return result
                
            except Exception as e:
                if "throttlingException" in str(e) and retry_count < max_retries:
                    retry_count += 1
                    # Calculate delay with exponential backoff and jitter
                    delay = (base_delay * (2 ** retry_count)) + (random.randint(0, 1000) / 1000)
                    # Silently wait without showing status
                    time.sleep(delay)
                else:
                    # If it's not a throttling exception or we've exhausted retries
                    print(f"DEBUG - Exception during agent invocation: {str(e)}")
                    raise e
        
        return {"completion": "Error: Maximum retries exceeded due to rate limiting"}
        
    except Exception as e:
        error_msg = f"Error invoking agent: {str(e)}"
        
        if "throttlingException" in str(e):
            st.error("Rate limit exceeded. Please try again in a few moments.")
        elif "ResourceNotFoundException" in str(e):
            st.error("Could not connect to agent. Please check your configuration.")
        else:
            st.error(error_msg)
        
        return {"completion": error_msg}
