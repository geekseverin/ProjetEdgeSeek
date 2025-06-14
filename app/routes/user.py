from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserRead, UserBase
from app.core.security import get_current_user
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.user import User
from pydantic import BaseModel
from app.core.security import verify_password, hash_password

router = APIRouter()

@router.get("/me", response_model=UserRead, summary="Obtenir le profil utilisateur", tags=["Utilisateurs"])
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/update", response_model=UserRead, summary="Mettre à jour son profil", tags=["Utilisateurs"])
def update_profile(updated: UserBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user.full_name = updated.full_name
    current_user.phone = updated.phone
    db.commit()
    db.refresh(current_user)
    return current_user

class PasswordChange(BaseModel):
    old_password: str
    new_password: str


@router.put("/change-password", summary="Changer son mot de passe", tags=["Utilisateurs"])
def change_password(data: PasswordChange, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=403, detail="Mot de passe actuel incorrect")
    current_user.hashed_password = hash_password(data.new_password)
    db.commit()
    return {"message": "Mot de passe mis à jour"}
