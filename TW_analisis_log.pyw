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

t2=process_time()
print(f"Importar Librerias: {t2-t1} segundos")
def actualiza_balance(moneda, monto):
    wallets={}
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
    with open("data/registro_log_harvester.json", 'r') as json_file:
        log = json.load(json_file)

    data=[]
    for key, fila in log.items():
        data.append([key[11:16], float(fila['chia']['porcentaje'].strip('%'))/100,float(fila['chaingreen']['porcentaje'].strip('%'))/100,float(fila['flax']['porcentaje'].strip('%'))/100,float(fila['spare-blockchain']['porcentaje'].strip('%'))/100])

    df = pd.DataFrame(data,columns=['hora','chia','chaingreen','flax','spare-blockchain'])
    plt.plot('hora', 'chia', data=df,   color='green', label='chia')
    plt.plot('hora', 'chaingreen', data=df,   color='orange', label='chaingreen')
    plt.plot('hora', 'flax', data=df,   color='grey', label='flax')
    plt.plot('hora', 'spare-blockchain', data=df,   color='blue', label='spare')
    plt.ylim(0,1.3)
    #plt.grid(axis='x', color='0.95')
    plt.xticks(np.arange(0, len(df['hora']), 30))


    plt.legend(title='Moneda:')
    plt.title(f'Salud del Harvester: Porcentaje de cumplimiento de Signage Point (última actualizacion: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')
    #plt.plot()
    plt.savefig('img/registro_log_harvester_24h.png')
    parametros.bot.edit_message_media(media=types.InputMediaPhoto(open('img/logo.png', 'rb')),message_id=847, chat_id=parametros.chat_id)
    parametros.bot.edit_message_media(media=types.InputMediaPhoto(open('img/registro_log_harvester_24h.png', 'rb')),message_id=847, chat_id=parametros.chat_id)
    #plt.show()
