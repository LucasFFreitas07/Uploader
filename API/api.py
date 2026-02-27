from fastapi import FastAPI, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from aiofile import async_open
from datetime import datetime
from pathlib import Path

from starlette.templating import _TemplateResponse

today = datetime.now().strftime("%d-%m")
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
media = Path("/app/media")
if not media.exists():
    media.mkdir(exist_ok=True, parents=True)

@app.get("/")
async def home(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload(request: Request) -> _TemplateResponse:
    form_data = await request.form()

    file: UploadFile = form_data.get("arquivo")
    file.filename = f"{today}_{file.filename}"
    context = {"request": request}

    async with async_open(media/file.filename, "wb") as f:
        content = await file.read()
        await f.write(content)

    return templates.TemplateResponse("index.html", context)


@app.get("/hello/{name}")
async def hello(request: Request, name: str) -> None:
    return f"Hello {name}!"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="api:app", host="0.0.0.0", port=8000, log_level="info", reload=True)