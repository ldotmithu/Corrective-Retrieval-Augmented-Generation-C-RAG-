from pydantic import Field,BaseModel
from typing_extensions import TypedDict
from langchain_chroma import Chroma
from langchain_groq import ChatGroq

class AgentState(TypedDict):
    """ Shared state for the RAG system. """
    question: str
    agent_response: str
    vector_store: Chroma
    relevant_documents: list[str]
    model: ChatGroq

class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )
