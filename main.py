# -----------------------------------------------
# Install dependencies (Run these in your terminal)
# -----------------------------------------------
# pip install --upgrade langchain langchain-community langgraph
# pip install langchain-ollama

from typing import List, Dict
from langgraph.graph import StateGraph, START, END
from langchain_ollama.llms import OllamaLLM


# ------------------------------------------------------
# STEP 1: Define the State (memory) structure
# ------------------------------------------------------
"""
State keeps data that flows between graph nodes.
Here, we store a list of messages exchanged between
the user and the assistant.

State = {
    "messages": [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi! How can I help?"}
    ]
}
"""

class State(Dict):
    messages: List[Dict[str, str]]


# ------------------------------------------------------
# STEP 2: Create the graph (conversation pipeline)
# ------------------------------------------------------
graph_builder = StateGraph(State)

# Initialize the LLM (Ollama local model)
llm = OllamaLLM(model="llama3.1")


# ------------------------------------------------------
# STEP 3: Create a chatbot function (graph node)
# ------------------------------------------------------
"""
This function is the brain of the chatbot.
It receives the conversation state,
sends messages to the LLM,
gets the model's response,
and updates the conversation.
"""

def chatbot(state: State):
    # Send the entire message list to LLM and receive text output
    response_text = llm.invoke(state["messages"])

    # Add assistant reply to message history
    state["messages"].append({
        "role": "assistant",
        "content": response_text
    })

    # Return updated state
    return {"messages": state["messages"]}


# Add the chatbot node to the graph
graph_builder.add_node("chatbot", chatbot)

# Create edges (flow)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Compile the graph
graph = graph_builder.compile()


# ------------------------------------------------------
# STEP 4: Function to stream chatbot responses
# ------------------------------------------------------
"""
graph.stream(state) emits partial/complete updates
as the graph executes.

We print only the assistant's new message.
"""

def stream_graph_updates(user_input: str):
    state = {"messages": [{"role": "user", "content": user_input}]}

    # Stream events one-by-one
    for event in graph.stream(state):
        for value in event.values():
            print("Assistant:", value["messages"][-1]["content"])


# ------------------------------------------------------
# STEP 5: Run an infinite chat loop
# ------------------------------------------------------
"""
This keeps asking the user for input until they type quit/exit.
"""

if __name__ == "__main__":
    print("🤖 Chatbot is running! Type 'quit' to exit.\n")
    
    while True:
        try:
            user_input = input("User: ")

            if user_input.lower() in ["quit", "exit", "q"]:
                print("\nGoodbye! 👋")
                break

            # Send user message to the graph and stream output
            stream_graph_updates(user_input)

        except Exception as e:
            print(f"An error occurred: {e}")
            break
