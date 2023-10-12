# Import necessary packages
import os
import re
import uvicorn
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import FastAPI

# Imports related to Langchain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate, MessagesPlaceholder
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.schema import SystemMessage

# Tools related to website scraping, searching, and summarizing
from tools.search import SearchTool
from tools.scrape_website import ScrapeWebsiteTool
from tools.summarize import SummarizeTool

# List of tools to be used
tools = [ScrapeWebsiteTool(), SearchTool(), SummarizeTool()]

# System message detailing the researcher's responsibilities
system_message = SystemMessage(
    content="""You are a world class researcher.
    You do not make things up, you will try as hard as possible to gather facts & data to back up the research.
    Your task is to carry out comprehensive research for a person and find out information about people including their contact information, position, company and any other relevant business information"""
)

# Define agent's parameters
agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    "system_message": system_message,
}

# Create language model
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")

# Create memory buffer
memory = ConversationSummaryBufferMemory(
    memory_key="memory", return_messages=True, llm=llm, max_token_limit=1000)

# Initialize agent with defined parameters
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    max_execution_time=600,
    agent_kwargs=agent_kwargs,
    memory=memory,
)

# Create FastAPI application
app = FastAPI()
app.port = int(os.environ.get("PORT", 8000))

# Define request body for POST request
class ResearchInput(BaseModel):
    person_name: str

# POST method to process the query and provide output
@app.post("/")
def research(input: ResearchInput):
    person_name = input.person_name
    content = agent({"input": person_name})

    research_result = content['output']

    return research_result

# Main entry
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)