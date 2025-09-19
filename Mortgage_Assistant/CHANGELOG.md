# CHANGELOG

## Modified Files

### 2_bedrock-multi-agent/01_create_knowledgebase.ipynb

**Changes:**
- **Package Installation**: Added `matplotlib termcolor pickleshare` to pip install command
- **Model Configuration**: Changed from variable `agent_foundation_model[0]` to hardcoded inference profile `"arn:aws:bedrock:us-east-1:025066245096:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0"`
- **Environment Variables**: Change `region` variable set to hardcoded 'us-east-1'

### 4_strands-agents-multi-agent-mcp/01_strands_multi_agent_collaboration-mcp-tool.ipynb

**Changes:**
- **Environment Variables**: Added `AWS_REGION` environment variable set to 'us-east-1'
- **Model Configuration**: Changed model from `"anthropic.claude-3-5-haiku-20241022-v1:0"` to `"us.anthropic.claude-3-5-haiku-20241022-v1:0"` (added region prefix)

## Added Files

### 6_strands-agents-bedrock-agentcore/01-mcp-server-hosting/

**Added:** Bedrock AgentCore Runtime workshop for hosting MCP Server (based on `3_mcp-server-client/strands_mcp/creditcheck_server_http.py` implementation)

### 6_strands-agents-bedrock-agentcore/02-multi-agent-with-mcp/

**Added:** Bedrock AgentCore Runtime workshop for multi-agent collaboration with MCP tools (based on `4_strands-agents-multi-agent-mcp/01_strands_multi_agent_collaboration-mcp-tool.ipynb` implementation)
