import os
from PyQt6.QtCore import QThread, pyqtSignal
from .text_processor import FarsiTextProcessor


class AudioWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, text, engine, output_filename="output.wav"):
        super().__init__()
        self.raw_text = text
        self.engine = engine  # The selected Strategy
        self.processor = FarsiTextProcessor()

        # Ensure absolute path for Windows PyQt6 playback
        self.output_path = os.path.abspath(output_filename)

    def run(self):
        try:
            # 1. Clean the text
            clean_text = self.processor.process(self.raw_text)

            # 2. Generate audio using whichever engine was passed in
            self.engine.generate(clean_text, self.output_path)

            # 3. Send absolute path back to UI
            self.finished.emit(self.output_path)
        except Exception as e:
            self.error.emit(str(e))