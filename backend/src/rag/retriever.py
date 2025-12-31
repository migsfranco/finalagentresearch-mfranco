"""Retriever factory for RAG pipeline."""

from langchain_core.retrievers import BaseRetriever

from .vector_store import VectorStoreManager


class RetrieverFactory:
    """Factory for creating retrievers from vector stores.

    Follows Factory Pattern for flexible retriever creation.
    """

    @staticmethod
    def create_similarity_retriever(
        vector_store_manager: VectorStoreManager,
        k: int = 3,
    ) -> BaseRetriever:
        """Create a similarity-based retriever.

        Args:
            vector_store_manager: Vector store manager instance.
            k: Number of documents to retrieve.

        Returns:
            Configured retriever.

        Raises:
            ValueError: If vector store not initialized.
        """
        if vector_store_manager.vector_store is None:
            raise ValueError("Vector store not initialized in manager")

        return vector_store_manager.vector_store.as_retriever(
            search_kwargs={"k": k}
        )

    @staticmethod
    def create_mmr_retriever(
        vector_store_manager: VectorStoreManager,
        k: int = 3,
        fetch_k: int = 10,
        lambda_mult: float = 0.5,
    ) -> BaseRetriever:
        """Create a Maximum Marginal Relevance (MMR) retriever.

        MMR balances relevance with diversity in results.

        Args:
            vector_store_manager: Vector store manager instance.
            k: Number of documents to retrieve.
            fetch_k: Number of documents to fetch before MMR.
            lambda_mult: Diversity factor (0 = max diversity, 1 = max relevance).

        Returns:
            Configured MMR retriever.

        Raises:
            ValueError: If vector store not initialized.
        """
        if vector_store_manager.vector_store is None:
            raise ValueError("Vector store not initialized in manager")

        return vector_store_manager.vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": k,
                "fetch_k": fetch_k,
                "lambda_mult": lambda_mult,
            },
        )
