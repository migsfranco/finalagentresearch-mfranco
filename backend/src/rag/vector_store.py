"""Vector store management for RAG pipeline."""

from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings


class VectorStoreManager:
    """Manage ChromaDB vector store for RAG.

    Follows Single Responsibility Principle - only handles vector store operations.
    """

    def __init__(
        self,
        persist_directory: str | Path = "./data/chroma",
        collection_name: str = "apa_documents",
        embeddings: Embeddings | None = None,
    ):
        """Initialize vector store manager.

        Args:
            persist_directory: Directory to persist the vector store.
            collection_name: Name of the collection.
            embeddings: Embedding model. Defaults to OpenAI embeddings.
        """
        self._persist_directory = str(persist_directory)
        self._collection_name = collection_name
        self._embeddings = embeddings or OpenAIEmbeddings()
        self._vector_store: Chroma | None = None

    def create_from_documents(self, documents: list[Document]) -> Chroma:
        """Create vector store from documents.

        Args:
            documents: List of documents to index.

        Returns:
            Configured Chroma vector store.
        """
        self._vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self._embeddings,
            persist_directory=self._persist_directory,
            collection_name=self._collection_name,
        )
        return self._vector_store

    def load_existing(self) -> Chroma:
        """Load existing vector store from disk.

        Returns:
            Loaded Chroma vector store.

        Raises:
            FileNotFoundError: If persist directory doesn't exist.
        """
        persist_path = Path(self._persist_directory)
        if not persist_path.exists():
            raise FileNotFoundError(
                f"Vector store not found at: {self._persist_directory}"
            )

        self._vector_store = Chroma(
            persist_directory=self._persist_directory,
            embedding_function=self._embeddings,
            collection_name=self._collection_name,
        )
        return self._vector_store

    def get_or_create(self, documents: list[Document] | None = None) -> Chroma:
        """Get existing vector store or create new one.

        Args:
            documents: Documents to use if creating new store.

        Returns:
            Chroma vector store.
        """
        try:
            return self.load_existing()
        except FileNotFoundError:
            if documents is None:
                raise ValueError(
                    "No existing vector store found and no documents provided"
                )
            return self.create_from_documents(documents)

    @property
    def vector_store(self) -> Chroma | None:
        """Get the current vector store instance."""
        return self._vector_store

    def add_documents(self, documents: list[Document]) -> None:
        """Add documents to existing vector store.

        Args:
            documents: Documents to add.

        Raises:
            ValueError: If vector store not initialized.
        """
        if self._vector_store is None:
            raise ValueError("Vector store not initialized")
        self._vector_store.add_documents(documents)

    def similarity_search(
        self,
        query: str,
        k: int = 3,
    ) -> list[Document]:
        """Search for similar documents.

        Args:
            query: Search query.
            k: Number of results to return.

        Returns:
            List of similar documents.

        Raises:
            ValueError: If vector store not initialized.
        """
        if self._vector_store is None:
            raise ValueError("Vector store not initialized")
        return self._vector_store.similarity_search(query, k=k)
