from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="AI PDF Agent")

app.include_router(router)


@app.get("/")
def home():
    return {"message": "AI PDF Agent is running 🚀"}