# import openai
from openai import AsyncOpenAI
import os
async def faire_recherche_openrouter(nom_entreprise):
    if not nom_entreprise or len(nom_entreprise) < 2:
        return ""

    client = AsyncOpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ.get("OPENROUTERAPI"))

    try:
        print('lancement de recherche en ligne...')
        completion = await client.chat.completions.create(
            model="perplexity/llama-3.1-sonar-small-128k-online",
            messages=[
                {
                    "role": "user",
                    "content": f"En une seule phrase de moins de 20 mots, explique les secteurs d'activités de l'entreprise {nom_entreprise}"
                }
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception:
        return ""