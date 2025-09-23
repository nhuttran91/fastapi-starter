import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

APP_ENV = os.getenv("APP_ENV", "local")

app = FastAPI(title="FastAPI Starter", version="1.0.0")
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "env": APP_ENV})

@app.get("/healthz", response_class=JSONResponse)
def healthz():
    return {"status": "ok", "env": APP_ENV}