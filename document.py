import os
import re


class Document:
    def __init__(self, document_file_path, max_chunk_length=500, allow_all_characters=False):
        self.name = os.path.basename(document_file_path)

        self.text = ""
        with open(document_file_path, 'r', encoding='utf-8') as file:
            self.text = file.read()
        self.text = _normalize_whitespace(self.text)
        if not allow_all_characters:
            self.text = _clean_text(self.text)
        sentences = _split_into_sentences(self.text)
        self.chunks = _split_sentences_into_chunks(sentences, max_chunk_length)


def _split_sentences_into_chunks(sentences, max_chunk_length):
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # If adding the sentence exceeds the chunk size `n`, store the current chunk and start a new one
        if len(current_chunk) + len(sentence) + 1 > max_chunk_length:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += " " + sentence

    # Add the last chunk
    if len(current_chunk) > 0:
        chunks.append(current_chunk.strip())

    return chunks


def _split_into_sentences(text):
    # Split the text by period (.), question mark (?), exclamation mark (!), colon (:) or semicolon (;)
    sentences = re.split(r'(?<=[.!?:;])\s+', text)
    return sentences


def _normalize_whitespace(text):
    # Replace all whitespace characters (tabs, newlines, etc.) with a single space
    return re.sub(r'\s+', ' ', text).strip()


def _clean_text(text):
    # Allow all printable ASCII characters (characters with ASCII values from 32 to 126)
    return re.sub(r'[^\x20-\x7E]', '', text)


text = "Hello! This is an example text: @#$%^&*(). Let's keep keyboard characters."
cleaned_text = _clean_text(text)
print(cleaned_text)
