from dotenv import load_dotenv
load_dotenv('.env')

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from database import database
from sql import GET_ALL_IMAGES, SEARCH_UPLOADED_IMAGE
from logic.image_process import process_image, searching_image
from threading import Thread
import shutil
from ai.gemini import image_to_base64

app = FastAPI()

# Create directories
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount static folders
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/static", StaticFiles(directory="ui/static"), name="static")

# Template setup
templates = Jinja2Templates(directory="ui/templates")

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/search", response_class=HTMLResponse)
async def search_image(request: Request, file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    if len(database.query(SEARCH_UPLOADED_IMAGE.format(image_path=file_path))) < 1:
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process image
        image_to_base64(file_path).save(file_path)

    related_images = searching_image(file_path, file)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "uploaded_filename": file_path,
        "first_image": related_images
    })

@app.post("/upload", response_class=HTMLResponse)
async def upload_image(request: Request, file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    if len(database.query(SEARCH_UPLOADED_IMAGE.format(image_path=file_path))) < 1:
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process image
        image_to_base64(file_path).save(file_path)

    task = Thread(target=process_image, args=(file_path, file))
    task.start()
    return RedirectResponse(url="/library", status_code=303)

@app.get("/library", response_class=HTMLResponse)
async def library(request: Request):
    all_images = database.query(GET_ALL_IMAGES)
    return templates.TemplateResponse("library.html", {
        "request": request,
        "images": all_images
    })
