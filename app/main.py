from fastapi import FastAPI
from app.router import router

app = FastAPI(title="FAQBot with OpenRouter")

app.include_router(router)
