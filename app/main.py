from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
#from app.routes.routes import router
#from app.routes.projects import router
#from app.routes.users import router
from .database import init_db
from app.routes import project_router, user_router, auth
#from app.auth import get_current_user
app = FastAPI(
    title="Alex Projects",
    description="API for portfolio managment",
    version="1.0.0"
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")


app.include_router(project_router)
app.include_router(user_router)
app.include_router(auth)

@app.on_event("startup")
async def startup_event():
    init_db()
