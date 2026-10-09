from dotenv import load_dotenv
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_unstructured import UnstructuredLoader
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2",
)

vector_store = PineconeVectorStore(
    index_name=os.environ["INDEX_NAME"], embedding=embeddings
)

retriever = vector_store.as_retriever()

def load_docs():
    files = [os.path.join("docs", name) for name in os.listdir("docs")]
    loader = UnstructuredLoader(file_path=files)
    docs = loader.load()
    for file in files:
        os.remove(file)
    return docs


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=10, max=60),
    retry=retry_if_exception_type((ConnectionError, TimeoutError, OSError)),
)
def add_documents_with_retry(chunks):
    vector_store.add_documents(chunks)


if __name__ == "__main__":

    docs = load_docs()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    chunks = text_splitter.split_documents(docs)

    add_documents_with_retry(chunks)

    print(f"Added {len(chunks)} chunks to the vector store")    

    