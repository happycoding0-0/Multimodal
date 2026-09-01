import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDial,
    QDoubleSpinBox,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QSlider,
    QSpinBox,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        
        
        self.setWindowTitle("Plugin Panel")
        
        label = QLabel("Plugin Panel")
        font = label.font()
        font.setPointSize(24)
        label.setFont(font)
        label.setStyleSheet("""padding: 10px;""") 
        label.setAlignment(
            Qt,Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        self.setCentralWidget()

        



