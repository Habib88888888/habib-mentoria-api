from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, EmailStr
import os

app = FastAPI(title="Mentoria HABIB — Verificação de Acesso", version="1.0.0")

API_KEY = os.getenv("HABIB_API_KEY", "troque-esta-chave")
VALID_KEYS = set(k.strip() for k in os.getenv("HABIB_MENTORIA_KEYS", "HABIB-ALFA-2025").split(","))

class Req(BaseModel):
    email: EmailStr
    chave: str

@app.post("/mentoria/verificar")
def verificar_acesso(req: Req, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="unauthorized")
    autorizado = req.chave in VALID_KEYS
    plano = "Mentoria" if autorizado else "Nenhum"
    observacao = "OK" if autorizado else "Chave inválida"
    return {"autorizado": autorizado, "plano": plano, "observacao": observacao}
