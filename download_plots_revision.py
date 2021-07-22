import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unicodedata import normalize
import json
import requests
from datetime import datetime, time
import wget
import parametros
import os
import time
import subprocess


plots={}
descargas={}
k=1
urllog = 'http://54.233.191.133/c1/chia-plotter-bb232c4a-e7e9-11eb-8f36-035da92160af.log'
my_stream_file = requests.get(urllog, stream=True)
path = 'C:/Users/gesti/.chia/mainnet/plotter/chia-plotter-bb232c4a-e7e9-11eb-8f36-035da92160af.log'
print(f"descargando archivo: {urllog}")
wget.download(urllog, path)
urllog = 'http://54.233.191.133/c1/chia-plotter-608a2404-e925-11eb-9cb7-27cdbdde0205.log'
my_stream_file = requests.get(urllog, stream=True)
path = 'C:/Users/gesti/.chia/mainnet/plotter/chia-plotter-608a2404-e925-11eb-9cb7-27cdbdde0205.log'
print(f"descargando archivo: {urllog}")
wget.download(urllog, path)


cmd = f"\"C:\\Program Files (x86)\\ChiaPlotStatus\\ChiaPlotStatus\\ChiaPlotStatusCli.exe\" -o {parametros.ruta_actual}\data\chia_plot_status.json -f json"
#print(cmd)
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=0)
time.sleep(30) 
with open("data/chia_plot_status.json", 'r') as json_file:
        plots = json.load(json_file)
listado_logs=["chia-plotter-bb232c4a-e7e9-11eb-8f36-035da92160af (1).log","chia-plotter-608a2404-e925-11eb-9cb7-27cdbdde0205 (1).log"]
for ruta in parametros.path:
    for archivo in os.listdir(ruta):
        if archivo.endswith(".plot"):
            descargas.setdefault(archivo, {
            "fecha_creacion": datetime.fromtimestamp(os.path.getctime(f"{ruta}\{archivo}")).strftime('%d/%m/%Y %H:%M:%S'),
            "ruta":ruta
        })
url = 'http://54.233.191.133/c1/'
table_MN = pd.read_html(url)
#print(table_MN)
num=1
numf=1
en_url=[]
for n in table_MN:
    for i in n["Name"].to_list():
        if str(i).find('.plot')>0: 
          en_url.append(str(i))
          '''
          if i in descargas: 
              descargado=True
              print(numf,i[0:25],"Archivo descargado en:",descargas[i]["ruta"])
              numf+=1
          else: 
              descargado=False
              print(i[0:25],"Descarga Pendiente",num)
              num+=1
                '''
descarga=""
ruta="-"
r=0
d=0
x=0
id1="-"
id2="-"
id3="-"
consolidado=[]
for plot in plots:
  if plot["LogFile"] in listado_logs:
    if plot["PlotName"]+".plot" in descargas: 
      ruta= descargas[plot["PlotName"]+".plot"]["ruta"]
      r+=1
      id1=r
    if plot["PlotName"]+".plot" in en_url: 
      descarga= "En url"
      d+=1
      id2=d
    #print(k, plot["PlotName"], r,ruta, d,descarga)
    if id1!="-" and id2!="-":
      x+=1
      id3=x
    consolidado.append({"plot": plot["PlotName"]+".plot", "desc":id1,"ruta":ruta,"link":id2,"xdesc":id3})
    
    descarga=""
    ruta="-"
    id1="-"
    id2="-"
    id3="-"
    k+=1
df = pd.DataFrame(consolidado)
with pd.option_context('display.max_rows', None):  # more options can be specified also
#    print(df.loc[df['xdesc'] != "-"])'
  print(df)
