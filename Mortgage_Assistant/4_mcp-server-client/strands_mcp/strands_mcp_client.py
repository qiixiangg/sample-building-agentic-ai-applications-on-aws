from strands import Agent
from strands.tools.mcp import MCPClient
from mcp.client.streamable_http import streamablehttp_client

def main():
    # Connect to the quiz MCP server
    print("\nConnecting to MCP Server...")
    mcp_credict_check_server = MCPClient(lambda: streamablehttp_client("http://localhost:8080/mcp"))

    try:
        with mcp_credict_check_server:

            # Create the subject expert agent with a system prompt
            credit_checker = Agent()

            # List the tools available on the MCP server...
            mcp_tools = mcp_credict_check_server.list_tools_sync()
            print(f"Available tools: {[tool.tool_name for tool in mcp_tools]}")

            # ... and add them to the agent
            credit_checker.tool_registry.process_tools(mcp_tools)

            # Start an interactive learning session
            print("\n👨‍💻 Credit checke Expert with MCP Integration")
            print("\n📋 Try: 'Give me the credit check score for customer id 1111'")

            while True:
                user_input = input("\n🎯 Your request: ")
                
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("👋 Happy learning!")
                    break
                
                print("\n🤔 Processing...\n")
                credit_checker(user_input)
               
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("💡 Make sure the credit check service is running: python creditcheck_server_http.py")

if __name__ == "__main__":
    main()