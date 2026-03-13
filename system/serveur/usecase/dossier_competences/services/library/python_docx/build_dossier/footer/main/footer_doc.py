from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

from usecase.dossier_competences.services.library.python_docx.build_dossier.footer.cellule_bas.cellule_bas import \
    cellule_bas
from usecase.dossier_competences.services.library.python_docx.build_dossier.footer.cellule_haut.cellule_haut import \
    cellule_haut


def footer_doc(doc, data):
    sect = doc.sections[0]
    tab = sect.footer.add_table(rows=2, cols=1, width=Cm(17))
    tab.alignment = WD_ALIGN_PARAGRAPH.CENTER

    cellule_haut(tab)
    cellule_bas(tab)

