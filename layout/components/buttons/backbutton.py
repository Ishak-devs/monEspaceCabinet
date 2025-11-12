from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt

def backbutton(layout, navigate_home=None):
    back_btn = QPushButton("← Retour")
    if navigate_home:
        back_btn.clicked.connect(navigate_home)
    layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignLeft)