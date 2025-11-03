from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
import threading
import time

app = FastAPI(title="API Farmacias FastAPI", version="1.0")


GetFarmacias = "https://script.google.com/macros/s/AKfycbx18-nVSTkwaBXShlG_nJtfXSn0Y-01EA18Q_OTVzlEm4pl9oFZql2yJIUrmIBOT0Jg6g/exec"
GetUsuraios = "https://script.google.com/macros/s/AKfycbzJWf6o4y-_g4rW9_Ivl0fTV5-mV5OwjcBeDoYmo2liH3UnZcRT7q-1V1Oa-eAEz_ShXw/exec"
PostFarmacia = "https://script.google.com/macros/s/AKfycbyKVyr8qaErTi3v4KmAj1TKDZ0FysUeySlkHGoTgVYD6i5Ez_gd181CwCys__S4pdA7LA/exec"

class FarmaciaData(BaseModel):
    farma_id: str
    title: str
    client_id: str

@app.get("/farmacias")
def obtener_farmacias():
    try:
        response = requests.get(GetFarmacias)
        response.raise_for_status()
        return JSONResponse(content=response.json())
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/usuarios")
def obtener_Usuarios():
    try:
        response = requests.get(GetUsuraios)
        response.raise_for_status()
        return JSONResponse(content=response.json())
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/farmacia")
def crear_farmacia(data: FarmaciaData):
    try:
        payload = {
            "farma_id": data.farma_id,
            "title": data.title,
            "client_id": data.client_id
        }
        response = requests.post(PostFarmacia, json=payload)
        response.raise_for_status()
        return JSONResponse(content=response.json())
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/ping")
def ping():
    return {"status": "alive"}

def keep_alive():
    while True:
        try:
            requests.get("https://roc-point.onrender.com/ping")  # <- Cambia por tu URL real
            print("✅ Ping enviado correctamente")
        except Exception as e:
            print(f"⚠️ Error enviando ping: {e}")
        time.sleep(180)

threading.Thread(target=keep_alive, daemon=True).start()
