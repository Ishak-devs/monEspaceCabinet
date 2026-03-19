from docx.shared import Cm

def add_marge(doc):

    for section in doc.sections:
        section.top_margin = Cm(2)
        section.left_margin = Cm(2)
        section.right_margin = Cm(2)