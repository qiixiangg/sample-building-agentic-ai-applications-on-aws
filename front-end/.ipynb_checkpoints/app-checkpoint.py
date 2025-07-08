import streamlit as st
import os
import uuid
import time
import json
import re
from bedrock_utils import load_agent_config, invoke_bedrock_agent, list_bedrock_agents

# Page configuration
st.set_page_config(
    page_title="Bedrock Agent Chat",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_mode" not in st.session_state:
    st.session_state.agent_mode = "single"  # Default to single agent mode
if "selected_agents" not in st.session_state:
    st.session_state.selected_agents = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "initialized" not in st.session_state:
    st.session_state.initialized = False

# Load agent configurations
available_agents = load_agent_config()

# Sidebar for configuration
st.sidebar.title("Bedrock Agent Configuration")

# Empty sidebar section for spacing
st.sidebar.write("")

# Uncomment this section if you need to debug agent listing
# try:
#     actual_agents = list_bedrock_agents()
#     if actual_agents:
#         st.sidebar.success(f"Found {len(actual_agents)} Bedrock agents in your account")
#         st.sidebar.expander("Available Agents").write(actual_agents)
#     else:
#         st.sidebar.warning("No Bedrock agents found in your account. Using values from Secrets Manager.")
# except Exception as e:
#     st.sidebar.error(f"Error checking for agents: {str(e)}")
# Agent selection based on mode
selected_agent = st.sidebar.selectbox(
    "Agent Mode",
    options=[agent["id"] for agent in available_agents],
    format_func=lambda x: next((a["name"] for a in available_agents if a["id"] == x), x),
    index=0 if not st.session_state.selected_agents else [a["id"] for a in available_agents].index(st.session_state.selected_agents[0])
)
st.session_state.selected_agents = [selected_agent]

# Reset conversation button
if st.sidebar.button("Reset Conversation"):
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.initialized = False
    st.rerun()

# Main app
st.title("Bedrock Agent Chat Interface")

# Display mode information

if st.session_state.selected_agents:
    agent_name = next((a["name"] for a in available_agents if a["id"] == st.session_state.selected_agents[0]), 
                        st.session_state.selected_agents[0])
    st.info(f"Connected to: {agent_name}")
else:
    st.warning("Please select an agent to continue.")

# Add welcome message if this is the first load
if not st.session_state.initialized and not st.session_state.messages:
    welcome_message = """
    Hello! Welcome to our mortgage assistant. I'm here to help you with any questions or information you need regarding your mortgage. How can I assist you today?
    
    Here are some questions you might want to ask: \n
    Single Agent
    - What's your general guidance about refinancing mortgages? \n
    Multi Agent
    - My customer id is 1234, what is the balance of my current mortgage?
    - I have a mortgage application with the ID 4567, what is mortgage amount, rate and maturity date?
    - What interest rate do i have on my existing mortgage (customer id 1234), and how does it compare to rates for my new mortgage application with id 4567
    """
    
    # First add to session state so it's not displayed twice
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})
    st.session_state.initialized = True
    
    # Force a rerun to display the welcome message properly
    st.rerun()

# Function to extract and display agent thoughts from trace data
def extract_agent_thoughts(model_input):
    thoughts_output = []
    
    try:
        # Extract thoughts directly from the trace structure
        if isinstance(model_input, dict) and "trace" in model_input:
            trace_data = model_input["trace"]
            
            # Check if we have orchestration trace data
            if "orchestrationTrace" in trace_data:
                orchestration = trace_data["orchestrationTrace"]
                thoughts_output.append("### Agent Processing")
                
                # Process collaborators first
                if "collaborators" in trace_data:
                    for collab_name, collab_traces in trace_data["collaborators"].items():
                        thoughts_output.append(f"**Collaborator: {collab_name}**")
                        
                        # Extract rationales from each step, but skip the first one
                        for i, trace in enumerate(collab_traces):
                            # Skip the first rationale (index 0)
                            if i == 0:
                                continue
                                
                            if "orchestrationTrace" in trace and "rationale" in trace["orchestrationTrace"]:
                                rationale = trace["orchestrationTrace"]["rationale"]
                                if isinstance(rationale, dict) and "text" in rationale:
                                    thoughts_output.append(f"```\n{rationale['text']}\n```")
                                elif isinstance(rationale, str) and len(rationale) > 50:
                                    thoughts_output.append(f"```\n{rationale}\n```")
                
                # Finally, add the main agent's rationale
                if "rationale" in orchestration:
                    thoughts_output.append("**Main Agent Conclusion:**")
                    rationale = orchestration["rationale"]
                    if isinstance(rationale, dict) and "text" in rationale:
                        thoughts_output.append(f"```\n{rationale['text']}\n```")
                    elif isinstance(rationale, str) and len(rationale) > 50:
                        thoughts_output.append(f"```\n{rationale}\n```")
    except Exception as e:
        thoughts_output.append(f"Error extracting agent thoughts: {str(e)}")
    
    return thoughts_output

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], dict):
            # For responses with trace information
            if "completion" in message["content"]:
                # Check if there's trace data with agent thoughts to display first
                if "trace" in message["content"]:
                    trace_data = message["content"]["trace"]
                    
                    # Try to extract agent thoughts directly from the trace data
                    thoughts = extract_agent_thoughts({"trace": trace_data})
                    if thoughts:
                        with st.expander("Agent Thought Process", expanded=False):
                            for thought in thoughts:
                                st.markdown(thought)
                
                # Display the actual completion text
                st.markdown(message["content"]["completion"])
                
            else:
                # For multiple agent responses (legacy format)
                for agent, response in message["content"].items():
                    st.markdown(f"**{agent}**:")
                    st.markdown(response)
        else:
            # For user messages and single agent responses
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response based on mode
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            agent_id = st.session_state.selected_agents[0]
            agent_config = next((a for a in available_agents if a["id"] == agent_id), None)
            
            if agent_config:
                response = invoke_bedrock_agent(
                    agent_id=agent_config["id"],
                    agent_alias_id=agent_config["alias_id"],
                    prompt=prompt,
                    session_id=st.session_state.session_id,
                    enable_trace=True
                )
                
                # Display response with typing effect
                message_placeholder = st.empty()
                full_response = ""
                
                # Get the completion text
                completion_text = response.get("completion", "No response from agent")
                
                # Check if there's trace data with agent thoughts to display first
                agent_thoughts_displayed = False
                if isinstance(response, dict) and "trace" in response:
                    trace_data = response["trace"]
                    
                    # Try to extract agent thoughts directly from the trace data
                    thoughts = extract_agent_thoughts({"trace": trace_data})
                    if thoughts:
                        with st.expander("Agent Thought Process", expanded=True):
                            for thought in thoughts:
                                st.markdown(thought)
                        agent_thoughts_displayed = True
                
                # Simulate typing for the main response
                for chunk in completion_text.split():
                    full_response += chunk + " "
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.05)  # Adjust typing speed here
                
                # Display final response
                message_placeholder.markdown(completion_text)
                
                # Add to session state after displaying
                stored_response = {
                    "completion": completion_text
                }
                if isinstance(response, dict) and "trace" in response:
                    stored_response["trace"] = response["trace"]
                
                st.session_state.messages.append({"role": "assistant", "content": stored_response})
            else:
                st.error("Selected agent configuration not found.")
