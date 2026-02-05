# import groq
from data.call_groq import call_groq


def prompt_check_ia_profile(offre, profile_main_content):

    prompt = f"""
        Analyse ce profil LinkedIn : {profile_main_content}
        Est-ce qu'il correspond à cette {offre} ?
        Réponds uniquement par 'OUI' ou 'NON'.
        et si c'est oui donne un résumé très court qui expliquerais pourquoi il est intéréssant avec les infos pour le contacter.
        Par exemple : "Tu devrais checker ce profil, il a une expérience de 5 ans dans le domaine ça colle avec l'offre, j'ai trouvé son numéro sur sa page : XXXXXXXXXX."
        """

    response_ia = call_groq(prompt) or ""
    response_clear = response_ia.strip().lower()
    print(f"Reponse IA: {response_clear}")
    print(
        f"✅ [IA CHECK] Verdict: {'Accepté' if 'OUI' in response_clear else 'Refusé'}"
    )

    return "OUI" in response_clear
