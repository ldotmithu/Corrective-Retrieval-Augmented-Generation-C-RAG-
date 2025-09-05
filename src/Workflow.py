from src.helper import *
from langgraph.graph import StateGraph, START, END
from src.State import AgentState
from IPython.display import Image
from src.helper import get_model,build_vector_store,get_relevant_documents,grade_and_filter_documents,generate_answer_from_documents,perform_web_search,transform_query

class BuildGraph:
    def __init__(self) -> None:
        pass
    
    def build_graph(self):
        workflow = StateGraph(AgentState)

        # Define the nodes
        workflow.add_node("get_model", get_model)
        workflow.add_node("build_vector_store", build_vector_store)
        workflow.add_node("get_relevant_documents", get_relevant_documents)
        workflow.add_node("grade_and_filter_documents", grade_and_filter_documents)
        workflow.add_node("generate_answer_from_documents", generate_answer_from_documents)
        workflow.add_node("perform_web_search", perform_web_search)  # web search
        workflow.add_node("transform_query", transform_query)

        # Build graph
        workflow.add_edge(START, "get_model")
        workflow.add_edge("get_model", "build_vector_store")
        workflow.add_edge("build_vector_store", "get_relevant_documents")
        workflow.add_edge("get_relevant_documents", "grade_and_filter_documents")
        workflow.add_conditional_edges(
            "grade_and_filter_documents",
            decide_to_generate,
            {
                "transform_query": "transform_query",
                "generate": "generate_answer_from_documents",
            },
        )
        workflow.add_edge("transform_query", "perform_web_search")
        workflow.add_edge("perform_web_search", "generate_answer_from_documents")
        workflow.add_edge("generate_answer_from_documents", END)

        # Compile
        return workflow.compile()
    
    def display_graph(self):
        graph = self.build_graph()
        return Image(graph.get_graph().draw_mermaid_png())
