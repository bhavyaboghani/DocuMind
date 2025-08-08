# test_backend.py

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.cohere import Cohere
from llama_index.core.settings import Settings
import os

cohere_api_key = "706SqLvA7kuktqALilzbE0ouZKwGmw7IMSvEaY1B"  # Replace with actual key

embed_model = CohereEmbedding(cohere_api_key=cohere_api_key)
llm = Cohere(api_key=cohere_api_key, model="command-r-plus", temperature=0.3, max_tokens=128)

Settings.embed_model = embed_model
Settings.llm = llm

query_engine = None

def build_query_engine():
    global query_engine
    if not os.path.exists("data"):
        os.makedirs("data")
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()

def ask_bot(question):
    if query_engine is None:
        build_query_engine()
    response = query_engine.query(question)
    return str(response)
