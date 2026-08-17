import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QPushButton,
                             QVBoxLayout, QWidget, QComboBox, QMessageBox)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from core.audio_controller import AudioWorker
from core.tts_engines.edge_engine import EdgeTTSEngine
from core.tts_engines.hf_engine import HuggingFaceEngine


class DigitalTwinUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Farsi TTS Architecture Engine")
        self.resize(600, 400)

        # Audio Setup
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        # Engine caching (so we don't reload heavy HF models into RAM every click)
        self.cached_engines = {
            "Edge TTS (Fast, Cloud)": None,
            "HuggingFace MMS (Local, Fine-Tuning base)": None
        }

        # UI Layout
        layout = QVBoxLayout()

        # Model Selector Dropdown
        self.model_selector = QComboBox()
        self.model_selector.addItems(self.cached_engines.keys())
        self.model_selector.setStyleSheet("font-size: 14px; padding: 5px;")
        layout.addWidget(self.model_selector)

        # Text Area
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("سلام، من آماده خواندن متن شما هستم...")
        self.text_input.setStyleSheet("font-size: 16px; padding: 10px; font-family: Tahoma;")
        self.text_input.setLayoutDirection(sys.modules['PyQt6.QtCore'].Qt.LayoutDirection.RightToLeft)
        layout.addWidget(self.text_input)

        # Play Button
        self.play_btn = QPushButton("Process and Play")
        self.play_btn.setStyleSheet("font-size: 16px; padding: 10px;")
        self.play_btn.clicked.connect(self.on_play_clicked)
        layout.addWidget(self.play_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_play_clicked(self):
        text = self.text_input.toPlainText().strip()
        if not text:
            return

        self.play_btn.setEnabled(False)
        self.play_btn.setText("Loading Engine & Generating...")

        selected_model = self.model_selector.currentText()
        engine = self.get_engine(selected_model)

        # Fire off the background thread
        self.worker = AudioWorker(text, engine)
        self.worker.finished.connect(self.on_generation_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def get_engine(self, selection_name):
        # Lazy-loading: Only instantiate heavy models the first time they are selected
        if self.cached_engines[selection_name] is None:
            if "Edge" in selection_name:
                self.cached_engines[selection_name] = EdgeTTSEngine()
            elif "HuggingFace" in selection_name:
                # You can change this path to "./my_fine_tuned_weights" later
                self.cached_engines[selection_name] = HuggingFaceEngine("facebook/mms-tts-fas")

        return self.cached_engines[selection_name]

    def on_generation_finished(self, file_path):
        self.play_btn.setEnabled(True)
        self.play_btn.setText("Process and Play")
        self.player.setSource(QUrl.fromLocalFile(file_path))
        self.player.play()

    def on_error(self, err_msg):
        self.play_btn.setEnabled(True)
        self.play_btn.setText("Process and Play")
        QMessageBox.critical(self, "Error", f"Failed to generate audio:\n{err_msg}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DigitalTwinUI()
    window.show()
    sys.exit(app.exec())