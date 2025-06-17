from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.user import User
from app.models.prompt import Prompt
from app.schemas.prompt import PromptCreate, PromptRead
from app.core.security import role_required
from app.services.hf_inference import run_omnimed_inference

router = APIRouter(prefix="/prompts", tags=["Prompts"])


# Route protégée pour les patients : soumission d'un prompt
@router.post("/submit", response_model=PromptRead)
async def submit_prompt(
    data: PromptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required("patient"))
):
    response = await run_omnimed_inference(data.symptoms)

    prompt = Prompt(
        user_id=current_user.id,
        symptoms=data.symptoms,
        ai_response=response
    )
    db.add(prompt)
    db.commit()
    db.refresh(prompt)

    return prompt


# Route protégée pour les médecins : voir tous les prompts
@router.get("/received", response_model=list[PromptRead])
def get_received_prompts(
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required("medecin"))
):
    return db.query(Prompt).all()
