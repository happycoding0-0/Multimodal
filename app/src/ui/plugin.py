import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QLabel,
    QMainWindow,
    QRadioButton,
    QVBoxLayout,
    QWidget,
    QHBoxLayout
)

app = QApplication(sys.argv)

window = QMainWindow()
window.setFixedSize(500, 500)
window.setWindowTitle("Plug-in Panel")

container = QWidget()
layout = QVBoxLayout(container)
layout.setContentsMargins(25, 25, 25, 25)  # 좌, 상, 우, 하 여백
layout.setSpacing(0)

widget_title = QLabel("Plug-in Panel")
widget_title.setFont(QFont("Arial", 24))

widget_des = QLabel("Select Model")
widget_des.setFont(QFont("Arial", 14))

layout.addWidget(widget_title)
layout.addWidget(widget_des)

# 라디오 버튼 추가
radio_layout = QHBoxLayout()


radio_group = QButtonGroup(container)  # 그룹으로 묶어야 단일 선택됨

radio1 = QRadioButton("Model A")
radio2 = QRadioButton("Model B")
radio3 = QRadioButton("Model C")
radio1.setFont(QFont("Arial", 12))
radio2.setFont(QFont("Arial", 12))
radio3.setFont(QFont("Arial", 12))

radio1.setChecked(True)  # 기본 선택

radio_group.addButton(radio1)
radio_group.addButton(radio2)
radio_group.addButton(radio3)


radio_layout.addStretch()  # 왼쪽 여백을 채워서 버튼들을 오른쪽으로 밀어냄
layout.addWidget(radio1, alignment=Qt.AlignmentFlag.AlignRight)
layout.addWidget(radio2, alignment=Qt.AlignmentFlag.AlignRight)
layout.addWidget(radio3, alignment=Qt.AlignmentFlag.AlignRight)

# 선택 변경 시 동작 (선택 사항)
def on_selection_changed(button):
    print(f"선택됨: {button.text()}")

radio_group.buttonClicked.connect(on_selection_changed)

# layout.addStretch()
layout.addLayout(radio_layout)  # 가로 레이아웃을 세로 레이아웃에 삽입
window.setCentralWidget(container)
window.show()
sys.exit(app.exec())