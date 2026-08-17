from abc import ABC, abstractmethod

class BaseTTSEngine(ABC):
    @abstractmethod
    def generate(self, text: str, output_path: str) -> str:
        """
        Takes Farsi text and an output file path.
        Returns the absolute path to the generated audio file.
        """
        pass