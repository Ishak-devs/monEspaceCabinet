def post_prompt(post, full_name, telephone):
    return f"""
    Nous sommes un cabinet de conseil et nous postons sur LinkedIn, aidez-nous à créer un message court et prêt à être posté sur LinkedIn.
    Prends en compte les instructions suivantes : {post}
    ou autres caractères spéciaux.
    Indique mes coordonnées : {full_name} - {telephone}
""".strip()
