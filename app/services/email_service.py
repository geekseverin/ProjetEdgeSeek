# from app.utils.mail_utils import send_email

# async def send_verification_email(to_email: str, token: str):
#     verification_url = f"http://localhost:8000/api/verify-email?token={token}"
#     html = f"""
#         <h3>Vérification d'email</h3>
#         <p>Merci de cliquer sur le lien suivant pour vérifier votre adresse :</p>
#         <a href="{verification_url}">Vérifier mon email</a>
#     """
#     await send_email("Vérification de votre compte", [to_email], html)


from jinja2 import Environment, FileSystemLoader
from app.utils.mail_utils import send_email
import os

templates_path = os.path.join(os.path.dirname(__file__), "..", "templates", "emails")
env = Environment(loader=FileSystemLoader(templates_path))

# async def send_verification_email(to_email: str, token: str):
#     verification_url = f"http://localhost:8000/api/verify-email?token={token}"
#     template = env.get_template("verification.html")
#     html = template.render(verification_url=verification_url)
#     await send_email("Vérification de votre compte", [to_email], html)

async def send_verification_email(to_email: str, token: str):
    verification_url = f"https://example.com/verify?token={token}"
    #verification_url = f"http://localhost:8000/api/verify-email?token={token}"
    template = env.get_template("verification.html")
    html = template.render(verification_url=verification_url)
    print(f"📨 Envoi mail de vérification à {to_email} ➜ {verification_url}")  # Debug
    #await send_email("Vérification de votre compte", [to_email], html)
    await send_email("Confirmation EdgeSeeker", [to_email], html)


async def send_password_reset_email(to_email: str, token: str):
    reset_url = f"http://localhost:8000/auth/password-reset-confirm?token={token}"
    template = env.get_template("reset_password.html")
    html = template.render(reset_url=reset_url)
    await send_email("Réinitialisation de mot de passe", [to_email], html)
