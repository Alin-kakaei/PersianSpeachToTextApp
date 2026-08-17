import torch
import scipy.io.wavfile
from transformers import VitsModel, AutoTokenizer
from .base_engine import BaseTTSEngine


class HuggingFaceEngine(BaseTTSEngine):
    def __init__(self, model_id_or_path: str = "facebook/mms-tts-fas"):
        # This will load standard models from the Hub OR local directories of your fine-tunes
        self.tokenizer = AutoTokenizer.from_pretrained(model_id_or_path)
        self.model = VitsModel.from_pretrained(model_id_or_path)

    def generate(self, text: str, output_path: str) -> str:
        # 1. Tokenize Farsi text
        inputs = self.tokenizer(text, return_tensors="pt")

        # 2. Generate raw audio waveform arrays
        with torch.no_grad():
            output = self.model(**inputs).waveform

        # 3. Save to WAV file using the model's native sample rate
        waveform_array = output.squeeze().cpu().numpy()
        scipy.io.wavfile.write(output_path, rate=self.model.config.sampling_rate, data=waveform_array)

        return output_path