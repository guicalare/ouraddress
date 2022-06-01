from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from os import getenv
from os.path import exists as file_exists
from os import remove as remove_file
import uvicorn
from json import load
from ouraddress import *
from utils import *

templates = Jinja2Templates(directory="templates")

app = FastAPI()

@app.post("/files/")
async def create_files(files: list[bytes] = File(), basura: str = "", calles: str = Form(), codigo_municipal: str = Form(), separador: str = Form()):

   clean_dir("./input ddbb")
   clean_dir("./output ddbb")
   clean_dir("./temp ddbb")

   with open("./input ddbb/datos.csv", "w", encoding='latin-1') as f:
      f.write(files[0].decode('latin-1'))

   ouraddress = Ouraddress()
   ouraddress.prepare_input_data(calles, codigo_municipal, separador)
   ouraddress.file_search_fuzzy_multiprocessing_init()

   return FileResponse("./output ddbb/ouradress.csv")

@app.get("/")
async def main(request: Request):

   clean_dir("./input ddbb")
   clean_dir("./output ddbb")
   clean_dir("./temp ddbb")
   
   return templates.TemplateResponse("upload.html",{"request":request})

if __name__ == "__main__":

   with open("config.json", "r", encoding='latin-1') as f:
      config_parameters = load(f)

   if not file_exists(config_parameters["input folder"]):
      makedirs(config_parameters["input folder"])
   if not file_exists(config_parameters["output folder"]):
      makedirs(config_parameters["output folder"])
   if not file_exists(config_parameters["temp folder"]):
      makedirs(config_parameters["temp folder"])

   uvicorn.run(app, host="0.0.0.0", port=int(getenv('APP_PORT')))