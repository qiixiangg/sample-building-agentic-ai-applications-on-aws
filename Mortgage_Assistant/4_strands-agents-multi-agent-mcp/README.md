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

In the first notebook, we will build hierarchical multi agent system that follows the graph pattern. In the second notebook, we will use the agent_graph tool.

**01_strands_multi_agent_collaboration-mcp-tool.ipynb** - You will be creating a Hierarchical Agent Graph usng strands and integrating custom tools and MCP tools
**02_strands_graph_coordinator_agents.ipynb** - You will be creating the same agent as above (but only Strands custom tools and not MCP tools) but using **agent_graph** tool provided by Strands. 