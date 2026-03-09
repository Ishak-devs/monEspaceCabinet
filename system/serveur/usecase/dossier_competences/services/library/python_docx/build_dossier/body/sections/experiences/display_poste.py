from docx.shared import Pt, RGBColor


def display_poste(doc, exp):
    p_poste = doc.add_paragraph()
    p_poste.add_run(str(exp.get('Poste_Occupé', '')).upper())

    p_poste.paragraph_format.space_before = Pt(10)
    p_poste.paragraph_format.space_after = Pt(10)

    p_poste.paragraph_format.keep_with_next = True
