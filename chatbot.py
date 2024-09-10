from openai import OpenAI
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
load_dotenv()

def pak_law_gpt(question):
    embeddings = OpenAIEmbeddings()
    def AskAI(messages:list):
        client = OpenAI()
        response = client.chat.completions.create(
        temperature=0,
        model="gpt-4o-mini",
        messages=messages
        )
        return response.choices[0].message.content

    def retriver(question:str):
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma(
            persist_directory="./chromadb",
            embedding_function=embeddings,
            collection_name="laws"
            )
        DOCS = []
        for i in vectorstore.similarity_search(question, k=4):
            DOCS.append(i.page_content)
        return DOCS

    PROMPT = """You are an expert on the Constitution of Pakistan. Your role is to provide detailed and accurate answers to any questions related to the Constitution, its articles, amendments, and legal framework.
    If someone greets you with phrases like 'hi' or 'hello,' respond with: 'Hello! How can I help you with questions about the Constitution of Pakistan?'
    You should answer all related Pakistani Law, and constitution.
    If someone asks you anything unrelated, kindly respond by saying: 'Sorry, I am only able to provide answers about the Constitution of Pakistan. Please ask me questions related to that topic.'
    Ensure that all of your responses are focused solely on the Constitution of Pakistan, and do not address any topics outside of this subject matter."""

    DOC_PROMPT = ''
    docs = retriver(question)
    for doc in docs:
        DOC_PROMPT += "\n" + doc
    messages = [
        {
            "role": "system",
            "content": PROMPT
        },
        {
            "role": "system",
            "content": DOC_PROMPT
        },
        {
            "role": "user",
            "content":question
        }
    ]
    answer = AskAI(messages)
    return answer
