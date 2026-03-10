def generate_exp(data):
    exp_val = str(data.get('Expérience_Totale_Années', '')).strip()
    if not exp_val:
        return ""

    if "an" not in exp_val.lower():
        exp_val += " ans"

    if "exp" not in exp_val.lower():
        exp_val += " d'expérience"

    return exp_val