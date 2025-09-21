# Strands Agents with Amazon Bedrock AgentCore Runtime

## Overview

Amazon Bedrock AgentCore Runtime is a secure, serverless runtime designed for deploying and scaling AI agents and tools. It supports any frameworks, models, and protocols, enabling developers to transform local prototypes into production-ready solutions with minimal code changes.

Amazon BedrockAgentCore Python SDK provides a lightweight wrapper that helps you deploy your agent functions as HTTP services that are compatible with Amazon Bedrock. It handles all the HTTP server details so you can focus on your agent's core functionality.

All you need to do is decorate your function with the `@app.entrypoint` decorator and use the `configure` and `launch` capabilities of the SDK to deploy your agent to AgentCore Runtime. Your application is then able to invoke this agent using the SDK or any of the AWS's developer tools such as boto3, AWS SDK for JavaScript or the AWS SDK for Java.

This directory demonstrates advanced integration patterns between **Strands Agents** and **Amazon Bedrock AgentCore Runtime**, showcasing how to deploy production-ready agentic AI systems with MCP (Model Context Protocol) integration for mortgage processing workflows.

![Runtime Overview](images/runtime_overview.png)

## Architecture Overview

The tutorials in this directory demonstrate two key deployment patterns:

### Pattern 1: MCP Server Hosting
```
Local Strands Agent → MCP Client → AgentCore Runtime → MCP Server (Credit Check)
```

### Pattern 2: Multi-Agent System Deployment
```
Client → AgentCore Runtime (Strands Multi-Agent) → AgentCore Runtime (MCP Server)
                    ↓
            Knowledge Base (Bedrock)
```

## Key Features

### Framework and Model Flexibility

- Deploy agents and tools from any framework (such as Strands Agents, LangChain, LangGraph, CrewAI) 
- Using any model (in Amazon Bedrock or not)
- **Framework Agnostic**: Deploy agents from any framework with built-in security, scaling, and monitoring
- **Protocol Support**: Both HTTP and MCP protocols

### Integration

Amazon Bedrock AgentCore Runtime integrates with other Amazon Bedrock AgentCore capabilities through a unified SDK, including:

- Amazon Bedrock AgentCore Memory
- Amazon Bedrock AgentCore Gateway
- Amazon Bedrock AgentCore Observability
- Amazon Bedrock AgentCore Tools

This integration aims to simplify the development process and provide a comprehensive platform for building, deploying, and managing AI agents.

### Model Context Protocol (MCP) Integration

- Standardized communication between AI systems and external tools
- Secure, stateless tool execution
- Session isolation and management
- Streamable HTTP transport for real-time interactions

### Strands Agents Integration

- Model-driven approach to building AI agents
- Native MCP client support
- Multi-agent collaboration patterns
- Built-in tool ecosystem

### Use Cases

The runtime is suitable for a wide range of applications, including:

- Real-time, interactive AI agents
- Long-running, complex AI workflows
- Multi-modal AI processing (text, image, audio, video)

## Tutorials overview

In these tutorials we will cover the following functionality:

- [Hosting MCP Servers](01-mcp-server-hosting)
- [Multi-Agent with MCP](02-multi-agent-with-mcp)

## Related Resources

### AWS Documentation
- [Amazon Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/)
- [Amazon Bedrock AgentCore Samples](https://github.com/awslabs/amazon-bedrock-agentcore-samples)

### Framework Documentation
- [Strands Agents Documentation](https://strandsagents.com/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
