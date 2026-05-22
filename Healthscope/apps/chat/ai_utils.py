from difflib import get_close_matches
from .disease_data import DISEASE_DATA


def get_disease_data(disease):
    return DISEASE_DATA.get(disease, {})


def format_disease(disease):
    data = get_disease_data(disease)

    if not data:
        return "<b>❌ Disease not found</b>"

    symptoms = "<br>".join(data.get("symptoms", []))
    remedies = "<br>".join(data.get("home_remedies", []))
    note = data.get("note", "Consult a doctor.")

    return f"""
    <b>🦠 Disease:</b> {disease} <br><br>
    <b>🤒 Symptoms:</b><br>{symptoms}<br><br>
    <b>🏠 Home Remedies:</b><br>{remedies}<br><br>
    <b>⚠️ Note:</b><br>{note}
    """


def fuzzy_match_disease(user_input):
    matches = get_close_matches(user_input.lower(), DISEASE_DATA.keys(), n=1, cutoff=0.6)
    return matches[0] if matches else None


def predict_disease(user_input):
    user_input = user_input.lower()

    best_match = None
    max_score = 0

    for disease, data in DISEASE_DATA.items():
        symptoms = data.get("symptoms", [])

        score = sum(1 for s in symptoms if s.lower() in user_input)

        if score > max_score:
            max_score = score
            best_match = disease

    return best_match


# ✅ MAIN FUNCTION (IMPORTANT)
def health_chatbot(user_input):
    disease = fuzzy_match_disease(user_input)

    if disease:
        return format_disease(disease)

    disease = predict_disease(user_input)

    if disease:
        return format_disease(disease)

    return "❌ Please describe your symptoms clearly."