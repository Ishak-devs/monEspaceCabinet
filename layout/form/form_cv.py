from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QCheckBox
from PyQt6.QtCore import Qt
from treatment.upload_cv import upload_cv
from treatment.fill_template import fill_template
from layout.components.buttons.backbutton import backbutton
from layout.components.header.logo import LogoWidget

class CVUploadForm(QWidget):
    def __init__(self, navigate_home=None):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(25)

        logo_widget = LogoWidget()
        layout.addWidget(logo_widget, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        backbutton(layout, navigate_home)

        """
                warning_label = QLabel("Il s'agit d'une première version, veillez à verifier le dossier généré")
                layout.addWidget(warning_label, alignment=Qt.AlignmentFlag.AlignCenter)
        """


        layout.addStretch()


        self.file_label = QLabel("")
        layout.addWidget(self.file_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.upload_btn = QPushButton("Sélectionner un cv")
        self.upload_btn.setEnabled(True)
        self.upload_btn.clicked.connect(lambda: upload_cv(self))
        layout.addWidget(self.upload_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.valider_btn = QPushButton("Générer un dossier")
        self.valider_btn.setEnabled(False)
        self.valider_btn.clicked.connect(lambda: fill_template(self))
        layout.addWidget(self.valider_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.english_cv = QCheckBox("CV en anglais", self)
        self.english_cv.setEnabled(False)
        layout.addWidget(self.english_cv, alignment=Qt.AlignmentFlag.AlignCenter)
        self.english_cv.setChecked(False)

        layout.addStretch()