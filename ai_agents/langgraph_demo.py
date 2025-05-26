# Essay writing agent using LangGraph
import os
import sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_dir)


from typing import TypedDict

from langgraph.graph import StateGraph, END


class EssayState(TypedDict):
    # State Representation
    question: str
    summary: str
    outline: str
    essay: str