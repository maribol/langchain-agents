import os
import json
import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Type
from langchain.tools import BaseTool

# Loads the .env file
load_dotenv()

# Reads the SERP_API_KEY from environment variables
serper_api_key = os.getenv("SERP_API_KEY")

# A function that performs a google search with the provided person_name
def search(person_name):
    # API endpoint
    url = "https://google.serper.dev/search"

    # Generates the data payload
    payload = json.dumps({"q": person_name})

    # Request headers, including api key and content type
    headers = {'X-API-KEY': serper_api_key, 'Content-Type': 'application/json'}

    # Executes the API request
    response = requests.request("POST", url, headers=headers, data=payload)

    # Returns the search results text
    return response.text

# Search Input model class defines the input parameters schema for the search tool
class SearchInput(BaseModel):
    """Inputs for search"""
    person_name: str = Field(description="The objective & task that users give to the agent")

# SearchTool class is a child of BaseTool and is useful to perform google searches
class SearchTool(BaseTool):
    # Tool name
    name = "search"

    # Tool description
    description = "useful to perform google searches, passing the person_name to the function"

    # Defines the schema for the tool's arguments
    args_schema: Type[BaseModel] = SearchInput

    # _run method executes the search function with the passed person_name
    def _run(self, person_name: str):
        return search(person_name)

    # _arun method is not implemented and will throw a NotImplementedError when called
    def _arun(self, url: str):
        raise NotImplementedError("error here")