import parametros
from datetime import datetime, time
import time
import json
import shutil
import string
from ctypes import windll
import os
import pandas as pd
from pandas.core.indexes.base import Index
from tabulate import tabulate
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import subprocess
import requests

def actualiza_wallet_signa():
    wallets={}
    balances={}
    try:   
        response = requests.get("https://signapool.notallmine.net/api/getMiner/S-GR8U-E9VA-4NJ2-FQUB4")
        if (response.status_code == 200):
            print("Conexión exitosa")
            #print(response.json())
            balances=response.json()
            print(balances['pendingBalance'])
            print(balances['committedBalance'])
            print(float(balances['pendingBalance'].replace(' SIGNA',''))+float(balances['committedBalance'].replace(' SIGNA','')))
            with open("data/wallets.json", 'r') as json_file:
                wallets = json.load(json_file)
            wallets['signum']['balance']="0"
            wallets['signum']['commitment']=balances['committedBalance'].replace(' SIGNA','')
            wallets['signum']['balance_pendiente']=str(balances['pendingBalance']).replace(' SIGNA','')
            wallets['signum']['balance_total']=str(float(balances['pendingBalance'].replace(' SIGNA',''))+float(balances['committedBalance'].replace(' SIGNA','')))
            wallets['signum']['timestamp_wallet']=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            with open("data/wallets.json", 'w') as outfile:
                json.dump(wallets, outfile,indent=3)
        elif (response.status_code == 404):
            print("Conexión con error 404")
            # Code here will react to failed requests
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e,"excepcion")

def actualiza_precios():
    api_token="9da2b54f-ed6e-4dcc-88a8-42aee223c5b4"
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
    "symbol": "BTC,SIGNA,XCH,BHD,MASS"
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_token,
    }
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        wallets={}
        with open("data/wallets.json", 'r') as json_file:
            wallets = json.load(json_file)
    #print(data)
        for symbol in data['data']:
            print(data['data'][symbol]['name'].replace(' Network','').lower(), symbol, data['data'][symbol]['quote']['USD']['price'],  data['data'][symbol]['quote']['USD']['percent_change_24h'])
            wallets[data['data'][symbol]['name'].replace(' Network','').lower()]["coinmarketcap"]["valor_usd"]=data['data'][symbol]['quote']['USD']['price']
            wallets[data['data'][symbol]['name'].replace(' Network','').lower()]["coinmarketcap"]["percent_change_1h"]=data['data'][symbol]['quote']['USD']['percent_change_1h']
            wallets[data['data'][symbol]['name'].replace(' Network','').lower()]["coinmarketcap"]["percent_change_24h"]=data['data'][symbol]['quote']['USD']['percent_change_24h']
            wallets[data['data'][symbol]['name'].replace(' Network','').lower()]["coinmarketcap"]["percent_change_7d"]=data['data'][symbol]['quote']['USD']['percent_change_7d']
            wallets[data['data'][symbol]['name'].replace(' Network','').lower()]["coinmarketcap"]["percent_change_30d"]=data['data'][symbol]['quote']['USD']['percent_change_30d']
            wallets[data['data'][symbol]['name'].replace(' Network','').lower()]["coinmarketcap"]["percent_change_60d"]=data['data'][symbol]['quote']['USD']['percent_change_60d']
            wallets[data['data'][symbol]['name'].replace(' Network','').lower()]["coinmarketcap"]["percent_change_90d"]=data['data'][symbol]['quote']['USD']['percent_change_90d']
            wallets[data['data'][symbol]['name'].replace(' Network','').lower()]["coinmarketcap"]["timestamp_coinmarket"]=data['status']['timestamp']
            #print(wallets)
        with open("data/wallets.json", 'w') as outfile:
            json.dump(wallets, outfile, indent=3)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

def actualiza_wallet():
    actualiza_wallet_signa()
    wallets={}
    assert os.path.isdir(parametros.ruta_daemon)
    os.chdir(parametros.ruta_daemon)
    p = subprocess.run([".\chia.exe","wallet","show","-f",str(parametros.finger_print)], capture_output=True)
    balance=p.stdout[p.stdout.decode().find("-Total Balance: ")+16:p.stdout.decode().find(" xch (")].decode()
    #nro_pruebas=int(p.stderr[fndproof-3:fndproof-1].decode())
    assert os.path.isdir(parametros.ruta_actual)
    os.chdir(parametros.ruta_actual)

    with open("data/wallets.json", 'r') as json_file:
        wallets = json.load(json_file)
    wallets['chia']['balance']=str(float(balance))
    wallets['chia']['balance_total']=str(float(balance)+float(wallets['chia']['balance_pendiente']))
    wallets['chia']['timestamp_wallet']=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open("data/wallets.json", 'w') as outfile:
        json.dump(wallets, outfile,indent=3)

