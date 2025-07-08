import json
import os
from typing import List
from mcp.server.fastmcp import FastMCP



# Initialize FastMCP server
mcp = FastMCP("creditcheck",
              host="0.0.0.0",
              port=8080
)

@mcp.tool()
def credit_check(customer_id: int) -> int:
    """
    Perform a credit check for the customer id.
    
    Args:
        customer_id: The ID of the existing customer
        
    Returns:
        returns an integer which is a credit score
    """   
    scores = {
        1111: 70,
        2222: 80,
        3333: 90
    }
    return scores.get(customer_id, 0) 





if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='streamable-http')
