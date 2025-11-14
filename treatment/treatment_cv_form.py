from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog
)
from PyQt6.QtCore import Qt
import sys
from dc import handle_valid_cv  

class Treatment_cv_form(QWidget):

    def upload_cv(self):
        file_dialog = QFileDialog(self)
        file_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, False)
        file_dialog.setNameFilter("Documents (*.pdf *.doc *.docx)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if file_dialog.exec():
            self.selected_file = file_dialog.selectedFiles()[0]
            self.file_label.setText("Fichier sélectionné")
            print(f"File selected: {self.selected_file}")
        else:
            self.selected_file = None
            self.file_label.setText("Aucun fichier sélectionné.")

    def valider(self):
        if hasattr(self, "selected_file") and self.selected_file:
            print("Fichier validé :", self.selected_file)
            handle_valid_cv(self.selected_file)  
        else:
            print("⚠️ Aucun fichier sélectionné.")
            self.file_label.setText("⚠️ Veuillez sélectionner un fichier avant de valider.")

