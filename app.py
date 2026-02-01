from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from src.prompt import system_prompt
import os

app = Flask(__name__)

# 1. Load Environment Variables
load_dotenv()
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# 2. Initialize Embeddings & Vector Store
print("Initializing Embeddings...")
embeddings = download_hugging_face_embeddings()

# Must match the index name you used in store_index.py
index_name = "pipeda-bot-huggingface" 

# Connect to the existing Pinecone index
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

# 3. Setup Retriever (Fetch top 3 most relevant chunks)
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

# 4. Initialize Gemini LLM
# transport="rest" avoids the DefaultCredentialsError
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    max_tokens=2000,
    transport="rest"
)

# 5. Create the Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# 6. Build the RAG Chain using LCEL (The Fix)
# This removes the dependency on 'langchain.chains'
rag_chain = (
    {
        "context": retriever, 
        "input": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

# --- Routes ---

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(f"User Query: {input}")
    
    # Note: With RunnablePassthrough, we pass the raw string 'msg', not a dict
    response = rag_chain.invoke(msg)
    
    print("Response : ", response)
    return str(response)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)