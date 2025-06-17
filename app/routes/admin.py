from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserRead
from app.core.db import get_db
from app.core.security import role_required
from app.schemas.user import UserCreate, UserRead
from app.core.security import hash_password


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=list[UserRead])
def list_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required("admin"))
):
    return db.query(User).all()


@router.delete("/users/{user_id}", summary="Supprimer un utilisateur")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required("admin"))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    db.delete(user)
    db.commit()
    return {"message": f"Utilisateur {user.email} supprimé avec succès"}

@router.post("/create-admin", response_model=UserRead, summary="Créer un compte admin")
def create_admin(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    db_user = User(
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        hashed_password=hash_password(user.password),
        role="admin",
        is_active=True,
        is_verified=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
