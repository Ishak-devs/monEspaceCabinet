from docx.shared import RGBColor


def build_section_formation(doc, data):
    table = doc.add_table(rows=1, cols=2)
    table.style = None
    cells = table.rows[0].cells

    for diplome in data.get('Diplômes', []):
        p_left = cells[0].paragraphs[0]
        run_dip = p_left.add_run(diplome.get('Diplôme', ''))
        run_dip.bold = True
        run_dip.font.color.rgb = RGBColor(0x00, 0x20, 0x60)

        p_right = cells[1].paragraphs[0]
        p_right.alignment = 2
        run_date = p_right.add_run(str(diplome.get('Année', '')))
        run_date.font.color.rgb = RGBColor(0x00, 0x20, 0x60)