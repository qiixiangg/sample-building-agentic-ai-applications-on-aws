In this section, we will build a multi agent collaboration system using [Strands Agents](https://strandsagents.com/latest/). 

The **Strands Agents SDK** supports various multi-agent patterns such as:

- [**Swarm**](https://strandsagents.com/latest/user-guide/concepts/multi-agent/swarm/)  
- [**Graph**](https://strandsagents.com/latest/user-guide/concepts/multi-agent/graph/)  
- [**Workflow**](https://strandsagents.com/latest/user-guide/concepts/multi-agent/workflow/)  
- [**Agent as a Tool**](https://strandsagents.com/latest/user-guide/concepts/multi-agent/agents-as-tools/)


### Lab Structure
This lab has two different notebooks
#### notebook 1 ####
 The first notebook in the lab is **01_create02_strands_multi_agent_collaboration-mcp-tool.ipynb** The aim of the  notebook is to create a multi agent collaboration system as described in the image below. 

<img src="/images/01_06_multi_agent_mcp.png" alt="Multi agent MCP" width="600"/>

*However, we have a small challenge for you in this lab*

We have implemented only two collaborator agents and would leave the implementation of the 'create new morgage application agent' as a challenge for you. Here's what you need to do:

Step 1: Run through each cell of the notebook and understand how to build the multi agent system with MCP support using Strands.
Step 2: Modify the notebook to add the 'create new morgage application agent' and include that into the workflow. 
Step 3: If you need help, we have the solution in the **solution_to_challenge.ipynb** notebook. However, use it only if required!

#### notebook 1 ####

**03_strands_graph_coordinator_agents.ipynb** - In the second notebook in the lab, we will create the same multi agent system as above but instead of weaving the agents together manually, we will use the **agent_graph** tool provided by Strands. 