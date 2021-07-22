import parametros
import os
from datetime import datetime, time
import time
import subprocess
import json
import pandas as pd

plots_analizados={}
descargas={}
plots=[]
with open("data/registro_plots.json", 'r') as json_file:
    plots_analizados = json.load(json_file)

for plot in plots_analizados:
    plots.append({"plot":plots_analizados[plot]["archivo"], "puntaje":plots_analizados[plot]["pruebas_aprobadas"],"porcentaje":"{:.2%}".format(plots_analizados[plot]["pruebas_aprobadas"]/50),"ruta":plots_analizados[plot]["ruta"] })
plots.sort(key=lambda x: x.get('puntaje'))
df = pd.DataFrame(plots)
#df.sort_values(by='puntaje', ignore_index=True)
pd.option_context('display.max_rows', None)
pd.set_option('display.max_colwidth', 100)
#    print(df.loc[df['xdesc'] != "-"])'
print(df.loc[df['puntaje'] <= 39])