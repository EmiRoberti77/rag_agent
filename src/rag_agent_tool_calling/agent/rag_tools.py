from typing import Literal
from langchain.tools import tool
from langchain_core.tools import create_retriever_tool
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from agent.rag_db import RagDB
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# init the rag database
db = RagDB()
# the search tool will retrieve data from the vector store
search_tool = create_retriever_tool(
    retriever=db.retriever,
    name="search_f1_data",
    description="Searcg for F1 season information"
)

@tool
def off_topic():
    """Catch all questions not related to Forumala 1"""
    return "Forbidded-no answer"

Race_weather = Literal['sunny', 'cloudy', 'light rain', 'full rain']
class RacePredictionArgs(BaseModel):
    context: str = Field(description='Previous race data')
    race_weather_forecast:Race_weather = Field(description='race weather forecast')
    location:str = Field(description='race location')


@tool(
    "race_preditions",
    description="based on previous context build a race prediction of top 3 race winners",
    args_schema=RacePredictionArgs
)
def race_prediction(context:str, race_weather_forecast:Race_weather='sunny', location:str='Italy'):
    system_msg = """ You are a formula 1 journalist and for for the media. 
                    you will make reliable prediction for race 
                    based on context provided"""
    prompt = (
        "CONTEXT:{context}\n" 
        "LOCATION:{location}\n"
        "WEATHER:{race_weather_forecast}\n"
        "QUESTION:{question}"
    )
    prompt_template = ChatPromptTemplate.from_messages(
        messages=[
            ('system', system_msg),
            ('human', prompt)
        ]
    )
    chain = ( 
        prompt_template 
        | ChatOpenAI() 
        | StrOutputParser() 
    )
    return chain.invoke({
        "context": context,
        "location": location,
        "race_weather_forecast": race_weather_forecast,
        "question": "create a prediction of the top 3 race drivers and why",
    })


# add all tools in a tools array
tools = [search_tool, off_topic, race_prediction]