from langchain_core.documents import Document
import os
from embeddings import T5LargeEmbedding, AllMiniLML6V2Embedding, AllMiniLML12V2Embedding
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
import PyPDF2


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

        return text


documents_dir_path = "./documents"
documents = []
for file in os.listdir(documents_dir_path):
    file_path = os.path.join(documents_dir_path, file)
    file_name, file_extension = os.path.splitext(file_path)
    if os.path.isfile(file_path):
        doc_content = ""
        if file_extension == ".pdf":
            doc_content = extract_text_from_pdf(file_path)
        else:
            with open(file_path, encoding='utf-8') as f:
                doc_content = f.read()
        documents.append(Document(page_content=doc_content, metadata={"source": file_path}))

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=500,
    chunk_overlap=50)
splits = text_splitter.split_documents(documents)
print("num splits:", len(splits))
embedding = AllMiniLML12V2Embedding(models_dir="./models")
vectorstore = InMemoryVectorStore.from_documents(documents=splits, embedding=embedding)
retriever = vectorstore.as_retriever()

question = "Welche Qualifikationen benötige ich?"

docs = retriever.invoke(question)
print("num relevant docs", len(docs))
print("Relevant docs:")
for doc in docs:
    print("----------------------------------------------------------------------------------------")
    print(doc.page_content)
