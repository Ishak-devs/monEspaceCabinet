def prompt_message_prospection(job_title):
    return f"""
    Rédige un message d'approche LinkedIn ultra-court (2 phrases max) pour un {job_title}.
    Le but est de susciter la curiosité sans avoir l'air d'un robot.
    Pas de "Cher/Chère", sois direct et moderne.
    Il faut pas qu'on sache que c'est généré par l'ia car on prospecte
    Ne met pas d'acollade, le message sera envoyé sans être lu.
    Réponds UNIQUEMENT avec le texte du message.

    """
