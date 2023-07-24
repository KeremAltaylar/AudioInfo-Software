import sys
import os
import wave
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Manipulator")
        self.setGeometry(100, 100, 500, 500)
        self.initUI()

    def initUI(self):
        # Create widgets
        self.label1 = QLabel("No audio file loaded.")
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setStyleSheet("border: 2px dashed #aaa; padding: 10px;")
        self.monitoring_box = QTextEdit()
        self.monitoring_box.setReadOnly(True)
        self.monitoring_box.setStyleSheet(
            "border: 2px dashed #aaa; padding: 10px;")
        self.button1 = QPushButton("Load Audio")
        self.button2 = QPushButton("Save Audio")
        self.button3 = QPushButton("Manipulate Audio")
        self.button2.setEnabled(False)
        self.button3.setEnabled(False)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.monitoring_box)
        h1 = QHBoxLayout()
        h1.addWidget(self.button1)
        h1.addWidget(self.button2)
        h1.addWidget(self.button3)
        layout.addLayout(h1)

        # Set widget layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Connect button signals
        self.button1.clicked.connect(self.loadAudio)
        self.button2.clicked.connect(self.saveAudio)
        self.button3.clicked.connect(self.manipulateAudio)

    def loadAudio(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Audio", "", "Waveform Audio File Format (*.wav)")
        if file_path:
            with wave.open(file_path, 'rb') as f:
                self.audio_data = f.readframes(f.getnframes())
                self.sample_rate = f.getframerate()
                self.bit_depth = f.getsampwidth() * 8
                self.bit_rate = self.sample_rate * self.bit_depth
                self.sample_amount1 = f.getnframes()
                self.sample_length = 1 / self.sample_rate
                self.number_of_channels = f.getnchannels()
                self.sample_amountAll = f.getnchannels() * self.sample_amount1
                self.file_length = self.sample_amount1 / self.sample_rate
            self.label1.setText(
                f"Audio file loaded successfully: {os.path.basename(file_path)}")
            self.monitoring_box.setText(f"Sample rate: {self.sample_rate} Hz\n"
                                        f"Bit depth: {self.bit_depth} bits\n"
                                        f"Bit rate: {self.bit_rate} bps\n"
                                        f"Sample amount 1 channel: {self.sample_amount1} samples\n"
                                        f"Number of Channels: {self.number_of_channels} chanels\n"
                                        f"Sample amount all channels: {self.sample_amountAll} samples\n"
                                        f"File length: {self.file_length:.2f} seconds\n"
                                        f"Sample length: {self.sample_length:.10f} seconds")
            self.button2.setEnabled(True)
            self.button3.setEnabled(True)

    def saveAudio(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Audio", "", "Waveform Audio File Format (*.wav)")
        if file_path:
            with open(file_path, 'wb') as f:
                f.write(self.audio_data)
                self.label1.setText("Audio file saved successfully!")
                self.button2.setEnabled(False)
                self.button3.setEnabled(True)

    def manipulateAudio(self):
        # Implement audio manipulation code here
        self.label1.setText("Audio manipulated successfully!")
        self.monitoring_box.setText("")
        self.button2.setEnabled(False)
        self.button3


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
