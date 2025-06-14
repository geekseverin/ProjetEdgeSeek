def send_verification_email(to_email: str, token: str):
    verification_url = f"http://localhost:8000/api/verify-email?token={token}"
    # Simulation pour le dev
    print(f"🔗 Lien de vérification pour {to_email}: {verification_url}")
