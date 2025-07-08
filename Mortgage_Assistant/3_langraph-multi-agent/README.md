# Mortgage Assistant with LangGraph Multi-Agent System

This project demonstrates how to build mortgage assistant applications using LangGraph, an extension of LangChain that provides a framework for building stateful agentic applications. 

## Project Overview

The Mortgage Assistant is designed to:
- Help customers access information about their existing mortgages
- Process new mortgage applications
- Answer frequently asked questions about mortgage products
- Demonstrate agent collaboration through a multi-agent architecture

## Repository Contents

- `01-langgraph-single-agent.ipynb`: Demonstrates how to create a single agent using LangGraph for mortgage assistance
- `02-langgraph-multi-agent.ipynb`: Builds upon single agent and showcases multi-agent system with specialized roles and inter-agent communication
- `04-langgraph-mcp-client.ipynb`: Demonstrates integration of MCP client with LangGraph agents. We will use the MCP server built during the earlier lab.

## Features

### Single Agent Implementation
- ReAct pattern for reasoning and action execution
- Tools for retrieving mortgage information
- Conversational interface for mortgage assistance
- Stateful memory management

### Multi-Agent System
- Specialized agents with defined roles and responsibilities:
  - Account Inquiry Agent: Handles existing mortgage information
  - Application Processing Agent: Manages new mortgage applications
  - FAQ Agent: Provides general mortgage information using knowledge bases
- Inter-agent communication and handover protocols

### Model Context Protocol (MCP) Integration
- MCP Server: Provides standardized credit check functionality through HTTP protocol
- MCP Client Integration: Shows how to connect LangGraph agents with MCP servers
- Enhanced agent capabilities through external service integration


## Learning Objectives

By working through these notebooks, you will:
1. Understand how to create single and multi-agent systems using LangGraph
2. Learn how to define tools for retrieving and processing mortgage information
3. Implement the ReAct pattern for reasoning and action execution
4. Build agent communication protocols and handover mechanisms
5. Implement Model Context Protocol (MCP) servers for extending agent capabilities
6. Integrate external services through MCP client connections