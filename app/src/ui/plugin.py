import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

app = QApplication(sys.argv)

window = QMainWindow()
window.setFixedSize(500, 500)
window.setWindowTitle("Plug-in Panel")

container = QWidget()
layout = QVBoxLayout(container)
layout.setContentsMargins(25, 25, 25, 25) # 좌, 상, 우, 하 여백
layout.setSpacing(0)
widget_title = QLabel("Plug-in Panel")
widget_title.setFont(QFont("Arial", 24))


widget_des = QLabel("Select Model")
widget_des.setFont(QFont("Arial", 14))


layout.addWidget(widget_title)
layout.addWidget(widget_des)
#layout.addStretch() 


window.setCentralWidget(container)
window.show()
sys.exit(app.exec())