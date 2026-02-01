
import os
from dotenv import load_dotenv
from src.helper import load_pipeda_pdf, text_split, download_hugging_face_embeddings
from pinecone import Pinecone, ServerlessSpec 
from langchain_pinecone import PineconeVectorStore

load_dotenv()


PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

#Extract and Process Data
print(" Loading PIPEDA PDF...")
extracted_data = load_pipeda_pdf(data_path='data/')

print(" Splitting text into chunks...")
text_chunks = text_split(extracted_data)

print(" Downloading Hugging Face Embeddings...")
embeddings = download_hugging_face_embeddings()

#Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

#Change index name to match our PIPEDA project
index_name = "pipeda-bot-huggingface" 

#Create index if it doesn't exist
if index_name not in [idx.name for idx in pc.list_indexes()]:
    print(f" Creating new Pinecone index: {index_name}...")
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
else:
    print(f" Index {index_name} already exists.")

#Push Vectors to Pinecone
print(f" Uploading {len(text_chunks)} chunks to Pinecone. This might take a moment...")
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings, 
)

print(" Successfully indexed PIPEDA! Your knowledge base is ready.")