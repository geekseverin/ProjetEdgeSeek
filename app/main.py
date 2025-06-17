from fastapi import FastAPI
from app.config import settings
from app.core.db import init_db
from app.routes import auth, user
from app.routes import prompts
from app.routes import admin

swagger_ui_init_oauth=None

init_db()
app = FastAPI(title=settings.APP_NAME)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="/users", tags=["Utilisateurs"])
app.include_router(prompts.router, prefix="/prompts", tags=["Prompts"])
app.include_router(admin.router)


@app.get("/")
def read_root():
    return {"message": f"Bienvenue sur {settings.APP_NAME}"}

