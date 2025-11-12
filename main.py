import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QPushButton
from layout.form.form_cv import CVUploadForm
from layout.components.header.logo import LogoWidget
from PyQt6.QtCore import Qt, QTimer
from version.update.compare_version import compare_version
from layout.components.dialog.user_dialog import user_dialog
from treatment.path_ressources import ressources_path
from dotenv import load_dotenv

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        load_dotenv(ressources_path(".env"))

        self.setWindowTitle("NAVA")

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        central_widget = QWidget()
        self.stacked_widget.addWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        logo_widget = LogoWidget()
        main_layout.addWidget(logo_widget, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        main_layout.addStretch()

        btn_generate_dc = QPushButton("Générateur dossier de compétences")
        btn_generate_dc.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))   
        btn_generate_dc.setFixedSize(250, 20)
        
        main_layout.addWidget(btn_generate_dc, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()

        cv_form = CVUploadForm(navigate_home=lambda: self.stacked_widget.setCurrentIndex(0))
        self.stacked_widget.addWidget(cv_form)

        QTimer.singleShot(500, self.check_update)

    def check_update(self):
        if compare_version():
            user_dialog(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)  

    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())