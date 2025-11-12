from PyQt6.QtWidgets import QMessageBox, QApplication
from version.update.update_app import update_app

def user_dialog(self):
    msg = QMessageBox()
    msg.setWindowTitle('Mise à jour logiciel')
    msg.setText('Mise à jour disponible')

    msg.setInformativeText('Mettre à jour ?')

    msg.setDetailedText(
        ""
    )

    msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

    result = msg.exec()

    if result == QMessageBox.StandardButton.Yes:
        update_app()
    else:
        pass