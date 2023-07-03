import os
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings 
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
# embeddings = SentenceTransformerEmbeddings(model_name="./cross-en-de-roberta-sentence-transformer")
loader = CSVLoader(file_path="german.csv")


documents = loader.load()


# embeddings = HuggingFaceInstructEmbeddings(model_name = "./model/instructor-xl")

db = FAISS.from_documents(documents, embeddings)

db.save_local("faiss_openai")