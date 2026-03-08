from docx.shared import Pt

def display_mission(doc, exp):
    p_mission = doc.add_paragraph()
    run_mission = p_mission.add_run(f"Mission : {exp.get('Mission')}")
    p_mission.paragraph_format.space_before = Pt(10)
    p_mission.paragraph_format.space_after = Pt(10)