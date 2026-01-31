# PIPEDA-Intelligence-Bot

An AI-powered legal research assistant designed to navigate the Personal Information Protection and Electronic Documents Act (PIPEDA). Built using a RAG (Retrieval-Augmented Generation) architecture to ensure factually grounded, source-cited responses.

# Key Features

Fact-Grounded Responses: Prevents LLM hallucinations by anchoring answers in the official Justice Canada statutory text.

Precision Retrieval: Uses Pinecone vector embeddings to find specific legal clauses within seconds.

Context-Aware Splitting: Implements RecursiveCharacterTextSplitter to maintain the hierarchy of legal subsections and parts.

Source Attribution: Every response includes direct citations from the Act (e.g., "According to Section 7(3)...").

# Tech Stack

LLM: Google Gemini 2.5 Flash

Orchestration: LangChain

Vector DB: Pinecone

Backend: Flask (Python)

Deployment: AWS
