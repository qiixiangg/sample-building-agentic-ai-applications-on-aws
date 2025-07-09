In this section, we will build a multi agent collaboration system using [Strands Agents](https://strandsagents.com/latest/). Multi-agent systems consist of multiple interacting intelligent agents that enable:

- **Distributed Problem Solving**: Breaking complex tasks into subtasks for parallel processing  
- **Information Sharing**: Agents exchange insights to build collective knowledge  
- **Specialization**: Different agents focus on specific aspects of a problem  
- **Redundancy**: Multiple agents working on similar tasks improve reliability  
- **Emergent Intelligence**: The system exhibits capabilities beyond those of its individual components  


The **Strands Agents SDK** supports various multi-agent patterns such as:

- [**Swarm**](https://strandsagents.com/latest/user-guide/concepts/multi-agent/swarm/)  
- [**Graph**](https://strandsagents.com/latest/user-guide/concepts/multi-agent/graph/)  
- [**Workflow**](https://strandsagents.com/latest/user-guide/concepts/multi-agent/workflow/)  
- [**Agent as a Tool**](https://strandsagents.com/latest/user-guide/concepts/multi-agent/agents-as-tools/)

In this lab we will include some of these patterns.

## Lab structure
<img src="/images/01_06_multi_agent_mcp.png" alt="Multi agent MCP" width="600"/>

**01_create-new-application-agent-strands.ipynb** - In the first notebook, we will build a single agent that can help a customer with a new mortgage application. This is similar to the single agent that we built in the bedrock agents lab. However, for this lab we will be using Strands. 

**02_strands_multi_agent_collaboration-mcp-tool.ipynb** - In the second notebook of this lab, we will build hierarchical multi agent system that follows the graph pattern. We will begin by creating two more agents and then a supervisor agent to coordinate the three agents. We will also enable our supervisor to perform a credit check using an MCP server that we built in the previous lab.  We will use the graph pattern in this lab.

**03_strands_graph_coordinator_agents.ipynb** - In the third lab, we will create the same multi agent system as above but instead of weaving the agents together manually, we will use the **agent_graph** tool provided by Strands. 