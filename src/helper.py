from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field, SkipValidation
from langchain_groq import ChatGroq
from typing_extensions import TypedDict
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import END, StateGraph, START
from langchain_tavily import TavilySearch
from src.State import AgentState
from rich.console import Console
from src.State import *

from dotenv import load_dotenv
load_dotenv()
import os 
from prompts.Agent_Prompt import GRADE_DOCUMENTS_PROMPT, QUESTION_REWRITER_PROMPT


PERSIST_DIR = "CHROMA-INDEX"

KNOWLEDGE_BASE_URLS = [
    "https://www.anthropic.com/engineering/building-effective-agents",
]


os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
os.environ["USER_AGENT"] = os.getenv("USER_AGENT", "CorrectiveRAG/1.0")


def get_model(shared_state:AgentState):
    shared_state['model'] = ChatGroq(model="qwen/qwen3-32b", temperature=0)
    return shared_state


console = Console()

def build_vector_store(shared_state: AgentState, urls=KNOWLEDGE_BASE_URLS) -> dict:
    """
    Build a Chroma vector store from a list of knowledge base URLs.

    Args:
        shared_state (dict): Dictionary to store shared objects like the vector store.
        urls (list): List of URLs to load documents from.

    Returns:
        dict: Updated shared_state with 'vector_store' retriever.
    """
    console.print("[yellow]⚡Chroma vector store...[/yellow]")

    # Load documents from all URLs
    loaded_docs = [WebBaseLoader(url).load() for url in urls]
    all_docs = [doc for sublist in loaded_docs for doc in sublist]

    # Split documents into smaller chunks for embeddings
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250,
        chunk_overlap=0
    )
    doc_chunks = text_splitter.split_documents(all_docs)

    # Create Chroma vector store
    vector_store = Chroma.from_documents(
        documents=doc_chunks,
        collection_name="rag-chroma",
        embedding=HuggingFaceEmbeddings()
    )

    # Store the retriever in shared_state
    shared_state['vector_store'] = vector_store.as_retriever()

    #console.print("[green]✅ Vector store built successfully![/green]")
    return shared_state

       


def get_relevant_documents(shared_state:AgentState):
    """
    Get relevant documents from the vector store.
    """
    question = shared_state["question"]
    vector_store = shared_state["vector_store"]

    documents = vector_store.invoke(question)
    shared_state["relevant_documents"] = [doc.page_content for doc in documents]

    return shared_state


def grade_and_filter_documents(shared_state:AgentState):
    """
    Grade the relevance of retrieved documents to a user question.
    """
    print("\n\n Grading documents for relevance... \n")
    question = shared_state['question']
    model = shared_state['model']
    documents = shared_state['relevant_documents']
    structured_llm_grader = model.with_structured_output(GradeDocuments)

    grade_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", GRADE_DOCUMENTS_PROMPT),
            ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
        ]
    )

    retrieval_grader = grade_prompt | structured_llm_grader
    filtered_documents = []

    for document in documents:
        grader_response = retrieval_grader.invoke({"question": question, "document": document})
        if grader_response.binary_score.lower() == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_documents.append(document)
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
    
    print("Relevant documents left after filtering:", len(filtered_documents))
    shared_state['relevant_documents'] = filtered_documents

    return shared_state


def generate_answer_from_documents(shared_state:AgentState):
    """ Generate an answer to the question using the relevant documents. """
    model = shared_state['model']
    rag_prompt = hub.pull("rlm/rag-prompt")
    question = shared_state['question']
    documents = shared_state['relevant_documents']

    rag_chain = rag_prompt | model | StrOutputParser()

    model_response = rag_chain.invoke({"context": documents, "question": question})
    shared_state['agent_response'] = model_response

    return shared_state


def decide_to_generate(shared_state:AgentState):
    """ Decide whether to generate an answer or perform a web search. """
    if len(shared_state['relevant_documents']) > 0:
        print("\n Generating answer from relevant documents... \n\n")
        return "generate"
    else:
        print("\n No relevant documents found, transform query and performing web search... \n\n")
        return "transform_query"


def transform_query(shared_state:AgentState):
    """
    Transform the query to produce a better question.
    """

    print("\n\n ---TRANSFORMING QUERY---")
    question = shared_state["question"]
    model = shared_state["model"]

    re_write_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", QUESTION_REWRITER_PROMPT),
            (
                "human",
                "Here is the initial question: \n\n {question} \n Formulate an improved question.",
            ),
        ]
    )
    question_rewriter = re_write_prompt | model | StrOutputParser()
    
    better_question = question_rewriter.invoke({"question": question})
    print("Transformed question: \n", better_question)
    shared_state['question'] = better_question
    
    return shared_state


def perform_web_search(shared_state):
    """ Perform a web search as a fallback. """
    print("\n\n Performing a Web Search--- \n\n")

    question = shared_state["question"]
    web_search_tool = TavilySearch(max_results=3)

    web_results = web_search_tool.invoke({"query": question})

    # Handle both dict (old) and list (new) formats
    documents = []
    if isinstance(web_results, dict) and "results" in web_results:
        documents = [r.get("content", "") for r in web_results["results"]]
    elif isinstance(web_results, list):
        # Newer versions return a list of results
        documents = [r.get("content", "") if isinstance(r, dict) else str(r) for r in web_results]

    if documents:
        print("First web search result:", documents[0][:200], "...\n")

    shared_state['relevant_documents'] = documents
    return shared_state

