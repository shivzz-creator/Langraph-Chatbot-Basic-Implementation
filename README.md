<!--
Beautiful, concise README for the LangGraph chatbot example.
Created to accompany `m.py` in this repository.
-->

# LangGraph Chatbot

A minimal example that demonstrates using LangGraph with an Ollama-backed LLM
to run a simple conversation flow. The primary script is `m.py`.

## Features

- Small state-driven graph that sends message history to an LLM
- Streams assistant responses from the graph runtime
- Minimal CLI for quick local testing

## Prerequisites

- Python 3.9+
- An Ollama runtime or compatible LLM endpoint if using `langchain-ollama`.

## Installation

Install the required Python packages (recommended in a virtualenv):

```bash
pip install --upgrade langchain langchain-community langgraph
# Optional: if you plan to use Ollama via langchain-ollama
pip install langchain-ollama
```

## Configuration

In `m.py` you can change the model name passed to the Ollama client:

```python
llm_client = OllamaLLM(model="llama3.1")
```

If your Ollama setup requires extra environment configuration, set those
according to your Ollama installation instructions.

## Usage

Run the chatbot script and type messages at the prompt:

```bash
python m.py
```

Type `quit`, `exit`, or `q` to end the session.

Sample interaction:

```
User: Hello
Assistant: Hi — how can I help today?
```

## File reference

- Primary script: `m.py` — the graph definition and CLI loop.

## Notes & Troubleshooting

- This example assumes a working Ollama client. If you don't have Ollama,
  you can adapt the node handler (`chat_node_handler`) to use any LangChain
  LLM wrapper that accepts a list of role/content messages.
- If the graph streaming call doesn't produce output, ensure your LLM
  client returns a plain string and that the `messages` structure matches
  the expected role/content format.

## License

This README and example code are provided for educational purposes.

By Shivansh Pareek
