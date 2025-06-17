from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserRead, PasswordResetRequest, PasswordResetConfirm
from app.models.user import User, Base, UserRole
from app.core.db import SessionLocal, get_db
from app.core.security import hash_password, verify_password, create_access_token, generate_email_token
from datetime import timedelta, datetime
from app.models.password_reset import PasswordResetToken
from uuid import uuid4
import smtplib  # (exemple, à remplacer par ton système mail)
from app.services.email_service import send_verification_email, send_password_reset_email
from app.utils.mail_utils import send_email


app = FastAPI()
router = APIRouter()

# Dépendance pour récupérer la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")

    hashed_pw = hash_password(user.password)
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        hashed_password=hashed_pw,
        role=user.role,
        is_active=True,
        is_verified=False  # on attend vérification
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    token = generate_email_token(db_user.email)
    # url = "http://localhost:8000/api/verify-email?token=fake-token"
    # html = f"""
    #     <h2>Test mail de vérification</h2>
    #     <p>Voici votre lien : <a href="{url}">{url}</a></p>
    # """
    # await send_email("Vérification testée", ["donaldtitembaye@gmail.com"], html)

    await send_verification_email(db_user.email, token)

    return db_user


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    access_token = create_access_token(
        data={"sub": db_user.email, "role": db_user.role.value},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/password-reset-request", summary="Demander une réinitialisation")
async def request_reset_password(payload: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    token = str(uuid4())
    reset_token = PasswordResetToken(email=payload.email, token=token)
    db.add(reset_token)
    db.commit()

    await send_password_reset_email(user.email, token)

    return {"message": "Lien de réinitialisation envoyé par e-mail"}


@router.post("/password-reset-confirm", summary="Réinitialiser le mot de passe")
def reset_password(payload: PasswordResetConfirm, db: Session = Depends(get_db)):
    # On récupère le token en base et on vérifie qu’il n’est pas expiré
    token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == payload.token,
        PasswordResetToken.expires_at > datetime.utcnow()
    ).first()

    if not token:
        # Si le token est invalide ou expiré
        raise HTTPException(status_code=400, detail="Token invalide ou expiré")

    # On récupère l'utilisateur lié au token
    user = db.query(User).filter(User.email == token.email).first()

    # On met à jour son mot de passe (après hachage)
    user.hashed_password = hash_password(payload.new_password)

    # On supprime le token car il a été utilisé
    db.delete(token)
    db.commit()

    # On retourne un message de succès
    return {"message": "Mot de passe réinitialisé avec succès"}


@router.get("/verify-email", tags=["auth"])
def verify_email(token: str, db: Session = Depends(get_db)):
    from app.core.security import verify_email_token
    email = verify_email_token(token)

    if not email:
        raise HTTPException(status_code=400, detail="Lien invalide ou expiré")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    
    if user.is_verified:
        return {"message": "Votre email est déjà vérifié."}
    
    user.is_verified = True
    db.commit()
    return {"message": "Email vérifié avec succès."}