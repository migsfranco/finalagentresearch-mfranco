"""RAG chain composition for APA citation correction."""

from pathlib import Path
from typing import Any

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from .document_loader import DocumentLoader
from .retriever import RetrieverFactory
from .vector_store import VectorStoreManager


APA_CORRECTION_PROMPT = ChatPromptTemplate.from_template("""
You are a specialist in APA 7th edition citation guidelines. Your task is to correct citations that are incorrectly formatted according to APA rules.

CONTEXT (APA 7th Edition Manual):
{context}

CITATION TO CORRECT:
{input}

INSTRUCTIONS:
1. Analyze the provided citation
2. Identify errors according to APA guidelines from the context
3. Provide the corrected citation
4. Briefly explain what was corrected and why

Respond in the following format:
**Original Citation:** [original citation]
**Corrected Citation:** [corrected citation]
**Explanation:** [explanation of corrections]

If the citation is already correct, indicate this and explain why it complies with APA guidelines.
""")


def format_docs(docs: list[Document]) -> str:
    """Format documents for context injection.

    Args:
        docs: List of documents to format.

    Returns:
        Formatted string with document contents.
    """
    return "\n\n".join(doc.page_content for doc in docs)


class APARagChain:
    """RAG chain for APA citation correction.

    Combines document retrieval with LLM to correct citations.
    """

    def __init__(
        self,
        pdf_path: str | Path | None = None,
        persist_directory: str | Path = "./data/chroma",
        collection_name: str = "apa_documents",
        model_name: str = "gpt-4o-mini",
        temperature: float = 0.0,
        retriever_k: int = 3,
    ):
        """Initialize APA RAG chain.

        Args:
            pdf_path: Path to APA manual PDF. If None, tries to load existing store.
            persist_directory: Directory for vector store persistence.
            collection_name: Name of the vector store collection.
            model_name: OpenAI model name.
            temperature: LLM temperature.
            retriever_k: Number of documents to retrieve.
        """
        self._pdf_path = pdf_path
        self._persist_directory = persist_directory
        self._collection_name = collection_name
        self._model_name = model_name
        self._temperature = temperature
        self._retriever_k = retriever_k

        self._chain = None
        self._vector_store_manager = None

    def _initialize(self) -> None:
        """Initialize the RAG chain components."""
        # Initialize document loader
        loader = DocumentLoader()

        # Initialize vector store
        self._vector_store_manager = VectorStoreManager(
            persist_directory=self._persist_directory,
            collection_name=self._collection_name,
        )

        # Load or create vector store
        if self._pdf_path:
            documents = loader.load_pdf(self._pdf_path)
            self._vector_store_manager.get_or_create(documents)
        else:
            self._vector_store_manager.load_existing()

        # Create retriever
        retriever = RetrieverFactory.create_similarity_retriever(
            self._vector_store_manager,
            k=self._retriever_k,
        )

        # Initialize LLM
        llm = ChatOpenAI(
            model=self._model_name,
            temperature=self._temperature,
        )

        # Build chain
        self._chain = (
            {"context": retriever | format_docs, "input": RunnablePassthrough()}
            | APA_CORRECTION_PROMPT
            | llm
            | StrOutputParser()
        )

    def invoke(self, citation: str) -> str:
        """Correct an APA citation.

        Args:
            citation: The citation to correct.

        Returns:
            Corrected citation with explanation.
        """
        if self._chain is None:
            self._initialize()

        return self._chain.invoke(citation)

    async def ainvoke(self, citation: str) -> str:
        """Asynchronously correct an APA citation.

        Args:
            citation: The citation to correct.

        Returns:
            Corrected citation with explanation.
        """
        if self._chain is None:
            self._initialize()

        return await self._chain.ainvoke(citation)

    def batch(self, citations: list[str]) -> list[str]:
        """Correct multiple citations.

        Args:
            citations: List of citations to correct.

        Returns:
            List of corrected citations.
        """
        if self._chain is None:
            self._initialize()

        return self._chain.batch(citations)
