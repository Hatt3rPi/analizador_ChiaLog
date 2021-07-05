print("Iniciando análisis de log")
from time import process_time 
t1=process_time()
import re
from datetime import datetime,timedelta
from file_read_backwards import FileReadBackwards
import json
import plotly.graph_objs as go
from plotly.subplots import make_subplots
# Libraries
import matplotlib.pyplot as plt
import pandas as pd
from math import pi
import parametros
from telebot import types
import numpy as np
import os

def main():
    t_inicio_gral=process_time()
    log_harvester={}
    
    programa={'chia':'latin-1',
    'chaingreen':'latin-1',
    'flax':'latin-1',
    'spare-blockchain':'latin-1'}
    #log_file_path = fr"C:\Users\{os.getlogin()}\.chia\mainnet\log\debug.log"
    match_list = []
    regex = '^([0-9:.T-]{23}) ([a-zA-Z_.]*) ([a-zA-Z_.]*): ([A-Z]*)'
    archivos=['','.1','.2','.3','.4','.5','.6','.7']
    registro_log={}
    if os.path.isfile("formato/registro_log_formato.json")==False: open("formato/registro_log_formato.json","w").close()
    with open("formato/registro_log_formato.json", 'r') as json_file:
        registro_log = json.load(json_file)
    for moneda in programa:
        contador=1
        t_inicio1=process_time()
        info_faltante=True
        fin_bucle=False
        for archivo in archivos:
            if info_faltante==False: break
            n=0
            with FileReadBackwards(fr"C:\Users\{os.getlogin()}\.{moneda}\mainnet\log\debug.log{archivo}",encoding=programa[moneda]) as frb:
                tmoneda=process_time()
                for line in frb:
                    if fin_bucle: break
                    for match in re.finditer(regex, line, re.S):
                        if datetime.fromisoformat(line[0:19])>(datetime.now() - timedelta(minutes=60)):
                       
                            #print (match.groups())
                            nuevo=False
                            nuevo1=False
                            nuevo2=False
                            nuevo3=False
                            if not moneda in registro_log:
                                registro_log.setdefault(moneda,{'contador':1})
                                nuevo=True
                            if not match.groups()[3] in registro_log[moneda]:
                                registro_log[moneda].setdefault(match.groups()[3],{'contador':1})
                                nuevo1=True
                            if not match.groups()[1] in registro_log[moneda][match.groups()[3]]:
                                registro_log[moneda][match.groups()[3]].setdefault(match.groups()[1],{'contador':1})
                                nuevo2=True
                            if not match.groups()[2] in registro_log[moneda][match.groups()[3]][match.groups()[1]]:
                                registro_log[moneda][match.groups()[3]][match.groups()[1]].setdefault(match.groups()[2],{'contador':1})
                                nuevo3=True  
                            if nuevo3==False:
                                registro_log[moneda][match.groups()[3]][match.groups()[1]][match.groups()[2]]['contador']=1+registro_log[moneda][match.groups()[3]][match.groups()[1]][match.groups()[2]]['contador']
                            if nuevo2==False:
                                registro_log[moneda][match.groups()[3]][match.groups()[1]]['contador']=1+registro_log[moneda][match.groups()[3]][match.groups()[1]]['contador']
                            if nuevo1==False:
                                registro_log[moneda][match.groups()[3]]['contador']=1+registro_log[moneda][match.groups()[3]]['contador']
                            if nuevo==False:
                                registro_log[moneda]['contador']=1+registro_log[moneda]['contador']
                        else:
                            info_faltante=False
                            fin_bucle=True
                            break 
                t_fin1=process_time()
                print("\t",moneda,f"archivo: debug.log{archivo}",f"-> tiempo ejecución: {t_fin1-tmoneda} segundos")
        t_fin1=process_time()
        print(moneda, f"-> tiempo ejecución: {t_fin1-t_inicio1} segundos")

        log_harvester.setdefault(moneda,{'cantidad':registro_log[moneda]['INFO']['harvester'][f"{moneda.replace('-blockchain','')}.harvester.harvester"]['contador'], 'porcentaje':"{:.2%}".format(registro_log[moneda]['INFO']['harvester'][f"{moneda.replace('-blockchain','')}.harvester.harvester"]['contador']/384)})
        #print(registro_log[moneda]['INFO']['harvester'][f"{moneda.replace('-blockchain','')}.harvester.harvester"]['contador'], (registro_log[moneda]['INFO']['harvester'][f"{moneda.replace('-blockchain','')}.harvester.harvester"]['contador']/384))

    log_harvester1={}
    if os.path.isfile("data/registro_log_harvester.json")==False: open("data/registro_log_harvester.json","w").close()
    with open("data/registro_log_harvester.json", 'r') as json_file:
        log_harvester1 = json.load(json_file)
    fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_harvester1.setdefault(fecha,log_harvester)
    #print(log_harvester1)
    for fecha in log_harvester1.copy():
        #print(fecha)
        if fecha<(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"):
            log_harvester1.pop(fecha)
    with open("data/registro_log_harvester.json", 'w') as outfile:
        json.dump(log_harvester1, outfile,indent=3)
    with open("data/registro_log.json", 'w') as outfile:
        json.dump(registro_log, outfile, indent=4)
    with open("data/registro_fecha.txt", 'w') as outfile:
        json.dump(fecha, outfile)

    
    t_fin_gral=process_time()
    print(f"Tiempo Total ejecución: {t_fin_gral-t_inicio_gral} segundos")

if __name__ == "__main__":
    main()

