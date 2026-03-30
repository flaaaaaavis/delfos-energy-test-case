"""Ponto de entrada principal da aplicação FastAPI."""


from fastapi import FastAPI
from .routes.routes import router


app = FastAPI(title="Source Data API")

app.include_router(router)
