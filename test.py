
print("Iniciando análisis de log")
from time import process_time 
t1=process_time()
t_inicio_gral=process_time()
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

def analiza_sp():
    log_historico_24hr={}
    with open("data/registro_parciales.json", 'r') as json_file:
        log_historico_24hr = json.load(json_file)


    pruebas=0
    total_parciales=0
    parciales_validos=0
    parciales_invalidos=0
    signage_point=0
    tiempo=[]
    reset=False
    alias=""
    regex = '^([0-9:.T-]{23}) ([a-zA-Z_.]*) ([a-zA-Z_ .]*): ([A-Z]*)'
    archivos=['','.1','.2','.3','.4','.5','.6','.7']
    reg_parcial_invalido='^([0-9:.T-]{23}) ([a-zA-Z_.]*) ([a-zA-Z _.]*): ERROR[\s]*Error in pooling'
    reg_sp='^([0-9:.T-]{23}) ([a-zA-Z_.]*) ([a-zA-Z_.]*): INFO[\s]*([0-9]*) plots were eligible for farming ([0-9a-z]*)... Found ([0-9]*) proofs. Time: ([0-9.]*) s. Total ([0-9]*)'
    
    fin_bucle=False
    for archivo in archivos:
        with FileReadBackwards(fr"C:\Users\{os.getlogin()}\.chia\mainnet\log\debug.log{archivo}",encoding='latin-1') as frb:
            tmoneda=process_time()
            for line in frb:
                if fin_bucle: break
                for validos in re.finditer(regex, line, re.S):
                    if datetime.fromisoformat(line[0:19])>(datetime.now() - timedelta(minutes=20)):
                        for match in re.finditer(reg_sp, line, re.S):
                            if alias=="":
                                alias=match.groups()[4]
                                log_historico_24hr.setdefault(alias,{
                                                        "timestamp": "",
                                                        "alias":alias,
                                                        "signage_points":0,
                                                        "pruebas":0,
                                                        "total_parciales" :0,
                                                        "parciales_validos":0,
                                                        "parciales_invalidos":0,
                                                        "dificultad":0,
                                                        "puntaje":0,
                                                        "tiempos":[],
                                                        "t_min":0,
                                                        "t_max":0,
                                                        "t_prom":0 
                                                        })
                            elif alias!="" and alias!=match.groups()[4]:
                                alias=match.groups()[4]
                                reset=True
                                log_historico_24hr.setdefault(alias,{
                                                        "timestamp": "",
                                                        "alias":alias,
                                                        "signage_points":0,
                                                        "pruebas":0,
                                                        "total_parciales" :0,
                                                        "parciales_validos":0,
                                                        "parciales_invalidos":0,
                                                        "dificultad":0,
                                                        "puntaje":0,
                                                        "tiempos":[],
                                                        "t_min":0,
                                                        "t_max":0,
                                                        "t_prom":0 
                                                        })
                            else:
                                reset=False

                            if reset==False:
                                log_historico_24hr[alias]["signage_points"]+=1
                                log_historico_24hr[alias]["pruebas"]+=int(match.groups()[3])
                                log_historico_24hr[alias]["total_parciales"]+=int(match.groups()[5])
                                log_historico_24hr[alias]["tiempos"].append(float(match.groups()[6]))
                                signage_point+=1 #obsoleto
                                #print(match.groups()[4], f"{signage_point}/64","Pruebas",match.groups()[3],"Parciales",match.groups()[5])
                                pruebas+=int(match.groups()[3]) #obsoleto
                                total_parciales+=int(match.groups()[5]) #obsoleto
                                tiempo.append(float(match.groups()[6])) #obsoleto
                            else:
                                print(alias, f"Signage Point: {signage_point}/64, Pruebas: {pruebas}, Total parciales: {total_parciales}, Parciales invalidos: {parciales_invalidos}, t_min:{round(min(tiempo),3)}s, t_max:{round(max(tiempo),3)}s, t_prom:{round(sum(tiempo) / len(tiempo),3)}s")
                                signage_point=1
                                tiempo=[]
                                parciales_invalidos=0
                                #print(match.groups()[4], f"{signage_point}/64","Pruebas",match.groups()[3],"Parciales",match.groups()[5])
                                pruebas=int(match.groups()[3])
                                total_parciales=int(match.groups()[5])
                                tiempo.append(float(match.groups()[6]))
                        for match in re.finditer(reg_parcial_invalido, line, re.S):
                            parciales_invalidos+=1
                    else:
                        print("break")
                        fin_bucle=True
                        break
    print(log_historico_24hr)
    
def main():

    log_harvester={}
    
    programa={'chia':'latin-1'}
    #log_file_path = fr"C:\Users\{os.getlogin()}\.chia\mainnet\log\debug.log"
    match_list = []
    sub_plot=""
    registrar_sp=False
    archivos=['','.1','.2','.3','.4','.5','.6','.7']
    registro_log={}
    if os.path.isfile("formato/registro_log_formato.json")==False: open("formato/registro_log_formato.json","w").close()
    with open("formato/registro_log_formato.json", 'r') as json_file:
        registro_log = json.load(json_file)
    for moneda in programa:
        if moneda in ('chia','chaingreen','flax','spare-blockchain'):
            regex = '^([0-9:.T-]{23}) ([a-zA-Z_.]*) ([a-zA-Z_ .]*): ([A-Z]*)'
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
                            reg_plot='^([0-9:.T-]{23}) ([a-zA-Z_.]*) ([a-zA-Z_.]*): INFO[\s]*Finished sub slot, SP 64/64, ([0-9a-z]*), number of sub-slots:'
                            reg_sp='^([0-9:.T-]{23}) ([a-zA-Z_.]*) ([a-zA-Z_.]*): INFO[\s]*([0-9]*) plots were eligible for farming ([0-9a-z]*)... Found ([0-9]*) proofs. Time: ([0-9.]*) s. Total ([0-9]*)'
                            reg_parcial_invalido='^([0-9:.T-]{23}) ([a-zA-Z_.]*) ([a-zA-Z _.]*): ERROR[\s]*Error in pooling'
                            if datetime.fromisoformat(line[0:19])>(datetime.now() - timedelta(minutes=10)):
                                for match2 in re.finditer(reg_sp, line, re.S):
                                    if sub_plot=="":
                                        sub_plot=match2.groups()[4]
                                    elif sub_plot!=match2.groups()[4] and registrar_sp==False:
                                        print("analizar sp",sub_plot)
                                        registrar_sp=True
                            else:
                                info_faltante=False
                                fin_bucle=True
                                break 
                    print("fin")
                    

                 

if __name__ == "__main__":
    analiza_sp()
