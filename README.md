# Corrective Retrieval-Augmented Generation (C-RAG) 🚀

Welcome to **C-RAG**! This project implements a **Corrective Retrieval-Augmented Generation** system to deliver accurate and relevant answers to your questions by combining document retrieval, relevance grading, query transformation, and web search. Built with Python and modern AI tools, it’s designed to be robust and extensible. Let’s dive in! 🌟

Read the research paper: arXiv:2401.15884

## 📖 Overview

C-RAG enhances the traditional Retrieval-Augmented Generation (RAG) framework by:
- 📚 **Retrieving** documents from a knowledge base using a Chroma vector store.
- ✅ **Grading** documents for relevance to ensure only the best content is used.
- ✍️ **Transforming** queries to improve retrieval when needed.
- 🌐 **Searching the web** as a fallback for missing information.
- 💬 **Generating** precise answers using a language model.

The system is powered by **LangChain**, **Chroma**, **HuggingFace embeddings**, **Grok**, and **Tavily** for web searches, orchestrated via a **StateGraph** workflow. 🎛️

## ✨ Features

- **Corrective Mechanism**: Filters out irrelevant documents to improve answer quality. 🛡️
- **Persistent Vector Store**: Saves processed documents for fast reuse. 💾
- **Web Search Fallback**: Uses Tavily to fetch real-time web data when needed. 🌍
- **Interactive CLI**: User-friendly interface with `rich` for styled outputs. 🖥️
- **Modular Workflow**: Extensible graph-based architecture for easy customization. 🧩

## 🛠️ Installation

Get started in a few simple steps! 🚧

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ldotmithu/Corrective-Retrieval-Augmented-Generation-C-RAG-.git
   cd Corrective-Retrieval-Augmented-Generation-C-RAG-
   ```

2. **Install Dependencies**:
   Ensure Python 3.8+ is installed, then run:
   ```bash
   pip install langchain langchain-chroma langchain-groq langchain-huggingface langchain-community pydantic rich python-dotenv langgraph
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the project root:
   ```plaintext
   GROQ_API_KEY=your_groq_api_key
   TAVILY_API_KEY=your_tavily_api_key
   USER_AGENT=CorrectiveRAG/1.0
   ```
   Get your API keys from [xAI](https://x.ai/api) for Grok and [Tavily](https://tavily.com) for web search.

4. **Run the Application**:
   ```bash
   python main.py
   ```

## 🎮 Usage

1. Launch the app and see the welcome panel! 🎉
2. Enter your question at the prompt (e.g., `What is an LLM agent?`). ❓
3. The system will:
   - Search the knowledge base (Chroma vector store). 📚
   - Grade documents for relevance. ✅
   - Rewrite the query or perform a web search if needed. 🌐
   - Generate a clear, concise answer. 💬
4. Type `exit`, `quit`, or `q` to stop. 👋

### Example
```plaintext
You: What is an LLM agent?
Agent: An LLM agent is a system that leverages a large language model to perform tasks autonomously by combining reasoning, planning, and interaction with external tools or environments. It typically uses a prompt-driven approach to process inputs, make decisions, and generate responses, often augmented with memory or retrieval mechanisms to access relevant information. For example, an LLM agent might retrieve documents from a knowledge base or perform web searches to answer complex queries, as described in sources like Lilian Weng’s blog on agents. 🧠
```

## 📂 Project Structure

```
Corrective-Retrieval-Augmented-Generation-C-RAG-/
├── src/
│   ├── helper.py          # Utility functions 🛠️
│   ├── State.py           # AgentState definition 📋
│   ├── Workflow.py        # Graph workflow setup 🧩
├── prompts/
│   ├── Agent_Prompt.py    # Prompts for grading and query rewriting ✍️
├── main.py                # Main application entry point 🚀
├── .env                   # Environment variables 🔐
├── README.md              # This file! 📖
```

## 🔧 How It Works

1. **Initialize Model**: Uses `ChatGroq` (e.g., `qwen/qwen3-32b`) for generation and grading. 🤖
2. **Build Vector Store**: Loads documents from URLs (e.g., Lilian Weng’s blog posts), splits them into chunks, and stores them in a persistent Chroma vector store. 📦
3. **Retrieve Documents**: Fetches relevant documents based on the user’s question. 🔍
4. **Grade Documents**: Filters documents using a binary relevance score (`yes`/`no`). ✅
5. **Transform Query**: Rewrites the question if no relevant documents are found. ✍️
6. **Web Search**: Falls back to Tavily for external content if needed. 🌐
7. **Generate Answer**: Combines the question and documents to produce a final response. 💬

The workflow is managed by a `StateGraph`, ensuring a clear and efficient pipeline. 🛤️

## 📚 Knowledge Base

The default knowledge base includes:
- [Lilian Weng’s blog on LLM agents](https://lilianweng.github.io/posts/2023-06-23-agent/) 🧠
- [Lilian Weng’s blog on LLM adversarial attacks](https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/) 🛡️

You can modify `KNOWLEDGE_BASE_URLS` in the code to add your own sources! 🌟

## 🤝 Contributing

We welcome contributions! 🎉 To contribute:
1. Fork the repository. 🍴
2. Create a feature branch (`git checkout -b feature/YourFeature`). 🌿
3. Commit your changes (`git commit -m "Add YourFeature"`). 💾
4. Push to the branch (`git push origin feature/YourFeature`). 🚀
5. Open a Pull Request. 📬

Please include clear descriptions and test your changes thoroughly. 🧪

## ⚠️ Limitations

- **Limited Knowledge Base**: Relies on predefined URLs; expand for broader coverage. 📚
- **API Dependency**: Requires Grok and Tavily API keys. 🔑
- **No Graph Visualization**: Workflow graph exists but isn’t displayed by default. 📊
- **Prompt Dependency**: Relies on external prompt definitions (`Agent_Prompt.py`). 📝

## 🌟 Future Improvements

- 📝 Add detailed documentation for prompts and helper functions.
- 🌐 Support custom knowledge base URLs or local files.
- 🖼️ Integrate workflow visualization using Mermaid diagrams.
- 🛠️ Enhance error handling for robust API interactions.
- 🤖 Support additional language models or embedding providers.

## 📜 License

© 2025 GitHub, Inc. See the repository for full license details. 📜

## 📬 Contact

For questions or suggestions, open an issue on the [GitHub repository](https://github.com/ldotmithu/Corrective-Retrieval-Augmented-Generation-C-RAG-) or reach out via GitHub. Let’s make C-RAG even better! 🚀

---

Happy querying with C-RAG! 🎉
