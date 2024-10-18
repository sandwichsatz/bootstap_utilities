from transformers import GPTNeoForCausalLM, GPT2Tokenizer
from langchain_core.documents import Document
from langchain.embeddings.base import Embeddings
from transformers import AutoModel, AutoTokenizer
from langchain_community.vectorstores import Chroma
import torch
from pathlib import Path

all_mini_model_path = str(Path.home().joinpath('PycharmProjects', 'CondaTest', 'models', 'all-MiniLM-L6-v2'))

# Documents
documents=[
    Document("My favorite pet is a cat."),
    Document("Last summer I visited Paris."),
    Document("it is 5 pm."),
    Document("Next sunday will be sunny."),
    Document("My train was late."),
]


# Check if CUDA is available
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")


class CustomEmbeddings(Embeddings):
    def __init__(self, model_name: str, device: str = "cuda"):
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)

    def embed_documents(self, documents):
        embeddings = []
        for doc in documents:
            inputs = self.tokenizer(doc, return_tensors='pt', truncation=True, padding=True).to(self.device)
            with torch.no_grad():
                model_output = self.model(**inputs)
            # Mean pooling
            embeddings.append(model_output.last_hidden_state.mean(dim=1).squeeze().cpu().numpy().tolist())
        return embeddings

    def embed_query(self, query):
        inputs = self.tokenizer(query, return_tensors='pt', truncation=True, padding=True).to(self.device)
        with torch.no_grad():
            model_output = self.model(**inputs)
        return model_output.last_hidden_state.mean(dim=1).squeeze().cpu().numpy().tolist()


custom_embeddings = CustomEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", device=device)

# Split
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=300,
    chunk_overlap=50)
splits = text_splitter.split_documents(documents)

# Create the Chroma vector store
vectorstore = Chroma.from_documents(documents=splits, embedding=custom_embeddings)
retriever = vectorstore.as_retriever()

question1 = "What kinds of pets do I like?"
question2 = "What did I do in my vacation?"
question3 = "What time is it?"

question = question1

docs = retriever.invoke(question)
print("Relevant docs:")
for doc in docs:
    print(doc)

print("")

prompt_template = """Answer the question based only on the following context:
{context}

Question: {question}
"""

# Load the pre-trained GPT-2 model and tokenizer
model_name = "EleutherAI/gpt-neo-1.3B"
model = GPTNeoForCausalLM.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Function to generate response
def ask_question(question, max_length=100, temperature=0.2):
    # Encode the question as input
    inputs = tokenizer.encode(question, return_tensors='pt')

    # Generate response
    outputs = model.generate(inputs, max_length=max_length, temperature=temperature, num_return_sequences=1)

    # Decode and return the response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

response = ask_question(prompt_template.replace("{context}", docs[0].page_content).replace("{question}", question))
print(f"Question: {question}")
print(f"Response: {response}")
