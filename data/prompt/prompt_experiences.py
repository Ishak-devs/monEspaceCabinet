def prompt_experiences(cv_text):
    return f"""
Extrais TOUTES les expériences professionnelles du CV suivant et retourne un JSON valide.

- Une expérience = un poste dans une entreprise sur une période donnée
- Extrais les tâches complètes telles qu'elles apparaissent dans le CV, ne coupe pas les phrase, mais ne retourne pas d'émoji.
- Pour Durée_expérience retourne ce format : X ans ou X mois
- Retourne les expériences de la plus récente à la plus ancienne.
- Le nom de l'entreprise peut apparaître sur une ligne seule, avant ou après le poste, ou dans une phrase.

CV :
{cv_text}

Format de sortie (JSON uniquement, sans commentaires) :
{{
  "Experiences": [
    {{
      "Nom_Entreprise": "",
      "Poste": "",
      "Dates": "",
      "Durée_expérience": "",
      "Taches": [],
      "Logiciels": []
    }}
  ]
}}
"""