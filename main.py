import os
import json 
from fastapi import FastAPI, File, UploadFile
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings 
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
app = FastAPI() 

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
# embeddings = HuggingFaceInstructEmbeddings(model_name = "./model/instructor-base") #can use cpu or gpu , model_kwargs = {'device': device}
# embeddings = SentenceTransformerEmbeddings(model_name="./cross-en-de-roberta-sentence-transformer")


text = ""
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

Chatbot_template = '''In this conversation, {user_name} and {bot_name}, a GPT-based chatbot powered by {company_name}, discuss various topics. {bot_name} can provide factual responses based on the Context. The Context can be of two types. Previous question's context should be less prioritized than the Current question's context by {bot_name}. In the context, there will also be context from uploaded documents. {bot_name} needs to answer the questions related to documents if {user_name} asks. {bot_name} can do intermediate or higher level mathematical calculations. 
If {bot_name} cannot answer a question, it will explain why.  {bot_name} will remember {user_name}'s name and personal information. 
Context:
{context_doc}
Document:
{document}
Conversation History:
{history}
User:
{question}
Reply:''' 


llm = ChatOpenAI(model_name="gpt-3.5-turbo-0613", temperature=0) 
qa_prompt = PromptTemplate(template=Chatbot_template, input_variables=["context_doc", "document", "history", "question"], partial_variables={"user_name": "John Doe", "bot_name": "Bro-bot", "company_name": "Bro Corporation"})

chatbot_chain = LLMChain(
    llm = llm,
    prompt = qa_prompt,
    verbose=True
)
def produce_context_doc(query):
    
    db = FAISS.load_local("./faiss_openai", embeddings)
    docs = db.similarity_search_with_score(query, k = 1)

    context_doc =[doc[0].page_content for doc in docs]
        

    return context_doc


def generate_history_func(chat_history):
    if len(chat_history) == 0:
        return "Human: \nAI: \n"
    
    generated_history = ""
    for (user, ai) in chat_history:
        generated_history = generated_history + "Human: {}\nAI: {}\n".format(user, "")
    
    if len(generated_history) > 600:
        return generated_history[-600:]
    
    return generated_history


chat_history = []
last_context_doc = []

@app.post("/doc")
async def doc(file: UploadFile = File(...)):
    file = await file.read()
    text = file.decode("utf-8")
    doc = [Document(page_content=text)]
    with open('info.json', 'w', encoding='utf8') as json_file:
        json.dump(text, json_file)
    db = FAISS.from_documents(doc, embeddings)
    prev_db = FAISS.load_local("./faiss_openai", embeddings)
    prev_db.merge_from(db)
    prev_db.save_local("./faiss_openai")
    return "What do you wanna know from this document?"

@app.post("/pdf")
async def pdf(file: UploadFile = File(...)):
    file = await file.read()
    f = open("demo.pdf","wb")
    f.write(file)
    loader = PyPDFLoader("./demo.pdf")
    documents = loader.load_and_split()
    text = documents[0].page_content
    with open('info.json', 'w', encoding='utf8') as json_file:
        json.dump(text, json_file) 
    db = FAISS.from_documents(documents, embeddings)
    prev_db = FAISS.load_local("./faiss_openai", embeddings)
    prev_db.merge_from(db)
    prev_db.save_local("./faiss_openai")
    return "What do you wanna know from this document?"



@app.post("/qna")
def tax(question: str):
    """
    Get an answer to a question.
    """
    if(len(chat_history)==0):
        last_context_doc.append("")
    user_input = question
    
    try:
        with open('info.json', 'r') as json_file:
            text = json.load(json_file)
    except:
        text = ""
    context_doc = produce_context_doc(user_input)
    current_history = generate_history_func(chat_history)
    
    reply = chatbot_chain.predict(question=user_input, history = current_history, context_doc="Previous Questions Context: "+str(last_context_doc[-1])+"  Current Questions Context: "+str(context_doc), document = text)
    reply = reply.replace("\n","")
    chat_history.append((user_input,reply))
    if len(chat_history) > 5:
        chat_history.pop(0)
    
    last_context_doc.append(context_doc)
    return reply 
