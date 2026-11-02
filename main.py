from fastapi import FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import subprocess
import uvicorn

app = FastAPI(title="Valheim Server Manager API")
#your token here |
#              \ |/
#               \/
API_TOKEN = "your_super_secret_password"
SERVER_FOLDER = r"C:\ValheimServer"
START_BAT_FILE = r"C:\ValheimServer\start_headless_server.bat"
PROCESS_NAME = "valheim_server.exe"


def is_server_running() -> bool:

    output = subprocess.check_output("tasklist", shell=True).decode("utf-8", errors="ignore")
    return PROCESS_NAME.lower() in output.lower()


def verify_token(authorization: str):
    if authorization != API_TOKEN:
        raise HTTPException(status_code=403, detail="Ramze API eshtebah ast!")


@app.get("/api/status")
def get_status():
    running = is_server_running()
    return {"online": running, "status": "Online" if running else "Offline"}


@app.post("/api/start")
def start_server(authorization: str = Header(None)):
    verify_token(authorization)
    
    if is_server_running():
        return {"message": "Server az ghabl roshan ast!"}
    
    try:
        subprocess.Popen(
            f'start "Valheim Server" "{START_BAT_FILE}"',
            cwd=SERVER_FOLDER,
            shell=True
        )
        return {"message": "Server ba movafaghiyat roshan shod."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/stop")
def stop_server(authorization: str = Header(None)):
    verify_token(authorization)
    
    if not is_server_running():
        return {"message": "Server dar hale hazer khamoosh ast!"}
    
    try:
        # Bastane barname dar Windows ba dastoore taskkill
        subprocess.run(f"taskkill /IM {PROCESS_NAME} /F", shell=True)
        return {"message": "Server ba movafaghiyat khamoosh shod."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def serve_home():
    return FileResponse("static/index.html")


app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)