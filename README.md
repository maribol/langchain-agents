# Langchain Agents Automated Research - GPT Example

This repository includes two python scripts:

1. main.py: An automated research web-service hosted by the FastAPI and uses OpenAI's gpt-3.5-turbo model to perform comprehensive research about a person.
2. The tools directory includes tools used for searching, website scraping, and summarizing.

## Getting Started

To run this project, clone the repository and follow these steps:

```bash
git clone https://github.com/maribol/langchain-agents.git
cd langchain-agents
```

### Setting up a Python Virtual Environment

Before installing the project dependencies, it's recommended to create a virtual environment. This helps to isolate the project-specific dependencies from the globally installed packages and avoid potential conflicts.

Follow the steps below to create and activate a virtual environment:

If using **Windows**, run the following in your command prompt:

```bash
python -m venv env
env\Scripts\activate
```

If using **macOS** or **Linux**, run the following in your terminal:

```bash
python3 -m venv env
source env/bin/activate
```
The `python` command might be `python3` or `py` depending on your Python installation.

The virtual environment will be created in a folder named `env` in your current directory. Before running any `pip install` commands, ensure that your virtual environment is active. The name of your virtual environment (in this case, `env`) should be visible in your command line (enclosed in parentheses).

## Prerequisites

This project makes use of several libraries, you can obtain them by running:

```bash
pip install -r requirements.txt
```

The project is based on Python 3.8 or later versions.

You need to get your API keys for browserless.io and serp.dev and set them as environmental variables in your system.

You can set those in a `.env` file and load them through a command.

## Usage

### Running the server

You can start the FastAPI server by running:

```bash
python main.py
```

The server runs on `localhost:8001`.

### Making a request

You can make a POST request to the `/` (root) endpoint with the name of the person to research in the request body. The server will return the result of the comprehensive research about the person.

Use the example command below to perform a request:

```bash
curl -X POST "http://localhost:8001/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"person_name\":\"Elon Musk\"}"
```

You will receive a response containing the search result.

## Summary

This project serves as an example of how to incorporate GPT-based Langchain Agents to automate comprehensive research about a person.
