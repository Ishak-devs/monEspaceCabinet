from usecase.dossier_competences.services.library.python_docx.build_dossier.body.section_competences import \
    section_competences
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.section_outils import section_outils
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.section_secteurs_activites import \
    section_secteurs_activites


def body_doc(doc, data):
    section_competences(doc, data)
    section_outils(doc, data)
    section_secteurs_activites(doc, data)