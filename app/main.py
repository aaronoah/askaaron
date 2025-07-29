from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
import uuid
from cachetools import TTLCache
import time
from dotenv import load_dotenv
import os

load_dotenv()

session_store = TTLCache(maxsize=1000, ttl=600)  # 10 min TTL

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Allow requests from your frontend
origins = [
    os.getenv("FRONTEND_HOST"), # your frontend dev server (e.g., Vite)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    data = {"title": "FastAPI Jinja2 Example", "message": "Hello from FastAPI!"}
    return templates.TemplateResponse("index.html", {"request": request, **data})


@app.post("/prompt")
async def prompt(request: Request):
    data = await request.json()
    prompt = data["prompt"]
    session_id = str(uuid.uuid4())

    # Save prompt or response generator
    session_store[session_id] = {
        "prompt": prompt,
        "status": "in_progress"
    }

    return { "session_id": session_id }


@app.get("/conversation")
def sse(session_id: str):
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    #
    # Training in progress..
    #
    response: str = "Hello! I'm Aaron's clone cyborg, I'm excited to help with any questions you might have\nbut my master is still actively working on my languages so stay tuned!"

    def event_stream():
        for token in response.split():
            yield f"data: {token}\n\n"
            time.sleep(0.08)
        session["status"] = "done"
        yield f"event: end\ndata: bye\n\n"
    
    return StreamingResponse(event_stream(), media_type="text/event-stream")