from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import threading
import time

app = FastAPI(title="API Farmacias FastAPI", version="1.0")

# ======================
# URL del Apps Script desplegado (GET y POST)
# ======================
GetFarmacias = "https://script.google.com/macros/s/AKfycbx18-nVSTkwaBXShlG_nJtfXSn0Y-01EA18Q_OTVzlEm4pl9oFZql2yJIUrmIBOT0Jg6g/exec"

# ======================
# ENDPOINT GET: obtiene farmacias desde Google Sheets
# ======================
@app.get("/farmacias")
def obtener_farmacias():
    try:
        response = requests.get(GetFarmacias)
        response.raise_for_status()
        return JSONResponse(content=response.json())
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# ======================
# ENDPOINT POST: agrega una fila a Google Sheets vía Apps Script


# ======================
# ENDPOINT PING para mantener vivo Render
# ======================
@app.get("/ping")
def ping():
    return {"status": "alive"}

# ======================
# HILO DE AUTO-PING
# ======================
def keep_alive():
    while True:
        try:
            requests.get("https://roc-point.onrender.com/ping")  # <- Cambia por tu URL real
            print("✅ Ping enviado correctamente")
        except Exception as e:
            print(f"⚠️ Error enviando ping: {e}")
        time.sleep(180)

threading.Thread(target=keep_alive, daemon=True).start()
