import os
import getpass

from langchain_openai import ChatOpenAI

from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from pydantic import SecretStr

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = SecretStr(os.environ.get("OPENAI_API_KEY", ""))
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE")


class State(TypedDict):
    messages: Annotated[list[str], add_messages]


graph_builder = StateGraph(State)

llm = ChatOpenAI(model="gpt-4o-mini",api_key=OPENAI_API_KEY if OPENAI_API_KEY else None,base_url=OPENAI_API_BASE)

def set_env(var: str)->None:
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"请输入环境变量 key {var}")

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}



graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


def main():
    set_env("OPENAI_API_KEY")
    set_env("OPENAI_API_BASE")
    print(1)


    return graph
    
    # while True:
    #     try:
    #         user_input = input("User: ")
    #         if user_input.lower() in ["quit", "exit", "q"]:
    #             print("Goodbye!")
    #             break

    #         stream_graph_updates(user_input)
    #     except:
    #         # fallback if input() is not available
    #         user_input = "What do you know about LangGraph?"
    #         print("User: " + user_input)
    #         stream_graph_updates(user_input)
    #         break

if __name__ == "__main__":
    main()
