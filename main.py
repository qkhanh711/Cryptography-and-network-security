from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import FastAPI, Request, Depends, Form, status
import os
from fastapi import Depends, FastAPI, Request
from pydantic import BaseModel
from typing import Union

app = FastAPI(title="Software Engineering", description="with FastAPI and Generative models", version="1.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/AES", StaticFiles(directory="model"), name="model")
app.mount("/DES", StaticFiles(directory="model"), name="model")
app.mount("/Caesar", StaticFiles(directory="model"), name="model")
# app.mount("/RSA", StaticFiles(directory="model"), name="model")
app.mount("/Vigenere", StaticFiles(directory="model"), name="model")
app.mount("/Playfair", StaticFiles(directory="model"), name="model")
app.mount("/HILL", StaticFiles(directory="model"), name="model")
app.mount("/VERNAM", StaticFiles(directory="model"), name="model")
app.mount("/One_time_pad", StaticFiles(directory="model"), name="model")

def Crytion(model, Plaintext, Key, Crytion):
    if model == "AES":
        from AES import AES
        return AES(Plaintext, Key, Crytion)
    elif model == "DES":
        from DES import DES
        return DES(Plaintext, Key, Crytion)
    elif model == "Ceasar":
        from Caesar import Caesar
        return Caesar(Plaintext, Key, Crytion)
    # elif model == "RSA":
    #     from RSA import RSA
    #     return RSA(Plaintext, Key, Crytion)
    elif model == "Vigenere":
        from Vigenere import Vigenere
        return Vigenere(Plaintext, Key, Crytion)
    elif model == "Playfair":
        from Playfair import Playfair
        return Playfair(Plaintext, Key, Crytion)
    elif model == "HILL":
        from HILL import HILL
        return HILL(Plaintext, Key, Crytion)
    elif model == "VERNAM":
        from VERNAM import VERNAM
        return VERNAM(Plaintext, Key, Crytion)
    elif model == "One-time-pad":
        from One_time_pad import Onetimepad
        return Onetimepad(Plaintext, Key, Crytion)
    else:
        return "No model"

class CryptoGraphy(BaseModel):
    model: str
    Plaintext: str = None
    Key: str = None
    Crytion: str = None

class Cypher(BaseModel):
    cap: Union[str, None] = None

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/result", response_class=JSONResponse)
async def generate_image(request: CryptoGraphy):
    result = Crytion(
        request.model,
        request.Plaintext,
        request.Key,
        request.Crytion
    )

    result = Cypher(cap= " ".join(result))

    if result:
        return {"result": result}
    else:
        return {"message": "No result available"}
