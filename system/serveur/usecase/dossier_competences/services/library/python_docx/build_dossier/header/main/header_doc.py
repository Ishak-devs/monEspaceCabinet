from usecase.dossier_competences.services.library.python_docx.build_dossier.header.left.header_left import header_left

from usecase.dossier_competences.services.library.python_docx.build_dossier.header.right.header_right import \
    header_right

def header_doc(doc, data, logo_path):
    header_left(logo_path, doc)
    header_right(data)
