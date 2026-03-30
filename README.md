Projet de Génération de Dossier de Compétences

Ce projet utilise FastAPI et python-docx pour transformer des données JSON (extraites de CV) en documents Word (.docx) professionnels et stylisés.
🚀 Fonctionnalités

    Génération dynamique : Création de sections (Expériences, Compétences, Outils) avec mise en page complexe.

    Mise en forme avancée : Gestion du keep_with_next pour éviter les sauts de page orphelins.

    Header personnalisé : Insertion de logos et tableaux de métadonnées dans l'en-tête.

    API REST : Endpoint /endpoint/generate_dossier pour traiter les fichiers via stream.

🛠️ Installation
Bash

pip install fastapi python-docx uvicorn

📂 Structure du Code

    router.py : Gestion des requêtes API et des réponses StreamingResponse.

    services/ : Logique métier pour la manipulation des paragraphes et des styles Word.

    library/ : Fonctions utilitaires pour le formatage (Pt, Cm, RGBColor).

📖 Utilisation

Lancez le serveur :
Bash

uvicorn main:app --reload
