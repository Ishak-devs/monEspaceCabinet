from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QCheckBox, QHBoxLayout, QRadioButton, QButtonGroup
from PyQt6.QtCore import Qt
from treatment.upload_cv import upload_cv
from treatment.fill_template import fill_template
from layout.components.buttons.backbutton import backbutton
from layout.components.header.logo import LogoWidget
from treatment.treatment_cv_form import Treatment_cv_form

class CVUploadForm(QWidget):
    def __init__(self, navigate_home=None):
        super().__init__() 
        self.navigate_home = navigate_home
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        logo_widget = LogoWidget()
        layout.addWidget(logo_widget, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        backbutton(layout, self.navigate_home)

        self.file_label = QLabel("")
        layout.addWidget(self.file_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.upload_btn = QPushButton("Sélectionner un cv")
        self.upload_btn.setEnabled(True)
        self.upload_btn.clicked.connect(lambda: upload_cv(self))
        layout.addWidget(self.upload_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.english_cv = QPushButton("Sélectionner un cv")
        self.english_cv.setEnabled(True)
        layout.addWidget(self.english_cv, alignment=Qt.AlignmentFlag.AlignCenter)

        cv_type_layout = QHBoxLayout()
        
        self.cv_simple = QRadioButton("CV simple", self)
        self.cv_simple.setEnabled(True)
        
        self.cv_complex = QRadioButton("CV complex", self)
        self.cv_complex.setEnabled(True)

        self.cv_type_group = QButtonGroup(self)
        self.cv_type_group.addButton(self.cv_simple)
        self.cv_type_group.addButton(self.cv_complex)

        cv_type_layout.addStretch()
        cv_type_layout.addWidget(self.cv_simple)
        cv_type_layout.addWidget(self.cv_complex)
        cv_type_layout.addStretch()

        layout.addLayout(cv_type_layout)

        self.label = QLabel("Générer un dossier de compétences :")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.valider_btn = QPushButton("Valider")
        self.valider_btn.clicked.connect(lambda: Treatment_cv_form(self))
        layout.addWidget(self.valider_btn)
