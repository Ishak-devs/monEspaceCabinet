from usecase.dossier_competences.IA.prompt.clean.clean_prompt import clean_prompt
from usecase.dossier_competences.IA.prompt.main.main_prompt import main_prompt
from usecase.dossier_competences.services.data.reading.read_cv import read_cv
from services.api_externes.openrouter.call_openrouter import call_openrouter
import json

def analyse_data(file_path):
    cv_text = read_cv(file_path)
    if not cv_text:
        print("Erreur : Impossible de lire le texte du CV")
        return ""

    prompt_clean = clean_prompt(cv_text)
    temp_output = call_openrouter(prompt_clean, model="google/gemini-2.0-flash-001")

    print(temp_output)

    prompt_main = main_prompt(temp_output)
    output = call_openrouter(prompt_main, model="nousresearch/hermes-3-llama-3.1-405b")
    output_clean = output.strip().removeprefix("```json").removesuffix("```").strip()
    print(output_clean)
    return json.loads(output_clean)
