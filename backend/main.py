from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes.generate import router as generate_router
from routes.decks import router as decks_router

# Create all DB tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="StudyGen API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate_router, prefix="/api")
app.include_router(decks_router, prefix="/api")


@app.get("/")
def health():
    return {"status": "ok", "message": "StudyGen API is running."}
