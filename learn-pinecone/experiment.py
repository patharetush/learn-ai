import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone_text.sparse import BM25Encoder

index_name = "learn-pinecone"
pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# create the index
if index_name not in pinecone.list_indexes().names():
    pinecone.create_index(
        name=index_name,
        dimension=384,
        metric="dotproduct",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pinecone.Index(index_name)

## vector embeddings and sparse metrics
load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

bm25_encoder = BM25Encoder().default()

sentences = [
    "The cat sat on the mat.",
    "The dog sat on the log.",
    "The cat and the dog are friends.",
    "The mat is on the floor.",
    "The log is in the yard.",
]

## encode the sentences tfidf values on these sentences
bm25_encoder.fit(sentences)
bm25_encoder.dump("bm25_encoder.json")
