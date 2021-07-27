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
import matplotlib.dates as mdates
import pandas as pd
from math import pi
import parametros
from telebot import types
import numpy as np
import os

t2=process_time()
print(f"Importar Librerias: {t2-t1} segundos")
def actualiza_balance(moneda, monto):
    wallets={}
    if os.path.isfile("data/wallets.json")==False: open("data/wallets.json","w").close()
    with open("data/wallets.json", 'r') as json_file:
        wallets = json.load(json_file)
    if '{:.12f}'.format(float(int(monto)/1000000000000))!=wallets[moneda]['balance']:
        wallets[moneda]['balance']='{:.12f}'.format(float(int(monto)/1000000000000))
        wallets[moneda]['balance_total']='{:.12f}'.format(float(wallets[moneda]['balance'])+float(wallets[moneda]['balance_pendiente']))
        #print(moneda,'{:.12f}'.format(float(int(monto)/1000000000000)))
        #notificacion cambio balance
        parametros.bot.send_message(parametros.chat_id, f"El balance de tu wallet de {moneda} cambió a {'{:.12f}'.format(float(int(monto)/1000000000000))}")
        with open("data/wallets.json", 'w') as outfile:
            json.dump(wallets, outfile,indent=3)
def historia_harvester():
    log={}
    plt.figure(figsize=(10,6))
    if os.path.isfile("data/registro_log_harvester.json")==False: open("data/registro_log_harvester.json","w").close()
    with open("data/registro_log_harvester.json", 'r') as json_file:
        log = json.load(json_file)
    #print(log)
    data=[]
    for key, fila in log.items():
        if 'signum' in fila:
            hrvst_sgna=float(fila['signum']['porcentaje'].strip('%'))/100
            hrvst_bth=float(fila['bitcoinhd']['porcentaje'].strip('%'))/100
        else:
            hrvst_sgna=0
            hrvst_bth=0
        data.append([key, float(fila['chia']['porcentaje'].strip('%'))/100,float(fila['chaingreen']['porcentaje'].strip('%'))/100,float(fila['flax']['porcentaje'].strip('%'))/100,float(fila['spare-blockchain']['porcentaje'].strip('%'))/100,hrvst_sgna,hrvst_bth])

    df = pd.DataFrame(data,columns=['hora','chia','chaingreen','flax','spare-blockchain','signum','bitcoinhd'])
    df['hora']= pd.to_datetime(df['hora'])
    plt.plot('hora', 'chia', data=df,   color='green', label='chia')
    plt.plot('hora', 'chaingreen', data=df,   color='orange', label='chaingreen')
    plt.plot('hora', 'flax', data=df,   color='grey', label='flax')
    plt.plot('hora', 'spare-blockchain', data=df,   color='blue', label='spare')
    plt.plot('hora', 'signum', data=df,   color='red', label='signum')
    plt.plot('hora', 'bitcoinhd', data=df,   color='brown', label='bitcoinhd')
    plt.ylim(0,1.3)
    plt.xlim(df['hora'].min(),df['hora'].max())
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.HourLocator(interval = 3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    #plt.grid(axis='x', color='0.95')
    #plt.xticks(np.arange(0, len(df['hora']), 30))


    plt.legend(title='Moneda:')
    plt.title(f'Salud del Harvester: Porcentaje de cumplimiento de Signage Point \n({datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')
    #plt.plot()
    plt.savefig('img/registro_log_harvester_24h.png')
    mensajes={}
    if os.path.isfile("data/telegram_mensajes.json"):
        with open("data/telegram_mensajes.json", 'r') as json_file:
            mensajes = json.load(json_file)
            if "registro_log_harvester_24h" in mensajes:
                parametros.bot.edit_message_media(media=types.InputMediaPhoto(open('img/logo.png', 'rb')),message_id=mensajes["registro_log_harvester_24h"], chat_id=parametros.chat_id)
                parametros.bot.edit_message_media(media=types.InputMediaPhoto(open('img/registro_log_harvester_24h.png', 'rb')),message_id=mensajes["registro_log_harvester_24h"], chat_id=parametros.chat_id)
            else:
                id1=parametros.bot.send_photo(parametros.chat_id, photo=open('img/registro_log_harvester_24h.png', 'rb'))
                
                mensajes.setdefault("registro_log_harvester_24h",id1.message_id)
                with open("data/telegram_mensajes.json", 'w') as outfile:
                    json.dump(mensajes, outfile,indent=3)
    else:
        id1=parametros.bot.send_photo(parametros.chat_id, photo=open('img/registro_log_harvester_24h.png', 'rb'))
        mensajes.setdefault("registro_log_harvester_24h",id1.message_id)
        with open("data/telegram_mensajes.json", 'w') as outfile:
            json.dump(mensajes, outfile,indent=3)
    #plt.show()

def estado_harvester():
    log_harvester={}
    fecha=''
    with open("data/registro_fecha.txt", 'r') as json_file:
        fecha = json.load(json_file)
    if os.path.isfile("data/registro_log_harvester.json")==False: open("data/registro_log_harvester.json","w").close()
    with open("data/registro_log_harvester.json", 'r') as json_file:
        log_harvester = json.load(json_file)
        #print(log_harvester)
        valor=[log_harvester[fecha]['chia']['cantidad'], log_harvester[fecha]['chaingreen']['cantidad'], log_harvester[fecha]['flax']['cantidad'], log_harvester[fecha]['spare-blockchain']['cantidad'], log_harvester[fecha]['signum']['cantidad'], log_harvester[fecha]['bitcoinhd']['cantidad']]
    #print(valor)
    color=[]
    n=0
    for  i in valor:
        if n in [0,1,2,3]:
            if i<=45:
                color.insert(n,'red')
            elif i>=57:
                color.insert(n,'green')
            else:
                color.insert(n,'yellow')
        elif n==4:
            if i<=20:
                color.insert(n,'red')
            else:
                color.insert(n,'green')
        elif n==5:
            if i<=30:
                color.insert(n,'red')
            else:
                color.insert(n,'green')              
        n=n+1

    trace1 = go.Indicator(mode="gauge+number",
            value=log_harvester[fecha]['chia']['cantidad'],
            delta = {'reference': 64}, 
            gauge = {'axis': {'range': [None, 70]},
                    'steps' :[
                                {'range': [0, 45], 'color': "lightgray"},
                                {'range': [45, 57], 'color': "gray"}
                            ], 
                    'bar': {'color': color[0]},
                    'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 64}}, 
            domain={'row' : 1, 'column' : 1}, title={'text': "Chia"})
    trace2 = go.Indicator(mode="gauge+number",    
            value=log_harvester[fecha]['chaingreen']['cantidad'],
            delta = {'reference': 64}, 
            gauge = {'axis': {'range': [None, 70]}, 
                    'steps' :[
                                {'range': [0, 45], 'color': "lightgray"},
                                {'range': [45, 57], 'color': "gray"}
                            ], 
                    'bar': {'color': color[1]},
                    'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 64}},    
            domain={'row' : 1, 'column' : 2}, title={'text': "Chaingreen"})
    trace3 = go.Indicator(mode="gauge+number",    
            value=log_harvester[fecha]['flax']['cantidad'],
            delta = {'reference': 64}, 
            gauge = {'axis':{'range': [None, 70]},
                    'steps' :[
                                {'range': [0, 45], 'color': "lightgray"},
                                {'range': [45, 57], 'color': "gray"}
                            ],  
                    'bar': {'color': color[2]},
                    'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 64}},    
            domain={'row' : 2, 'column' : 1}, title={'text': "Flax"})
    trace4 = go.Indicator(mode="gauge+number",    
            value=log_harvester[fecha]['spare-blockchain']['cantidad'],
            delta = {'reference': 64},  
            gauge = {'axis':{'range': [None, 70]}, 
                    'steps' :[
                                {'range': [0, 45], 'color': "lightgray"},
                                {'range': [45, 57], 'color': "gray"}
                            ], 
                    'bar': {'color': color[3]},
                    'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 64}},    
            domain={'row' : 2, 'column' : 2}, title={'text': "Spare"})
    trace5 = go.Indicator(mode="gauge+number",    
            value=log_harvester[fecha]['signum']['cantidad'],
            delta = {'reference': 30},  
            gauge = {'axis':{'range': [None, 35]}, 
                    'steps' :[
                                {'range': [0, 20], 'color': "lightgray"}
                            ], 
                    'bar': {'color': color[4]},
                    'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 30}},    
            domain={'row' : 1, 'column' : 3}, title={'text': "Signum"})
    trace6 = go.Indicator(mode="gauge+number",    
            value=log_harvester[fecha]['bitcoinhd']['cantidad'],
            delta = {'reference': 40},  
            gauge = {'axis':{'range': [None, 45]}, 
                    'steps' :[
                                {'range': [0, 30], 'color': "lightgray"}
                            ], 
                    'bar': {'color': color[5]},
                    'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 40}},    
            domain={'row' : 2, 'column' :3}, title={'text': "BitcoinHD"})

    fig = make_subplots(
        rows=2,
        cols=3,
        specs=[[{'type' : 'indicator'}, {'type' : 'indicator'}, {'type' : 'indicator'}],[{'type' : 'indicator'}, {'type' : 'indicator'}, {'type' : 'indicator'}]],
        )
        
    fig.update_layout(title_text=f'Cantidad Signage point de últimos 10min ({datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')
    #,         scene=dict(        annotations=[        dict(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))])
    fig.append_trace(trace1, row=1, col=1)
    fig.append_trace(trace2, row=1, col=2)
    fig.append_trace(trace3, row=2, col=1)
    fig.append_trace(trace4, row=2, col=2)
    fig.append_trace(trace5, row=1, col=3)
    fig.append_trace(trace6, row=2, col=3)
    #fig.show()

    fig.write_image("img/estado_harvester.png")
    mensajes={}
    
    if os.path.isfile("data/telegram_mensajes.json"):
        with open("data/telegram_mensajes.json", 'r') as json_file:
            mensajes = json.load(json_file)
            if "estado_harvester" in mensajes and "analisis_log" in mensajes:
                parametros.bot.edit_message_media(media=types.InputMediaPhoto(open('img/logo.png', 'rb')),message_id=mensajes["estado_harvester"], chat_id=parametros.chat_id)
                parametros.bot.edit_message_media(media=types.InputMediaPhoto(open('img/estado_harvester.png', 'rb')),message_id=mensajes["estado_harvester"], chat_id=parametros.chat_id)
                parametros.bot.edit_message_media(media=types.InputMediaPhoto(open('img/logo.png', 'rb')),message_id=mensajes["analisis_log"], chat_id=parametros.chat_id)
                parametros.bot.edit_message_media(media=types.InputMediaPhoto(open('img/analisis_log.png', 'rb')),message_id=mensajes["analisis_log"], chat_id=parametros.chat_id)
            else:
                id1=parametros.bot.send_photo(parametros.chat_id, photo=open('img/estado_harvester.png', 'rb'))
                id2=parametros.bot.send_photo(parametros.chat_id, photo=open('img/analisis_log.png', 'rb'))
                mensajes.setdefault("estado_harvester",id1.message_id)
                mensajes.setdefault("analisis_log",id2.message_id)
                with open("data/telegram_mensajes.json", 'w') as outfile:
                    json.dump(mensajes, outfile,indent=3)
    else:
        id1=parametros.bot.send_photo(parametros.chat_id, photo=open('img/estado_harvester.png', 'rb'))
        id2=parametros.bot.send_photo(parametros.chat_id, photo=open('img/analisis_log.png', 'rb'))
        mensajes.setdefault("estado_harvester",id1.message_id)
        mensajes.setdefault("analisis_log",id2.message_id)
        with open("data/telegram_mensajes.json", 'w') as outfile:
            json.dump(mensajes, outfile,indent=3)

def grafico_log():
    log={}
    if os.path.isfile("data/registro_log.json")==False: open("data/registro_log.json","w").close()
    with open("data/registro_log.json", 'r') as json_file:
        log = json.load(json_file)
    #print(log['chia']['INFO']['harvester']['chia.harvester.harvester']['contador'])
    # Set data
    df = pd.DataFrame({
    'group': ['A','B','C','D'],
    'harvester.harvester': [log['chia']['INFO']['harvester']['chia.harvester.harvester']['contador'], log['chaingreen']['INFO']['harvester']['chaingreen.harvester.harvester']['contador'], log['flax']['INFO']['harvester']['flax.harvester.harvester']['contador'], log['spare-blockchain']['INFO']['harvester']['spare.harvester.harvester']['contador']],
    'plotting.plot_tools': [log['chia']['INFO']['harvester']['chia.plotting.plot_tools']['contador'], log['chaingreen']['INFO']['harvester']['chaingreen.plotting.plot_tools']['contador'], log['flax']['INFO']['harvester']['flax.plotting.plot_tools']['contador'], log['spare-blockchain']['INFO']['harvester']['spare.plotting.plot_tools']['contador']],
    #'full_node.full_node': [log['chia']['INFO']['full_node']['chia.full_node.full_node']['contador'], log['chaingreen']['INFO']['full_node']['chaingreen.full_node.full_node']['contador'], log['flax']['INFO']['full_node']['flax.full_node.full_node']['contador'], log['spare-blockchain']['INFO']['full_node']['spare.full_node.full_node']['contador']],
    #'full_node.mempool_manager': [log['chia']['INFO']['full_node']['chia.full_node.mempool_manager']['contador'], log['chaingreen']['INFO']['full_node']['chaingreen.full_node.mempool_manager']['contador'], log['flax']['INFO']['full_node']['flax.full_node.mempool_manager']['contador'], log['spare-blockchain']['INFO']['full_node']['spare.full_node.mempool_manager']['contador']],
    'full_node.full_node_store': [log['chia']['INFO']['full_node']['chia.full_node.full_node_store']['contador'], log['chaingreen']['INFO']['full_node']['chaingreen.full_node.full_node_store']['contador'], log['flax']['INFO']['full_node']['flax.full_node.full_node_store']['contador'], log['spare-blockchain']['INFO']['full_node']['spare.full_node.full_node_store']['contador']],
    'wallet.wallet_blockchain': [log['chia']['INFO']['wallet']['chia.wallet.wallet_blockchain']['contador'], log['chaingreen']['INFO']['wallet']['chaingreen.wallet.wallet_blockchain']['contador'], log['flax']['INFO']['wallet']['flax.wallet.wallet_blockchain']['contador'], log['spare-blockchain']['INFO']['wallet']['spare.wallet.wallet_blockchain']['contador']],
    'wallet.wallet_state_manager': [log['chia']['INFO']['wallet']['chia.wallet.wallet_state_manager']['contador'], log['chaingreen']['INFO']['wallet']['chaingreen.wallet.wallet_state_manager']['contador'], log['flax']['INFO']['wallet']['flax.wallet.wallet_state_manager']['contador'], log['spare-blockchain']['INFO']['wallet']['spare.wallet.wallet_state_manager']['contador']]
    #'Warning': [log['chia']['WARNING']['contador'], log['chaingreen']['WARNING']['contador'], log['flax']['WARNING']['contador'], log['spare-blockchain']['WARNING']['contador']]
    })
    
    # ------- PART 1: Create background
    
    # number of variable
    categories=list(df)[1:]
    N = len(categories)
    
    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)
    
    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    
    # Draw one axe per variable + add labels
    plt.xticks(angles[:-1], categories)
    
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([20,40,60], ["20","40","60"], color="grey", size=7)
    plt.ylim(0,80)
    

    # ------- PART 2: Add plots
    
    # Plot each individual = each line of the data
    # I don't make a loop, because plotting more than 3 groups makes the chart unreadable
    
    # Ind1
    values=df.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="Chia")
    ax.fill(angles, values, 'b', alpha=0.1)
    
    # Ind2
    values=df.loc[1].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="Chaingreen")
    ax.fill(angles, values, 'r', alpha=0.1)


    values=df.loc[2].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="Flax")
    ax.fill(angles, values, 'r', alpha=0.1)

    values=df.loc[3].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="Spare")
    ax.fill(angles, values, 'r', alpha=0.1)
    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    # Show the graph
    plt.title(f'Comportamiento archivos log ({datetime.now().strftime("%Y-%m-%d %H:%M:%S")})', loc='center')
    #plt.show()
   
    plt.savefig('img/analisis_log.png')

def main():

    log_harvester={}
    
    programa={'chia':'latin-1',
    'chaingreen':'latin-1',
    'flax':'latin-1',
    'spare-blockchain':'latin-1',
    'signum':'latin-1',
    'bitcoinhd':'latin-1'}
    #log_file_path = fr"C:\Users\{os.getlogin()}\.chia\mainnet\log\debug.log"
    match_list = []
    
    archivos=['','.1','.2','.3','.4','.5','.6','.7']
    registro_log={}
    if os.path.isfile("formato/registro_log_formato.json")==False: open("formato/registro_log_formato.json","w").close()
    with open("formato/registro_log_formato.json", 'r') as json_file:
        registro_log = json.load(json_file)
    for moneda in programa:
        if moneda in ('chia','chaingreen','flax','spare-blockchain'):
            regex = '^([0-9:.T-]{23}) ([a-zA-Z_.]*) ([a-zA-Z_.]*): ([A-Z]*)'
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
                            if datetime.fromisoformat(line[0:19])>(datetime.now() - timedelta(minutes=10)):
                                for match2 in re.finditer('^([0-9:.T-]{23}) ([a-zA-Z_.]*) ([a-zA-Z_.]*): ([A-Z]*)[\s]*Confirmed balance amount is ([0-9]*)', line, re.S):
                                    print(moneda, match2.groups()[4])
                                    actualiza_balance(moneda, match2.groups()[4])
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

            log_harvester.setdefault(moneda,{'cantidad':registro_log[moneda]['INFO']['harvester'][f"{moneda.replace('-blockchain','')}.harvester.harvester"]['contador'], 'porcentaje':"{:.2%}".format(registro_log[moneda]['INFO']['harvester'][f"{moneda.replace('-blockchain','')}.harvester.harvester"]['contador']/64)})
            #print(registro_log[moneda]['INFO']['harvester'][f"{moneda.replace('-blockchain','')}.harvester.harvester"]['contador'], (registro_log[moneda]['INFO']['harvester'][f"{moneda.replace('-blockchain','')}.harvester.harvester"]['contador']/64))
        elif moneda=='signum':
            regex='^([0-9:, -]{23})\s([a-zA-Z0-9-\W]*):\sbtdex.ui.MiningPanel\s([a-zA-Z0-9-\W]*)round finished: roundtime=([0-9]*)ms, speed=([0-9.]*)MiB/s'
            contador=1
            t_inicio1=process_time()
            info_faltante=True
            fin_bucle=False
            if info_faltante==False: break
            n=0
            #fr"{parametros.ruta_log_signum}\\btdex.log"
            with FileReadBackwards(parametros.ruta_log_signum , encoding=programa[moneda]) as frb:
                tmoneda=process_time()
                
                for line in frb:
                    if fin_bucle: break
                    for match in re.finditer(regex, line, re.S):
                        #print(line[0:19].replace(' ','T').replace(',','.'), datetime.fromisoformat(line[0:19].replace(' ','T').replace(',','.'))>(datetime.now() - timedelta(minutes=60)))
   
                        if datetime.fromisoformat(line[0:19].replace(' ','T').replace(',','.'))>(datetime.now() - timedelta(minutes=120)):
                                registro_log[moneda]['contador']+=1

                t_fin1=process_time()
                print("\t",moneda,f"archivo: btdex.log",f"-> tiempo ejecución: {t_fin1-tmoneda} segundos")
            t_fin1=process_time()
            print(moneda, f"-> tiempo ejecución: {t_fin1-t_inicio1} segundos")

            log_harvester.setdefault(moneda,{'cantidad':registro_log[moneda]['contador'],'porcentaje':"{:.2%}".format(registro_log[moneda]['contador']/30)})
            #print({'cantidad':registro_log[moneda]['contador'],'porcentaje':registro_log[moneda]['contador']/15})
        elif moneda=='bitcoinhd':
            regex='^([0-9:. -]{23})\s([a-zA-Z0-9-\W]*) round finished: roundtime=([0-9]*)ms, speed=([0-9.]*)MiB/s'
            contador=1
            t_inicio1=process_time()
            info_faltante=True
            fin_bucle=False
            if info_faltante==False: break
            n=0
            #fr"{parametros.ruta_log_signum}\\btdex.log"
            with FileReadBackwards(parametros.ruta_log_bhd , encoding=programa[moneda]) as frb:
                tmoneda=process_time()
                
                #print(line[0:19].replace(' ','T').replace(',','.'), datetime.fromisoformat(line[0:19].replace(' ','T').replace(',','.'))>(datetime.now() - timedelta(minutes=120)))
                for line in frb:
                    if fin_bucle: break
                    for match in re.finditer(regex, line, re.S):
                        #print(line[0:19].replace(' ','T').replace(',','.'), datetime.fromisoformat(line[0:19].replace(' ','T').replace(',','.'))>(datetime.now() - timedelta(minutes=60)))
   
                        if datetime.fromisoformat(line[0:19].replace(' ','T').replace(',','.'))>(datetime.now() - timedelta(minutes=120)):
                                registro_log[moneda]['contador']+=1

                t_fin1=process_time()
                print("\t",moneda,f"archivo: btdex.log",f"-> tiempo ejecución: {t_fin1-tmoneda} segundos")
            t_fin1=process_time()
            print(moneda, f"-> tiempo ejecución: {t_fin1-t_inicio1} segundos")

            log_harvester.setdefault(moneda,{'cantidad':registro_log[moneda]['contador'],'porcentaje':"{:.2%}".format(registro_log[moneda]['contador']/40)})
            #print({'cantidad':registro_log[moneda]['contador'],'porcentaje':registro_log[moneda]['contador']/20})
    log_harvester1={}
    if os.path.isfile("data/registro_log_harvester.json")==False: 
        open("data/registro_log_harvester.json","w").close()
    else:
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
    t_inicio=process_time()
    
    grafico_log()
    t_fin=process_time()
    print(f"Análisis de log: Tiempo ejecución: {t_fin-t_inicio} segundos")
    t_inicio=process_time()

    estado_harvester()
    t_fin=process_time()
    print(f"Análisis de Harvester: Tiempo ejecución: {t_fin-t_inicio} segundos")
    t_inicio=process_time()

    historia_harvester()
    t_fin=process_time()
    print(f"Análisis historia de Harvester: Tiempo ejecución: {t_fin-t_inicio} segundos")
    t_fin_gral=process_time()
    print(f"Tiempo Total ejecución: {t_fin_gral-t_inicio_gral} segundos")

def analiza_sp():
    hora_corte=(datetime.now() - timedelta(days=1))
    log_historico_24hr={}
    log_historico_24hr_nuevos={}
    with open("data/registro_parciales.json", 'r') as json_file:
        log_historico_24hr = json.load(json_file)
    log_historico_24hr=dict(log_historico_24hr)
    sp_nuevos=[]
    alias=""
    regex = '^([0-9:.T-]{23}) ([a-zA-Z_.]*) ([a-zA-Z_ .]*): ([A-Z]*)'
    archivos=['','.1','.2','.3','.4','.5','.6','.7']
    reg_parcial_estropeado='^([0-9:.T-]{23}) ([a-zA-Z_.]*) ([a-zA-Z _.]*): ERROR[\s]*Error in pooling'
    reg_parcial_invalido='^([0-9:.T-]{23}) ([a-zA-Z_.]*) ([a-zA-Z _.]*): ERROR[\s]*Error connecting to pool: Cannot connect to host'
    reg_sp='^([0-9:.T-]{23}) ([a-zA-Z_.]*) ([a-zA-Z_.]*): INFO[\s]*([0-9]*) plots were eligible for farming ([0-9a-z]*)... Found ([0-9]*) proofs. Time: ([0-9.]*) s. Total ([0-9]*)'
    reg_get_pool="^([0-9:.T-]{23}) ([a-zA-Z_.]*) ([a-zA-Z _ .]*): INFO[\s]* GET /farmer response: \{'authentication_public_key': '0x8e03a755200[a-z0-9 :,']* 'current_difficulty': ([0-9]*), 'current_points': ([0-9]*)"
    reg_inicio_sp='^([0-9:.T-]{23}) ([a-zA-Z_.]*) ([a-zA-Z _ .]*): INFO[\s]*Finished sub slot, SP 64/64, ([a-z0-9]*)'
    reg_server_down='^([0-9:.T-]{23}) ([a-zA-Z_.]*) ([a-zA-Z _.]*): ERROR[\s][a-zA-Z _:.,/]*Server disconnected'
    fin_bucle=False
    server_down=False
    for archivo in archivos:
        with FileReadBackwards(fr"C:\Users\{os.getlogin()}\.chia\mainnet\log\debug.log{archivo}",encoding='latin-1') as frb:
            tmoneda=process_time()
            for line in frb:
                if fin_bucle: break
                for validos in re.finditer(regex, line, re.S):
                    if datetime.fromisoformat(line[0:19])>(datetime.now() - timedelta(minutes=30)):

                        for match in re.finditer(reg_sp, line, re.S):
                            alias=match.groups()[4]
                            
                            if alias not in sp_nuevos:
                                sp_nuevos.append(match.groups()[4])
                                log_historico_24hr_nuevos.setdefault(match.groups()[4],{
                                    "timestamp": "",
                                    "alias":match.groups()[4],
                                    "signage_points":0,
                                    "pruebas":0,
                                    "total_parciales" :0,
                                    "parciales_validos":0,
                                    "parciales_estropeados":0,
                                    "parciales_invalidos":0,
                                    "dificultad":0,
                                    "plots":0,
                                    "puntaje":0,
                                    "TiB_estimados":0,                                    
                                    "tiempos":[],
                                    "t_min":0,
                                    "t_max":0,
                                    "t_prom":0 
                                    })

                            if log_historico_24hr_nuevos[match.groups()[4]]["timestamp"]=="":
                                log_historico_24hr_nuevos[match.groups()[4]]["timestamp"]=match.groups()[0]
                            else:
                                log_historico_24hr_nuevos[match.groups()[4]]["timestamp"]=datetime.isoformat(min([datetime.fromisoformat(log_historico_24hr_nuevos[match.groups()[4]]["timestamp"]),datetime.fromisoformat(match.groups()[0])])                            )
                            log_historico_24hr_nuevos[match.groups()[4]]["signage_points"]+=1
                            log_historico_24hr_nuevos[match.groups()[4]]["pruebas"]+=int(match.groups()[3])
                            log_historico_24hr_nuevos[match.groups()[4]]["total_parciales"]+=int(match.groups()[5])
                            log_historico_24hr_nuevos[match.groups()[4]]["tiempos"].append(float(match.groups()[6]))
                            log_historico_24hr_nuevos[match.groups()[4]]["plots"]=float(match.groups()[7])
                        for match in re.finditer(reg_parcial_estropeado, line, re.S):
                            log_historico_24hr_nuevos[alias]["parciales_estropeados"]+=1
                        for match in re.finditer(reg_parcial_invalido, line, re.S):
                            log_historico_24hr_nuevos[alias]["parciales_invalidos"]+=1
                            #parametros.bot.send_message(parametros.chat_id, '@h4tt3r Pool desconectada, validar y cambiarse de pool opciones: https://xch-us-east.flexpool.io o https://api.biopool.tk')   
                        for match in re.finditer(reg_get_pool, line, re.S):
                            #dificultad=int(match.groups()[3])
                            log_historico_24hr_nuevos[alias]["dificultad"]=int(match.groups()[3])
                            log_historico_24hr_nuevos[alias]["puntaje"]=int(match.groups()[4])
                            #if int(match.groups()[4])==0:
                                #print(line[0:19],"bloque pagado por la pool")
                            
                        for match in re.finditer(reg_inicio_sp, line, re.S):
                            if log_historico_24hr_nuevos[alias]["timestamp"]=="":
                                log_historico_24hr_nuevos[alias]["timestamp"]=datetime.isoformat(match.groups()[0])
                            else:
                                log_historico_24hr_nuevos[alias]["timestamp"]=datetime.isoformat(min([datetime.fromisoformat(log_historico_24hr_nuevos[alias]["timestamp"]),datetime.fromisoformat(match.groups()[0])]))
                    else:
                        fin_bucle=True
                        for signagnes_nuevos in sp_nuevos:
                            log_historico_24hr_nuevos[signagnes_nuevos]["t_min"]=round(min(log_historico_24hr_nuevos[signagnes_nuevos]["tiempos"]),3)
                            log_historico_24hr_nuevos[signagnes_nuevos]["t_max"]=round(max(log_historico_24hr_nuevos[signagnes_nuevos]["tiempos"]),3)
                            log_historico_24hr_nuevos[signagnes_nuevos]["t_prom"]=round(sum(log_historico_24hr_nuevos[signagnes_nuevos]["tiempos"]) / len(log_historico_24hr_nuevos[signagnes_nuevos]["tiempos"]),3)
                            log_historico_24hr_nuevos[signagnes_nuevos]["parciales_validos"]=log_historico_24hr_nuevos[signagnes_nuevos]["total_parciales"]-log_historico_24hr_nuevos[signagnes_nuevos]["parciales_estropeados"]-log_historico_24hr_nuevos[signagnes_nuevos]["parciales_validos"]
                            log_historico_24hr_nuevos[signagnes_nuevos]["TiB_estimados"]=log_historico_24hr_nuevos[alias]["dificultad"]*log_historico_24hr_nuevos[signagnes_nuevos]["parciales_validos"]*6*24*101/(10000)   
                            print(log_historico_24hr_nuevos[alias]["timestamp"],log_historico_24hr_nuevos[alias]["dificultad"]*log_historico_24hr_nuevos[signagnes_nuevos]["parciales_validos"]*6*24*101/(10000)   )
                            if signagnes_nuevos in log_historico_24hr:
                                if log_historico_24hr_nuevos[signagnes_nuevos]["signage_points"]<log_historico_24hr[signagnes_nuevos]["signage_points"]:
                                    log_historico_24hr_nuevos.pop(signagnes_nuevos)
                                else:
                                    log_historico_24hr.pop(signagnes_nuevos)
                        for match in re.finditer(reg_server_down, line, re.S):
                            server_down=True
                            
    z = dict(list(log_historico_24hr.items()) + list(log_historico_24hr_nuevos.items()))
    for n in z.copy():
        
        #print(n,z[n]["signage_points"],datetime.fromisoformat(z[n]["timestamp"]),hora_corte,datetime.fromisoformat(z[n]["timestamp"])<hora_corte, f"|| Hora Actual: {datetime.now()}")
        if datetime.fromisoformat(z[n]["timestamp"])<hora_corte:
            #print(n,"se elimina por tener fecha",z[n]["timestamp"])
            z.pop(n)
            
    with open("data/registro_parciales.json", 'w') as outfile:
        json.dump(dict(sorted(z.items(), key=lambda item: item[1]['timestamp'])), outfile,indent=3)
    if server_down==True:
        print('Servidor de pool caído')
    #print(log_historico_24hr_nuevos)

def grafica_proofs():
    log_historico_24hr={}
    with open("data/registro_parciales.json", 'r') as json_file:
        log_historico_24hr = json.load(json_file)
    
    df=pd.DataFrame.from_dict(log_historico_24hr,orient='index',columns=['timestamp','parciales_validos','parciales_estropeados','parciales_invalidos','dificultad','total_parciales'])
    df['timestamp']= pd.to_datetime(df['timestamp'])
    fig, ax = plt.subplots(num=10,facecolor='#0B1C28', figsize=(12,6))
    ax.bar('timestamp', 'parciales_validos', data=df,   color='blue', label='Parciales Válidos', width = 0.005)
    ax.bar('timestamp', 'parciales_estropeados', data=df,   color='yellow', label='Parciales Estropeados', width = 0.005)
    ax.bar('timestamp', 'parciales_invalidos', data=df,   color='grey', label='Parciales Inválidos', width = 0.005)
    ax.plot('timestamp', 'dificultad', data=df ,  color='white', label='Dificultad')
    ax.spines['top'].set_color('#0B1C28') 
    ax.spines['right'].set_color('#0B1C28')
    ax.spines['left'].set_color('#0B1C28')
    ax.spines['bottom'].set_color('white')
    ax.tick_params(axis='x', colors='white')  
    ax.tick_params(axis='y', colors='white')
    ax.set_ylabel('PARCIALES ENCONTRADOS',color='white')
    ax.set_xlabel(f'HORA \n(Actualización:{datetime.now().strftime("%Y-%m-%d %H:%M:%S")})',color='white')
    ax.set_title('Distribución de parciales por signage point',color='white')
    ax.legend(loc='upper left')
    ax.set_xlim(df['timestamp'].min(),df['timestamp'].max())
    ax.set_ylim(0,df['parciales_validos'].max()*1.2)
    ax.xaxis.set_major_locator(mdates.HourLocator(interval = 3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    men_parvalidos=f"Parciales válidos:{df['parciales_validos'].sum()} ("+"{:.2%}".format(df['parciales_validos'].sum()/df['total_parciales'].sum())+")"
    men_parinvalidos=f"Parciales inválidos:{df['parciales_invalidos'].sum()} ("+"{:.2%}".format(df['parciales_invalidos'].sum()/df['total_parciales'].sum())+")"
    men_parestropeados=f"Parciales estropeados:{df['parciales_estropeados'].sum()} ("+"{:.2%}".format(df['parciales_estropeados'].sum()/df['total_parciales'].sum())+")"
    ax.text(df['timestamp'].max()-timedelta(hours=7),df['parciales_validos'].max()*0.85,f"Últimas 24 horas \n{men_parvalidos}\n{men_parestropeados}\n{men_parinvalidos}",
        bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 10})   

    df.loc[df['timestamp'] >= df['timestamp'].max()-timedelta(hours=1), 'parciales_validos'].sum() 
    men_parvalidos=f"Parciales válidos:{df.loc[df['timestamp'] >= df['timestamp'].max()-timedelta(hours=1), 'parciales_validos'].sum() } ("+"{:.2%}".format(df.loc[df['timestamp'] >= df['timestamp'].max()-timedelta(hours=1), 'parciales_validos'].sum() /df.loc[df['timestamp'] >= df['timestamp'].max()-timedelta(hours=1), 'total_parciales'].sum())+")"
    men_parinvalidos=f"Parciales inválidos:{df.loc[df['timestamp'] >= df['timestamp'].max()-timedelta(hours=1), 'parciales_invalidos'].sum() } ("+"{:.2%}".format(df.loc[df['timestamp'] >= df['timestamp'].max()-timedelta(hours=1), 'parciales_invalidos'].sum() /df.loc[df['timestamp'] >= df['timestamp'].max()-timedelta(hours=1), 'total_parciales'].sum())+")"
    men_parestropeados=f"Parciales estropeados:{df.loc[df['timestamp'] >= df['timestamp'].max()-timedelta(hours=1), 'parciales_estropeados'].sum() } ("+"{:.2%}".format(df.loc[df['timestamp'] >= df['timestamp'].max()-timedelta(hours=1), 'parciales_estropeados'].sum() /df.loc[df['timestamp'] >= df['timestamp'].max()-timedelta(hours=1), 'total_parciales'].sum())+")"
  
    ax.text(df['timestamp'].max()-timedelta(hours=7),df['parciales_validos'].max()*0.62,f"Última hora \n{men_parvalidos}\n{men_parestropeados}\n{men_parinvalidos}",
        bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 10}) 
    ax.set_facecolor('#102b38')
    #plt.show()
    plt.savefig('img/registro_parciales_24h.png')
    mensajes={}
    if os.path.isfile("data/telegram_mensajes.json"):
        with open("data/telegram_mensajes.json", 'r') as json_file:
            mensajes = json.load(json_file)
            if "parciales" in mensajes:
                parametros.bot.edit_message_media(media=types.InputMediaPhoto(open('img/logo.png', 'rb')),message_id=mensajes["parciales"], chat_id=parametros.chat_id)
                parametros.bot.edit_message_media(media=types.InputMediaPhoto(open('img/registro_parciales_24h.png', 'rb')),message_id=mensajes["parciales"], chat_id=parametros.chat_id)
            else:
                id1=parametros.bot.send_photo(parametros.chat_id, photo=open('img/registro_parciales_24h.png', 'rb'))
                
                mensajes.setdefault("parciales",id1.message_id)
                with open("data/telegram_mensajes.json", 'w') as outfile:
                    json.dump(mensajes, outfile,indent=3)
    else:
        id1=parametros.bot.send_photo(parametros.chat_id, photo=open('img/registro_parciales_24h.png', 'rb'))
        mensajes.setdefault("parciales",id1.message_id)
        with open("data/telegram_mensajes.json", 'w') as outfile:
            json.dump(mensajes, outfile,indent=3)

def grafica_tib():
    log_historico_24hr={}
    with open("data/registro_parciales.json", 'r') as json_file:
        log_historico_24hr = json.load(json_file)
    
    df=pd.DataFrame.from_dict(log_historico_24hr,orient='index',columns=['timestamp','TiB_estimados'])
    df['timestamp']= pd.to_datetime(df['timestamp'])
    df['TiB_estimados_6h'] = df.TiB_estimados.rolling(18, min_periods=1).mean()
    fig, ax = plt.subplots(num=11,facecolor='#0B1C28', figsize=(12,6))
    ax.plot('timestamp', 'TiB_estimados', data=df ,  color='blue', label='TiB estimado según parciales válidos')
    ax.plot('timestamp', 'TiB_estimados_6h', data=df ,  color='green', label='TiB media móvil de 3 horas')
    ax.spines['top'].set_color('#0B1C28') 
    ax.spines['right'].set_color('#0B1C28')
    ax.spines['left'].set_color('#0B1C28')
    ax.spines['bottom'].set_color('white')
    ax.tick_params(axis='x', colors='white')  
    ax.tick_params(axis='y', colors='white')
    ax.set_ylabel('TiB',color='white')
    ax.set_xlabel(f'HORA \n(Actualización:{datetime.now().strftime("%Y-%m-%d %H:%M:%S")})',color='white')
    ax.set_title('TiB según parciales válidos encontrados',color='white')
    ax.legend(loc='upper left')
    ax.set_xlim(df['timestamp'].min(),df['timestamp'].max())
    ax.set_ylim(0,df['TiB_estimados'].max()*1.2)
    ax.xaxis.set_major_locator(mdates.HourLocator(interval = 3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set_facecolor('#102b38')
    #print(df['timestamp'].max()-timedelta(hours=24))
    #print(round(df.loc[df['timestamp'] >=df['timestamp'].max()-timedelta(hours=24), 'TiB_estimados'].mean(),2))
    ax.text(df['timestamp'].max()-timedelta(hours=4.85),df['TiB_estimados'].max()*0.89,f"TiB promedio \nPasadas 24h: {round(df.loc[df['timestamp'] >=df['timestamp'].max()-timedelta(hours=24), 'TiB_estimados'].mean(),2)} TiB\nPasadas 6h: {round(df.loc[df['timestamp'] >=df['timestamp'].max()-timedelta(hours=6), 'TiB_estimados'].mean(),2)} TiB\nPasadas 3h: {round(df.loc[df['timestamp'] >=df['timestamp'].max()-timedelta(hours=3), 'TiB_estimados'].mean(),2)} TiB\nPasada 1h: {round(df.loc[df['timestamp'] >=df['timestamp'].max()-timedelta(hours=1), 'TiB_estimados'].mean(),2)} TiB",
        bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 10})
    plt.savefig('img/registro_tib_24h.png')
    mensajes={}
    if os.path.isfile("data/telegram_mensajes.json"):
        with open("data/telegram_mensajes.json", 'r') as json_file:
            mensajes = json.load(json_file)
            if "tib_movil" in mensajes:
                parametros.bot.edit_message_media(media=types.InputMediaPhoto(open('img/logo.png', 'rb')),message_id=mensajes["tib_movil"], chat_id=parametros.chat_id)
                parametros.bot.edit_message_media(media=types.InputMediaPhoto(open('img/registro_tib_24h.png', 'rb')),message_id=mensajes["tib_movil"], chat_id=parametros.chat_id)
            else:
                id1=parametros.bot.send_photo(parametros.chat_id, photo=open('img/registro_tib_24h.png', 'rb'))
                
                mensajes.setdefault("tib_movil",id1.message_id)
                with open("data/telegram_mensajes.json", 'w') as outfile:
                    json.dump(mensajes, outfile,indent=3)
    else:
        id1=parametros.bot.send_photo(parametros.chat_id, photo=open('img/registro_tib_24h.png', 'rb'))
        mensajes.setdefault("tib_movil",id1.message_id)
        with open("data/telegram_mensajes.json", 'w') as outfile:
            json.dump(mensajes, outfile,indent=3)

if __name__ == "__main__":
    main()
    analiza_sp()
    grafica_proofs()
    grafica_tib()