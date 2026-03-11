def main_prompt(cv_text, current_template):

    return f"""En tant qu'expert pour un cabinet de conseil, analyse ce CV
     pour générer un dossier de compétences valorisant en reformulant et complétant intelligemment
      le JSON suivant : {current_template} 
      à partir de {cv_text}, 
      sans aucun commentaire.
"""