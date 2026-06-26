from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from agent.rag_env import load_rag_env
from agent.rag_tools import tools, search_tool, off_topic
from typing import Annotated, Literal, TypedDict, Sequence
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.graph import START, END, StateGraph
load_rag_env()

# graph state
class AgentState(TypedDict):
    messages:Annotated[Sequence[BaseMessage], add_messages]


# graph nodes
def agent(state:AgentState):
    messages = state['messages']
    model = ChatOpenAI()
    model = model.bind_tools(tools=tools)
    response = model.invoke(messages)
    return {"messages": [response]}

def should_continue(state:AgentState) -> Literal['_tool_', END]:
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return "_tool_"
    return END

# start the graph workflow
workflow = StateGraph(AgentState)
tool_node = ToolNode(tools)
workflow.add_node('_agent_', agent)
workflow.add_node('_tool_', tool_node)
workflow.add_edge(START, '_agent_')
workflow.add_conditional_edges(
    '_agent_',
    should_continue
)
workflow.add_edge('_tool_', '_agent_')
graph = workflow.compile()
response = graph.invoke({
    "messages": [HumanMessage(content="tell me about the 2026 f1 season")]
})
print(response)