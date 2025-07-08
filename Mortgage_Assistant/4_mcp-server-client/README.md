### Model Context Protocol ###

The [**Model Context Protocol (MCP)**](https://modelcontextprotocol.io/introduction)  is an open protocol standardizing how AI agents connect to external services, like databases, APIs, legacy systems, or third-party tools. Instead of building custom integrations for each service, MCP provides one standard interface for all external connections - somewhat like REST, but for AI agents.

The below diagram shows MCP Client and server connection mechanism using HTTP as transport protocol, another option is stdio which we are not showing in this workshop

![Hierarchical Mortgage Agent](../../images/mcp_client_server.png)

Manual MCP implementation involves a lot of work: managing handshakes, connection state, message parsing, schema validation, etc. 

With Strands, on the other hand, it's really just a few lines of code as you can see in the notebooks we have provided for you to try it out.

The Strands SDK handles all the protocol complexity, letting you focus on agent functionality rather than integration details.

We will be creating a simple MCP server which provides a **credit_check tool**. It takes cthe customer id as input parameter and returns the credit score for the customer. The logic for credit scoring is to return the score for a known set of customer ids, however in real world scenario it could be collating all the required documents from the customer or from the customer profile already stored to maybe connecting to an external application to calculate the score.

We will use this MCP server later in the **Strands** lab where we integrate Strands tools and MCP tool.

## Instructions to run the server and the client

**Run the MCP server** provided in the mcp_agent folder. Go to the SageMaker terminal from this notebook and navigate to the agent-mcp foler and run the below command:

**pip install mcp**

**python creditcheck_server_http.py**

This will start the MCP server that can accessible through this url: "http://0.0.0.0:8080/mcp".

We will connect to this server through Strands MCP client by running the below command:

**python strands_mcp_client.py**