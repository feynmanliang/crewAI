from typing import Any, Dict, Optional
from crewai.memory.memory import Memory
from crewai.memory.short_term.short_term_memory_item import ShortTermMemoryItem
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.mem0_storage import Mem0Storage


class ShortTermMemory(Memory):
    """
    ShortTermMemory class for managing transient data related to immediate tasks
    and interactions.
    Inherits from the Memory class and utilizes an instance of a class that
    adheres to the Storage for data storage, specifically working with
    MemoryItem instances.
    """

    def __init__(
        self, memory_provider=None, crew=None, embedder_config=None, storage=None
    ):
        self.memory_provider = memory_provider
        if self.memory_provider == "mem0":
            storage = Mem0Storage(type="short_term", crew=crew)
        else:
            storage = (
                storage
                if storage
                else RAGStorage(
                    type="short_term", embedder_config=embedder_config, crew=crew
                )
            )
        super().__init__(storage)

    def save(
        self,
        value: Any,
        metadata: Optional[Dict[str, Any]] = None,
        agent: Optional[str] = None,
    ) -> None:
        item = ShortTermMemoryItem(data=value, metadata=metadata, agent=agent)
        if self.memory_provider == "mem0":
            item.data = f"Remember the following insights from Agent run: {item.data}"

        super().save(value=item.data, metadata=item.metadata, agent=item.agent)

    def search(
        self,
        query: str,
        limit: int = 3,
        filters: dict = {},
        score_threshold: float = 0.35,
    ):
        return self.storage.search(
            query=query, limit=limit, filters=filters, score_threshold=score_threshold
        )  # type: ignore # BUG? The reference is to the parent class, but the parent class does not have this parameters

    def reset(self) -> None:
        try:
            self.storage.reset()
        except Exception as e:
            raise Exception(
                f"An error occurred while resetting the short-term memory: {e}"
            )