def analiza_discos():
    ttotal=0
    tused=0
    tfree=0
    drives = {}
    resumen=[]
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            total, used, free = shutil.disk_usage(f"{letter}:/")
            drives.setdefault(letter, {
            "Total" : (total // (2**30)),
            "Utilizado" : (used // (2**30)),
            "Diponible" : (free // (2**30))   
            })
            ttotal+=total// (2**30)
            tused+=used// (2**30)
            tfree+=free// (2**30)
        bitmask >>= 1
    drives.setdefault('Total', {
            "Total" : ttotal,
            "Utilizado" : tused,
            "Diponible" : tfree   
            })
    #print (drives)
    #pd.DataFrame(drives,columns=['hora','chia','chaingreen','flax','spare-blockchain'])
    TTamaño_carpeta =0
    for moneda in parametros.blockchain:
        Tamaño_carpeta = 0
        for disco in parametros.blockchain[moneda]:
            for entry in os.scandir(disco):
                if entry.is_file():
                    Tamaño_carpeta += entry.stat().st_size
                    TTamaño_carpeta += entry.stat().st_size//(2**30)
        resumen.append([moneda,f"{Tamaño_carpeta//(2**30)} Gib","{:.2%}".format(Tamaño_carpeta//(2**30)/ tused), "{:.2%}".format(Tamaño_carpeta//(2**30)/ttotal)])
    resumen.append(['Sistema',f"{tused-TTamaño_carpeta} Gib","{:.2%}".format((tused-TTamaño_carpeta)/ tused), "{:.2%}".format((tused-TTamaño_carpeta)/ttotal)])
    #print(resumen)
    resumen.append(["-----------","---------","-------","-------"])
    resumen.append(['Utilizado',f"{tused} Gib","100.00%","{:.2%}".format(tused/ttotal)])
    resumen.append(['Libre',f"{tfree} Gib","","{:.2%}".format(tfree/ttotal)])
    resumen.append(['Total',f"{ttotal} Gib","","100.00%"])
    df=pd.DataFrame(resumen,columns=['Ítem','Tamaño','% uso','% total'])
    df=df.to_string(index=False)
    #print(df)
    parametros.bot.send_message(parametros.chat_id, f'```{df}```',parse_mode="markdown")

def wallet_actual():
    wallets={}
    resumen=[]
    profit=0.0
    if os.path.isfile("data/wallets.json")==False: 
        open("data/wallets.json","w").close()
    else:
        with open("data/wallets.json", 'r') as json_file:
            wallets = json.load(json_file)
    for moneda in wallets:
        profit+=float(wallets[moneda]['balance_total'])*float(wallets[moneda]['coinmarketcap']['valor_usd'])
        resumen.append([moneda.capitalize().replace('-blockchain',''),"{:.4g}".format(float(wallets[moneda]['balance_total']))+" "+wallets[moneda]['moneda'],"USD "+ str(round(float(wallets[moneda]['balance_total'])*float(wallets[moneda]['coinmarketcap']['valor_usd']),1))])
    resumen.append(["Total","", "USD {:.4}".format(profit)])
    df=pd.DataFrame(resumen,columns=['Moneda','Balance','Estimado'])
    df=df.to_string(index=False)
    #print(df)
    parametros.bot.send_message(parametros.chat_id, f'```{df}```',parse_mode="markdown")

def resumen_diario():
    proofs=0
    plots_analizados={}

    if os.path.isfile("data/registro_plots.json")==False: 
        open("data/registro_plots.json","w").close()
    else:
        with open("data/registro_plots.json", 'r') as json_file:
            plots_analizados = json.load(json_file)
    plots_nuevos=0
    for key, valor in plots_analizados.items():
        proofs=proofs+plots_analizados[key]['pruebas_aprobadas']
        a=plots_analizados[key]['pruebas_aprobadas']/parametros.check_plot_nro_proof
        #print(plots_analizados[key]['fecha_creacion'], (datetime.now()- datetime.fromtimestamp(time.mktime(datetime.strptime(plots_analizados[key]['fecha_creacion'],"%d/%m/%Y %H:%M:%S").timetuple()))).total_seconds()<=24*60*60)
        if (datetime.now()- datetime.fromtimestamp(time.mktime(datetime.strptime(plots_analizados[key]['fecha_creacion'],"%d/%m/%Y %H:%M:%S").timetuple()))).total_seconds()<=24*60*60:
            plots_nuevos=plots_nuevos+1
    if (len(plots_analizados)*parametros.check_plot_nro_proof)==0:
        calidad=0
    else:
        calidad=proofs/(len(plots_analizados)*parametros.check_plot_nro_proof)
    if calidad<=0.7:
        mensaje_check=f"🔴{round(calidad,3)}🔴"
    elif calidad>0.7 and calidad<=1:
        mensaje_check=f"🟡{round(calidad,3)}🟡"
    elif calidad>1 and calidad<=1.1:
        mensaje_check=f"🟢{round(calidad,3)}🟢"
    elif calidad>1.1:
        mensaje_check=f"🌟{round(calidad,3)}🌟"

    mensaje=f"""Hola patrones 🧑‍🌾!
    les comento como va nuestra granja:  

    Total plots: {len(plots_analizados)} ({plots_nuevos} nuevo(s))
    Calidad plots: {mensaje_check} /plots
    """
    parametros.bot.send_message(parametros.chat_id, mensaje)
    print(mensaje)

if __name__ == '__main__':
    resumen_diario()
    analiza_discos()
    actualiza_precios()
    actualiza_wallet()
    wallet_actual()
    