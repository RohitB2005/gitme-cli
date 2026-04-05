from abc import ABC, abstractmethod

class BaseProvider(ABC):

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Send prompts to the LLM and return commit message."""
        pass
