from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from treatment.path_ressources import ressources_path

class LogoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("logoWidget")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Logo
        logo_label = QLabel()

        logo_path = ressources_path('ressources/logo.ico')

        print(logo_path)

        pixmap = QPixmap(logo_path).scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(logo_label)
