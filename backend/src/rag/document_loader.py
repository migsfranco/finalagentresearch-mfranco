"""Document loading and chunking for RAG pipeline."""

from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentLoader:
    """Load and chunk documents for RAG pipeline.

    Follows Single Responsibility Principle - only handles document loading.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        """Initialize document loader.

        Args:
            chunk_size: Size of text chunks.
            chunk_overlap: Overlap between chunks.
        """
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap
        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

    def load_pdf(self, file_path: str | Path) -> list[Document]:
        """Load and chunk a PDF document.

        Args:
            file_path: Path to the PDF file.

        Returns:
            List of chunked documents.

        Raises:
            FileNotFoundError: If the file doesn't exist.
            ValueError: If the file is not a PDF.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {path}")

        if path.suffix.lower() != ".pdf":
            raise ValueError(f"Expected PDF file, got: {path.suffix}")

        loader = PyPDFLoader(str(path))
        docs = loader.load()

        return self._text_splitter.split_documents(docs)

    def load_documents(self, directory: str | Path) -> list[Document]:
        """Load all PDF documents from a directory.

        Args:
            directory: Path to the directory containing PDFs.

        Returns:
            List of all chunked documents.
        """
        path = Path(directory)
        if not path.is_dir():
            raise NotADirectoryError(f"Not a directory: {path}")

        all_chunks = []
        for pdf_file in path.glob("*.pdf"):
            chunks = self.load_pdf(pdf_file)
            all_chunks.extend(chunks)

        return all_chunks

    @property
    def chunk_size(self) -> int:
        """Get the chunk size."""
        return self._chunk_size

    @property
    def chunk_overlap(self) -> int:
        """Get the chunk overlap."""
        return self._chunk_overlap
