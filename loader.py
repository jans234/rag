from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import shutil
load_dotenv()

print("laoding Started")
embeddings = OpenAIEmbeddings()

# loading pdf
file_path = "./Dataset/Pakistan_ang_010117.pdf"
loader = PyPDFLoader(file_path)
docs = loader.load()


# text splitting
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=5000,
    chunk_overlap=1000,
    length_function=len,
    is_separator_regex=False,
)
texts = text_splitter.create_documents([doc.page_content for doc in docs])
texts = [doc.page_content for doc in texts]

# laoding data into chroma
if os.path.exists("./chromadb"):
        shutil.rmtree("./chromadb")
vectorstore = Chroma(
        persist_directory="./chromadb",
        embedding_function=embeddings,
        collection_name="laws"
        )
Chroma.add_texts(vectorstore, texts)
print("laoding completed")