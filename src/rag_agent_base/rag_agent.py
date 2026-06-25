print("RAG Agent")
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from rag_query import query_rag
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from operator import add

# define the state for the graph
class State(TypedDict):
    question: str
    messages: Annotated[list[str], add]
    look_outside: bool


def router(state:State):
    question = state['question']
    last_message = state['messages'][-1]
    print('router_last_message', last_message)
    if last_message == "I don't have information about that in my data.":
        return '_external_lookup_'
    else:
        return '_completed_lookup'


def external_tool(state:State):
    question = state['question']
    return {"messages": ["I have done a external call and my response is bla blah"]}


def query_node(state:State):
    question = state['question']
    prompt_template = ChatPromptTemplate.from_messages(
        messages=[
            ("system", """You are a sports journalist.
            Answer ONLY using the provided CONTEXT.
            If CONTEXT does not contain enough information to answer, say:
            "I don't have information about that in my data."
            Do not use outside knowledge."""),
            ("human", "CONTEXT:{context}  QUESTION:{question}")
        ]
    )

    chain = (
        RunnablePassthrough.assign(
            context=lambda x: query_rag(x['question'])
        ) 
        | prompt_template
        | ChatOpenAI()
        | StrOutputParser()
    )

    response = chain.invoke({"question": question})
    return {"messages": [response]}


def main() -> None:
    # workflow
    workflow = StateGraph(State)
    # nodes
    workflow.add_node('_query_', query_node)
    workflow.add_node('_external_', external_tool)
    # edges
    workflow.add_edge(START, '_query_')
    workflow.add_conditional_edges('_query_', router, {
        "_external_lookup_":"_external_",
        "_completed_lookup": END 
    })
    workflow.add_edge('_external_', END)
    # compile the graph
    graph = workflow.compile()
    # responses
    response = graph.invoke({"question":"how did Ferrari do in the season"})
    print('RESPONSE 1')
    print(response)

    response = graph.invoke({"question":"how Sebastial Vettel do in the season"})
    print('RESPONSE 2')
    print(response)

if __name__ == "__main__":
    main()