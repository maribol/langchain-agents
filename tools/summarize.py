# Import necessary libraries.

from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type

# Define a function to summarize text.

def summarize(objective, content):
    # Initialize with the ChatOpenAI model.
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")

    # Split the text into smaller chunks.
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=10000, chunk_overlap=500)
    docs = text_splitter.create_documents([content])

    # Define a template prompt.
    map_prompt = """
    Summarize the following text for {objective}:
    "{text}"
    SUMMARY:
    """
    # Create a map prompt template.
    map_prompt_template = PromptTemplate(
        template=map_prompt, input_variables=["text", "objective"])

    # Load the summary chain.
    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type='map_reduce',
        map_prompt=map_prompt_template,
        combine_prompt=map_prompt_template,
        verbose=True
    )

    # Run summary chain and return output.
    output = summary_chain.run(input_documents=docs, objective=objective)
    return output

# Define a class for summarization input.
class SummarizeInput(BaseModel):
    """Inputs for the summary process."""
    objective: str = Field(
        description="The objective & task that users give to the agent.")
    content: str = Field(description="The content to be summarized.")

# Define a tool class for summarization.
class SummarizeTool(BaseTool):
    name = "scrape_website"
    description = "Useful tool for performing google summarization, passing the query as a function parameter."
    args_schema: Type[BaseModel] = SummarizeInput

    # Define a run method.
    def _run(self, objective: str, content: str):
        return summarize(objective, content)

    # Define a async run method.
    def _arun(self, url: str):
        # This method is not yet implemented.
        raise NotImplementedError("async run method is not yet implemented.")