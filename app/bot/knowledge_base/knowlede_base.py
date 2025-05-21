from typing import List
from dataclasses import dataclass
from .store import KnowledgeBaseStore, ChromaKnowledgeBaseStore
from .preprocess import KnowledgeBasePreprocessor
from app.bot.memory.models import State
from typing_extensions import List, TypedDict
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate


class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


class KnowledgeBase:
    def __init__(self, **kwargs):
        """
        Initialize KnowledgeBase with vector store and processor dependencies

        Args:
            vector_store: Vector store for knowledge retrieval
            processor: Processor for handling knowledge base operations
        """
        self.store: KnowledgeBaseStore = ChromaKnowledgeBase()
        self.processor: KnowledgeBasePreprocessor = processor
        self.llm = ChatOpenAI(
            base_url=kwargs.get("base_url", "http://127.0.0.1:11434/v1"),
            api_key=kwargs.get("api_key", "not-need-for-local-models"),
            model_name=kwargs.get("model_name", "not-need-for-local-models"),
            temperature=kwargs.get("temperature", 0),
            extra_body={"max_tokens": kwargs.get("max_tokens", 4096)},
        )

    def train(self, documents: List[KnowledgeBaseDocument]):
        """
        Train the knowledge base using a list of documents

        Args:
            documents: List of documents to train the knowledge base
        """

        # Preprocess documents
        documents = await list_documents()

        # Process documents using the preprocessor
        preprocessed_documents = self.processor.preprocess(documents)

        # Add preprocessed documents to vector store
        self.store.add_documents(preprocessed_documents)

    def process(self, current_state: State) -> List[ChatMessage]:
        """
        Process the current state and generate content as chat messages

        Args:
            current_state: Current conversation/application state

        Returns:
            List[ChatMessage]: Generated content as list of chat messages
        """

        query = current_state.user_message.query

        # Get relevant knowledge from vector store based on current state
        relevant_knowledge = self.store.query(query, 5)

        docs_content = "\n\n".join(doc.page_content for doc in relevant_knowledge)

        prompt = ChatPromptTemplate.from_template("""Answer the question based only on the following context:
{context}
If the context does not contain the answer, say NO_ANSWER.
Question: {question}
""")

        messages = prompt.invoke({"question": query, "context": docs_content})

        response = self.llm.invoke(messages)

        return [{"text": response.content}]
