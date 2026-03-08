from docx.shared import Cm

from usecase.dossier_competences.services.library.python_docx.build_dossier.header.loops.delete_bord import delete_bord

def header_left(logo_path, doc):
    section = doc.sections[0]
    header = section.header

    table = header.add_table(rows=1, cols=2, width=Cm(17))
    table.columns[0].width = Cm(5)
    table.columns[1].width = Cm(12)

    cells = table.rows[0].cells
    run_logo = cells[0].paragraphs[0].add_run()
    run_logo.add_picture(logo_path, width=Cm(3))

    delete_bord(table)
    return header_left(logo_path, doc)