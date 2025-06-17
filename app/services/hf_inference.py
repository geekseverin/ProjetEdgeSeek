import httpx
from app.config import settings

# async def run_omnimed_inference(symptoms: str) -> str:
#     url = settings.OMNIMED_FUNCTION_URL
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.post(url, json={"symptoms": symptoms})
#             response.raise_for_status()
#             return response.json().get("result", "Aucune réponse reçue.")
#     except Exception as e:
#         return f"Erreur d'appel à Omnimed : {str(e)}"


async def run_omnimed_inference(symptoms: str) -> str:
    # Simulation d'une réponse du moteur Omnimed
    simulated_response = (
        "🧠 Analyse IA:\n"
        f"Symptômes reçus : {symptoms}\n\n"
        "🔍 Hypothèse : Infection virale bénigne (type rhinopharyngite).\n"
        "💡 Recommandation : Repos, hydratation, paracétamol si fièvre ou douleurs.\n"
        "⚠️ Limites : consultation réelle nécessaire si aggravation sous 48h."
    )
    return simulated_response
