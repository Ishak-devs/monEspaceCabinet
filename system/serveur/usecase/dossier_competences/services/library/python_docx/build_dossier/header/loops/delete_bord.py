def delete_bord(table):
    for row in table.rows:
            for cell in row.cells:
                for side in ["top", "left", "bottom", "right"]:
                    cell._tc.get_or_add_tcPr()
