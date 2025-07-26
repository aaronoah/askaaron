from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    data = {"title": "FastAPI Jinja2 Example", "message": "Hello from FastAPI!"}
    return templates.TemplateResponse("index.html", {"request": request, **data})
