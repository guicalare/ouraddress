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

templates = Jinja2Templates(directory="templates")

app = FastAPI()

@app.post("/files/")
async def create_files(files: list[bytes] = File(), basura: str = "", calles: str = Form(), codigo_municipal: str = Form(), separador: str = Form()):
   
   if file_exists("./input ddbb/datos.csv"):
      remove_file("./input ddbb/datos.csv")
   if file_exists("./output ddbb/ouradress.csv"):
      remove_file("./output ddbb/ouradress.csv")

   '''index_calles = files[0].decode('latin-1').split("\n").split(separador).index(calles)
   index_municipios = files[0].decode('latin-1').split("\n").split(separador).index(codigo_municipal)

   with open("./input ddbb/datos.csv", "w", encoding='latin-1') as f:
      for line in files[0].decode('latin-1').split("\n"):

         temp_line = line.strip().split(separador)

         aux_value = temp_line[0]
         temp_line[0] = temp_line[index_municipios]
         temp_line[index_municipios] = aux_value

         aux_value = temp_line[1]
         temp_line[1] = temp_line[index_calles]
         temp_line[index_calles] = aux_value

         f.write("#".join(temp_line)+"\n")'''

   Ouraddress().file_search_fuzzy_multiprocessing_init()

   return FileResponse("./output ddbb/ouradress.csv")

@app.get("/")
async def main(request: Request):
   if file_exists("./input ddbb/datos.csv"):
      remove_file("./input ddbb/datos.csv")
   if file_exists("./output ddbb/ouradress.csv"):
      remove_file("./output ddbb/ouradress.csv")
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
