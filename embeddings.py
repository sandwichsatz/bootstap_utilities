import os
from abc import ABC, abstractmethod
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore
from transformers import T5Tokenizer, T5Model, AutoTokenizer, AutoModel
import torch


class Embedding(Embeddings, ABC):

    @abstractmethod
    def embed_text(self, text: str) -> list:
        """
        Embed the given text into a vector using the loaded local model.

        Args:
            text (str): The text to embed.

        Returns:
            list: The embedding vector for the text.
        """
        pass

    def embed_documents(self, texts:list) -> list:
        """
        Embed a list of documents.

        Args:
            texts (list): List of document texts to embed.

        Returns:
            list: A list of embedding vectors, one for each document.
        """
        print(texts)
        return [self.embed_text(text) for text in texts]

    def embed_query(self, text: str) -> list:
        """
        Embed a query.

        Args:
            text (str): The query text to embed.

        Returns:
            list: The embedding vector for the query.
        """
        return self.embed_text(text)


class T5LargeEmbedding(Embedding):
    def __init__(self, models_dir: str, device="cpu"):
        """
        Initialize the Embedding class with the path where all models are stored.

        Args:
            models_dir (str): The directory where all models are stored.
        """
        model_name = "t5-large"
        cache_dir = os.path.join(models_dir, model_name)
        self._device = torch.device(device)
        self.tokenizer = T5Tokenizer.from_pretrained(model_name, cache_dir=cache_dir)
        self.model = T5Model.from_pretrained(model_name, cache_dir=cache_dir).to(device)

    def embed_text(self, text: str) -> list:
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(self._device)
        with torch.no_grad():
            encoder_outputs = self.model.encoder(**inputs).last_hidden_state
            embeddings = encoder_outputs.mean(dim=1)  # Mean pooling
        return embeddings[0].numpy().tolist()


class AutoEmbedding(Embedding):
    def __init__(self, models_dir: str, model_name: str, device="cpu"):
        """
        Initialize the Embedding class with the path where all models are stored.

        Args:
            models_dir (str): The directory where all models are stored.
            model_name (str): The name of the model.
        """
        cache_dir = os.path.join(models_dir, model_name)
        self._device = torch.device(device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
        self.model = AutoModel.from_pretrained(model_name, cache_dir=cache_dir).to(device)

    def embed_text(self, text: str) -> list:
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(self._device)

        # Forward pass through the model to get embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Get the last hidden state (embedding vector)
        embeddings = outputs.last_hidden_state.mean(dim=1)  # Mean pooling over sequence of tokens

        # Convert to list and return
        return embeddings.squeeze().tolist()


class AllMiniLML6V2Embedding(AutoEmbedding):
    def __init__(self, models_dir: str):
        """
        Initialize the Embedding class with the path where all models are stored.

        Args:
            models_dir (str): The directory where all models are stored.
        """
        super().__init__(models_dir, "sentence-transformers/all-MiniLM-L6-v2")


class AllMiniLML12V2Embedding(AutoEmbedding):
    def __init__(self, models_dir: str):
        """
        Initialize the Embedding class with the path where all models are stored.

        Args:
            models_dir (str): The directory where all models are stored.
        """
        super().__init__(models_dir, "sentence-transformers/all-MiniLM-L12-v2")
