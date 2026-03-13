from usecase.linkedin.IA.prompt.prospection.prompt_message_prospection import prompt_message_prospection
from usecase.linkedin.IA.prompt.sourcing import prompt_message_sourcing


def check_mode_and_get_instruction(origin_mode,     driver,
    job_title,
    details,
    telephone,
    full_name,
    candidatrecherche):

    previous_message = []

    if origin_mode == "linkedin":
        instruction = prompt_message_prospection(
            job_title, details, telephone, full_name, previous_message
        )
    elif origin_mode == "sourcing":
        instruction = prompt_message_sourcing(
            job_title, details, telephone, full_name, candidatrecherche, previous_message
        )

    return instruction
