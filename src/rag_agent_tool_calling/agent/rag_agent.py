from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
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
    "messages": [
        SystemMessage(content="""
            You are an F1 assistant with access to tools.
            Rules:
            1. For race predictions, ALWAYS call search_f1_data first to get context.
            2. Then call race_predictions, passing the search results as the context argument.
            3. Use off_topic only for non-F1 questions.
            4. After tools run, give a clear final answer to the user.
            """),
        HumanMessage(content="give me prediction of the top 3 for Monza in Italy")
    ]
})
print(response)