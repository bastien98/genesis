import os
import pickle
import re
from rank_bm25 import BM25Okapi
from ports.file_storage_port import FileStoragePort


class LocalFileStorageAdapter(FileStoragePort):
    BM25_INDEX_FILENAME = "knowledge_base_bm25_index.pkl"

    def save_raw_file(self, document: bytes, location: str) -> None:
        directory = os.path.dirname(location)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"[INFO] Directory created: {directory}")
        else:
            print(f"[INFO] Directory already exists: {directory}")

        with open(location, 'wb') as f:
            f.write(document)
            print(f"Document saved at {location}")

    def save_md_chunks(self, chunks: list[str], location: str) -> None:
        directory = location if os.path.isdir(location) else os.path.dirname(location)
        if not os.path.exists(directory):
            os.makedirs(location, exist_ok=True)
            print(f"[INFO] Directory created: {location}")
        else:
            print(f"[INFO] Directory already exists: {location}")

        # Save each chunk in a numbered markdown file
        for index, chunk in enumerate(chunks, start=1):
            chunk_filename = f"chunk_{index}.md"
            chunk_path = os.path.join(location, chunk_filename)
            os.makedirs(location, exist_ok=True)
            with open(chunk_path, 'w') as chunk_file:
                chunk_file.write(chunk)
            print(f"[INFO] Saved chunk {index} to {chunk_path}")

    def save_text_chunks(self, chunks: list[str], location: str) -> None:
        directory = location if os.path.isdir(location) else os.path.dirname(location)
        if not os.path.exists(directory):
            os.makedirs(location, exist_ok=True)
            print(f"[INFO] Directory created: {location}")
        else:
            print(f"[INFO] Directory already exists: {location}")

        # Save each chunk in a numbered markdown file
        for index, chunk in enumerate(chunks, start=1):
            chunk_filename = f"chunk_{index}.txt"
            chunk_path = os.path.join(location, chunk_filename)
            os.makedirs(location, exist_ok=True)
            with open(chunk_path, 'w') as chunk_file:
                chunk_file.write(chunk)
            print(f"[INFO] Saved chunk {index} to {chunk_path}")

    def read_text_chunks(self, location: str) -> list[str]:
        text_chunks = []

        if not os.path.isdir(location):
            raise ValueError(f"The location '{location}' is not a valid directory.")

        # Function to extract the numeric value from the filename for proper sorting
        def natural_key(filename):
            return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', filename)]

        # Get all txt files and sort them using the natural key
        sorted_filenames = sorted([f for f in os.listdir(location) if f.endswith('.txt')], key=natural_key)

        for filename in sorted_filenames:
            file_path = os.path.join(location, filename)

            if os.path.isfile(file_path) and filename.endswith('.txt'):
                with open(file_path, 'r') as file:
                    text_chunks.append(file.read())

        return text_chunks

    def save_BM25_index(self, bm25_index: BM25Okapi, location: str) -> None:
        with open(location, 'wb') as f:
            pickle.dump(bm25_index, f)

    def read_BM25_index(self, location: str) -> BM25Okapi:
        with open(str(location), mode='rb') as f:
            bm25_index = pickle.load(f)
            return bm25_index
