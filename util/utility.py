import os
import sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_dir)

from typing import List

from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    TextLoader,
    CSVLoader,
    UnstructuredExcelLoader,
)
from langchain_core.documents import Document



class Utility:
    @staticmethod
    def read_file_content(file_path: str) -> list:
        """
        Reads and returns the content of a local file using LangChain loaders.
        If the file exists locally, it is used directly.

        Supported file types: .pdf, .docx, .txt, .csv, .xls, .xlsx.
        """

        if file_path.startswith("/"):
            file_path = file_path.lstrip("/")

        # Check if the file exists locally.
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Determine file extension and select the proper loader.
        extension = os.path.splitext(file_path)[1].lower()
        if extension == ".pdf":
            loader = PyPDFLoader(file_path)
            documents = loader.load()
        elif extension == ".docx":
            loader = UnstructuredWordDocumentLoader(file_path)
            documents = loader.load()
        elif extension == ".txt":
            loader = TextLoader(file_path)
            documents = loader.load()
        elif extension == ".csv":
            loader = CSVLoader(file_path)
            documents = loader.load()
        elif extension in [".xls", ".xlsx"]:
            loader = UnstructuredExcelLoader(file_path)
            documents = loader.load()
        elif extension == ".md":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            documents = [Document(page_content=text, metadata={"source": file_path})]
        else:
            raise ValueError(f"Unsupported file type: {extension}")

        return documents