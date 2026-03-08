from docx.shared import Cm

from usecase.dossier_competences.services.library.python_docx.build_dossier.header.loops.delete_bord import delete_bord

def header_left(logo_path, cell_gauche):
    paragraph = cell_gauche.paragraphs[0]
    run_logo = paragraph.add_run()
    run_logo.add_picture(logo_path, width=Cm(3))

    # delete_bord()