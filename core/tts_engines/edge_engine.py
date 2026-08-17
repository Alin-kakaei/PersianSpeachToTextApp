import asyncio
import edge_tts
from .base_engine import BaseTTSEngine

class EdgeTTSEngine(BaseTTSEngine):
    def __init__(self, voice="fa-IR-DilaraNeural"):
        self.voice = voice

    def generate(self, text: str, output_path: str) -> str:
        # We run the async Edge TTS synchronously inside the background thread
        asyncio.run(self._async_generate(text, output_path))
        return output_path

    async def _async_generate(self, text: str, output_path: str):
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_path)