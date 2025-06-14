from fastapi import FastAPI
from app.config import settings
from app.core.db import init_db
from app.routes import auth, user


init_db()
app = FastAPI(title=settings.APP_NAME)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="/users", tags=["Utilisateurs"])

@app.get("/")
def read_root():
    return {"message": f"Bienvenue sur {settings.APP_NAME}"}

