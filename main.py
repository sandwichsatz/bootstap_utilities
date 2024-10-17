from document import Document
import os


def get_all_file_paths(directory):
    file_paths = []

    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            file_paths.append(file_path)

    return file_paths


document_file_paths = get_all_file_paths('./documents')
documents = [Document(file_path) for file_path in document_file_paths]

question = "On which continents are bees found?"
