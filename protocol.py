from abc import ABC, abstractmethod
from typing import Dict, Any

class Comparator(ABC):
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def replay(self, transition_id: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def duplicate_event(self, event_id: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def recover(self, transition_id: str) -> str:
        raise NotImplementedError
