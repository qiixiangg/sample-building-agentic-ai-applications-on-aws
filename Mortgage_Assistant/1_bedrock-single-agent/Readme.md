### Creating a single Bedrock for new Mortgage application (pre approval)

In this first lab, we will create a single agent using [Amazon Bedrock agents](https://aws.amazon.com/bedrock/agents/). This single agent will walk the user through the process of creating a new mortgage application (The agent does not ask for any documents, so think of this as a preapproval).  Here's how the flow works:
1. For a new chat, the agent  will ask user for their customer id. If the user does not have a customer id, it will create one. 
2. It then asks a series of questions to get some basic information such as  name, age, annual income and annual expense.
3. Once it gets all the information, it provides the user an application id and the flow is complete.

#### Building the agent
To build the agent, use the instructions specified in the notebook **1_bedrock-single-agent/create-new-application-agent.ipynb** 

#### Testing the agent
To test the agent follow the steps at the end of the notebook.

#### Challenge
As a challenge, we invite you to change the prompt to ask a question on loan value as well. You will need to propagate to the action group lambda and make sure its visible in the lambda logs.