def estado_harvester():
    log_harvester={}
    fecha=''
    with open("data/registro_fecha.txt", 'r') as json_file:
        fecha = json.load(json_file)
    with open("data/registro_log_harvester.json", 'r') as json_file:
        log_harvester = json.load(json_file)
        #print(log_harvester)
        valor=[log_harvester[fecha]['chia']['cantidad'], log_harvester[fecha]['chaingreen']['cantidad'], log_harvester[fecha]['flax']['cantidad'], log_harvester[fecha]['spare-blockchain']['cantidad']]

    color=[]
    n=0
    for i in valor:
        if i<=307:
            color.insert(n,'red')
        elif i>=364:
            color.insert(n,'green')
        else:
            color.insert(n,'yellow')
        n=n+1

    trace1 = go.Indicator(mode="gauge+number",
            value=log_harvester[fecha]['chia']['cantidad'],
            delta = {'reference': 384}, 
            gauge = {'axis': {'range': [None, 400]},
                    'steps' :[
                                {'range': [0, 307], 'color': "lightgray"},
                                {'range': [307, 364], 'color': "gray"}
                            ], 
                    'bar': {'color': color[0]},
                    'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 384}}, 
            domain={'row' : 1, 'column' : 1}, title={'text': "Chia"})
    trace2 = go.Indicator(mode="gauge+number",    
            value=log_harvester[fecha]['chaingreen']['cantidad'],
            delta = {'reference': 384}, 
            gauge = {'axis': {'range': [None, 400]}, 
                    'steps' :[
                                {'range': [0, 307], 'color': "lightgray"},
                                {'range': [307, 364], 'color': "gray"}
                            ], 
                    'bar': {'color': color[1]},
                    'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 384}},    
            domain={'row' : 1, 'column' : 2}, title={'text': "Chaingreen"})
    trace3 = go.Indicator(mode="gauge+number",    
            value=log_harvester[fecha]['flax']['cantidad'],
            delta = {'reference': 384}, 
            gauge = {'axis':{'range': [None, 400]},
                    'steps' :[
                                {'range': [0, 307], 'color': "lightgray"},
                                {'range': [307, 364], 'color': "gray"}
                            ],  
                    'bar': {'color': color[2]},
                    'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 384}},    
            domain={'row' : 2, 'column' : 1}, title={'text': "Flax"})
    trace4 = go.Indicator(mode="gauge+number",    
            value=log_harvester[fecha]['spare-blockchain']['cantidad'],
            delta = {'reference': 384},  
            gauge = {'axis':{'range': [None, 400]}, 
                    'steps' :[
                                {'range': [0, 307], 'color': "lightgray"},
                                {'range': [307, 364], 'color': "gray"}
                            ], 
                    'bar': {'color': color[3]},
                    'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 384}},    
            domain={'row' : 2, 'column' : 2}, title={'text': "Spare"})


    fig = make_subplots(
        rows=2,
        cols=2,
        specs=[[{'type' : 'indicator'}, {'type' : 'indicator'}],[{'type' : 'indicator'}, {'type' : 'indicator'}]],
        )
        
    fig.update_layout(title_text="Cantidad Signage point por hora")
    #,         scene=dict(        annotations=[        dict(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))])
    fig.append_trace(trace1, row=1, col=1)
    fig.append_trace(trace2, row=1, col=2)
    fig.append_trace(trace3, row=2, col=1)
    fig.append_trace(trace4, row=2, col=2)
    #fig.show()

    fig.write_image("img/estado_harvester.png")
    parametros.bot.edit_message_media(media=types.InputMediaPhoto(open('img/logo.png', 'rb')),message_id=846, chat_id=parametros.chat_id)
    parametros.bot.edit_message_media(media=types.InputMediaPhoto(open('img/estado_harvester.png', 'rb')),message_id=846, chat_id=parametros.chat_id)
    parametros.bot.edit_message_media(media=types.InputMediaPhoto(open('img/logo.png', 'rb')),message_id=848, chat_id=parametros.chat_id)
    parametros.bot.edit_message_media(media=types.InputMediaPhoto(open('img/analisis_log.png', 'rb')),message_id=848, chat_id=parametros.chat_id)
def grafico_log():
    log={}
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
    plt.yticks([100,200,300], ["100","200","300"], color="grey", size=7)
    plt.ylim(0,400)
    

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
    plt.title(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), loc='center')
    #plt.show()
   
    plt.savefig('img/analisis_log.png')

def main():

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
    with open("registro_log_formato.json", 'r') as json_file:
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

        log_harvester.setdefault(moneda,{'cantidad':registro_log[moneda]['INFO']['harvester'][f"{moneda.replace('-blockchain','')}.harvester.harvester"]['contador'], 'porcentaje':"{:.2%}".format(registro_log[moneda]['INFO']['harvester'][f"{moneda.replace('-blockchain','')}.harvester.harvester"]['contador']/384)})
        #print(registro_log[moneda]['INFO']['harvester'][f"{moneda.replace('-blockchain','')}.harvester.harvester"]['contador'], (registro_log[moneda]['INFO']['harvester'][f"{moneda.replace('-blockchain','')}.harvester.harvester"]['contador']/384))

    log_harvester1={}
    with open("data/registro_log_harvester.json", 'r') as json_file:
        log_harvester1 = json.load(json_file)
    fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_harvester1.setdefault(fecha,log_harvester)
    #print(log_harvester1)
    for fecha in log_harvester1.copy():
        #print(fecha)
        if fecha<(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"):
            log_harvester1.pop(fecha)
    
    
    with open("registro_log_harvester.json", 'w') as outfile:
        json.dump(log_harvester1, outfile,indent=3)
    with open("data/registro_log.json", 'w') as outfile:
        json.dump(registro_log, outfile, indent=4)
    with open("registro_fecha.txt", 'w') as outfile:
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

if __name__ == "__main__":
    main()