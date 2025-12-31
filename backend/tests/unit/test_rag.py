"""Unit tests for RAG components."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.rag.document_loader import DocumentLoader


class TestDocumentLoader:
    """Tests for DocumentLoader."""

    def test_init_default_values(self) -> None:
        """Test default initialization values."""
        loader = DocumentLoader()
        assert loader.chunk_size == 1000
        assert loader.chunk_overlap == 200

    def test_init_custom_values(self) -> None:
        """Test custom initialization values."""
        loader = DocumentLoader(chunk_size=500, chunk_overlap=100)
        assert loader.chunk_size == 500
        assert loader.chunk_overlap == 100

    def test_load_pdf_file_not_found(self) -> None:
        """Test loading non-existent PDF raises error."""
        loader = DocumentLoader()
        with pytest.raises(FileNotFoundError):
            loader.load_pdf("/nonexistent/path/file.pdf")

    def test_load_pdf_invalid_extension(self, tmp_path: Path) -> None:
        """Test loading non-PDF file raises error."""
        # Create a temporary text file
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("test content")

        loader = DocumentLoader()
        with pytest.raises(ValueError, match="Expected PDF"):
            loader.load_pdf(txt_file)

    def test_load_documents_not_directory(self, tmp_path: Path) -> None:
        """Test loading from non-directory raises error."""
        # Create a file, not a directory
        file_path = tmp_path / "not_a_dir.txt"
        file_path.write_text("test")

        loader = DocumentLoader()
        with pytest.raises(NotADirectoryError):
            loader.load_documents(file_path)

    def test_load_documents_empty_directory(self, tmp_path: Path) -> None:
        """Test loading from empty directory returns empty list."""
        loader = DocumentLoader()
        result = loader.load_documents(tmp_path)
        assert result == []


class TestVectorStoreManager:
    """Tests for VectorStoreManager."""

    def test_load_existing_not_found(self, tmp_path: Path) -> None:
        """Test loading non-existent store raises error."""
        from src.rag.vector_store import VectorStoreManager

        manager = VectorStoreManager(
            persist_directory=tmp_path / "nonexistent",
        )
        with pytest.raises(FileNotFoundError):
            manager.load_existing()

    def test_get_or_create_no_documents_no_store(self, tmp_path: Path) -> None:
        """Test get_or_create fails without documents or store."""
        from src.rag.vector_store import VectorStoreManager

        manager = VectorStoreManager(
            persist_directory=tmp_path / "nonexistent",
        )
        with pytest.raises(ValueError, match="No existing vector store"):
            manager.get_or_create()

    def test_similarity_search_not_initialized(self, tmp_path: Path) -> None:
        """Test search fails when not initialized."""
        from src.rag.vector_store import VectorStoreManager

        manager = VectorStoreManager(
            persist_directory=tmp_path,
        )
        with pytest.raises(ValueError, match="not initialized"):
            manager.similarity_search("test query")

    def test_add_documents_not_initialized(self, tmp_path: Path) -> None:
        """Test add_documents fails when not initialized."""
        from src.rag.vector_store import VectorStoreManager

        manager = VectorStoreManager(
            persist_directory=tmp_path,
        )
        with pytest.raises(ValueError, match="not initialized"):
            manager.add_documents([])


class TestRetrieverFactory:
    """Tests for RetrieverFactory."""

    def test_create_similarity_retriever_not_initialized(self) -> None:
        """Test creating retriever from uninitialized manager fails."""
        from src.rag.retriever import RetrieverFactory
        from src.rag.vector_store import VectorStoreManager

        manager = MagicMock(spec=VectorStoreManager)
        manager.vector_store = None

        with pytest.raises(ValueError, match="not initialized"):
            RetrieverFactory.create_similarity_retriever(manager)

    def test_create_mmr_retriever_not_initialized(self) -> None:
        """Test creating MMR retriever from uninitialized manager fails."""
        from src.rag.retriever import RetrieverFactory
        from src.rag.vector_store import VectorStoreManager

        manager = MagicMock(spec=VectorStoreManager)
        manager.vector_store = None

        with pytest.raises(ValueError, match="not initialized"):
            RetrieverFactory.create_mmr_retriever(manager)
