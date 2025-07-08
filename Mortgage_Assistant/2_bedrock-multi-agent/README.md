### Creating a multi-agent collaboration using Amazon Bedrock
Multi-agent collaboration enables multiple Amazon Bedrock Agents to collaboratively plan and solve complex tasks. With multi-agent collaboration, you can quickly assemble a team of agents that can break down tasks, assign specific tasks to domain specialist sub-agents, work in parallel, and leverage each other's strengths, which leads to more efficient problem-solving. Multi-agent provides a centralized mechanism for planning, orchestration , and user interaction for your generative AI applications.

In the previous lab, you created a single agent that can help customers submit a pre-approval for a mortgage application. In this lab you will learn how to 
1. Create two other agents that can 1/answer general questions on mortgage and 2/ Answer questions on existing mortgage/
2. Create a supervisor agent that can 'orchestrate' the request and call the appropriate sub agent.


#### Building the agent
This lab has three notebooks that help you build the agents -     

**2_bedrock-multi-agent/01_create_knowledgebase.ipynb** - This notebook creates a knowledge base that will be used by the agent that answers general questions on mortgage.

**2_bedrock-multi-agent/02_create_collaborator_agents.ipynb** - This notebook creates the two collaborator or sub agents described above.

**2_bedrock-multi-agent/03_create_supervisor_agent.ipynb** - This notebook creates the orchestrator agent.

#### Testing the agent
To test the agent follow the steps at the end of each notebook.


