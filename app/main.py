from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from app.routes.users import router as users_router
from app.routes.utils import router as utils_router
from app.routes.items import router as items_router
import os

app = FastAPI()

frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

app.include_router(users_router)
app.include_router(utils_router)
app.include_router(items_router)

@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")

@app.get("/health")
async def health_check():
    return {"status": "ok"}