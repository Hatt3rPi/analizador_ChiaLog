import parametros
import os
from datetime import datetime, time
import time
import subprocess
import json
import notificador

############## Registra plots creados en directorio ##############
def validar_plots_nuevos():
    plots=[]
    plots_por_analizar={}
    with open("data/registro_plots.json", 'r') as json_file:
        plots_analizados = json.load(json_file)
    for ruta in parametros.path:
        for archivo in os.listdir(ruta):
            if archivo.endswith(".plot"):
                plots_por_analizar.setdefault(archivo, {
                "fecha_creacion": datetime.fromtimestamp(os.path.getctime(f"{ruta}\{archivo}")).strftime('%d/%m/%Y %H:%M:%S'),
                "ruta" :ruta
            })

############## Lee los plots ya procesados por el bot ##############
    with open("registro_plots_por_analizar.json", 'w') as outfile:
        json.dump(plots_por_analizar, outfile, indent=3)

    with open("registro_plots_por_analizar.json", 'r') as outfile:
        plots_por_analizar = json.load(outfile)

############## Identifica los archivos nuevos no procesados ################   
    plots=list(set(plots_por_analizar).symmetric_difference(set(plots_analizados)))
    plots_analizados=dict(plots_analizados)
    if len(plots)==0:
        print(f"{datetime.now()}: 0 Nuevo(s) plot(s) encontrado(s)")
        parametros.zero_plots_nuevos=True
    if len(plots)>0:
        print(f"{datetime.now()}: {len(plots)} Nuevo(s) plot(s) encontrado(s): {plots}")
        cmd = f"\"C:\\Program Files (x86)\\ChiaPlotStatus\\ChiaPlotStatus\\ChiaPlotStatusCli.exe\" -o C:\\Users\\{os.getlogin()}\\Documents\\Notificador\\chia_plot_status.json -f json"
        #print(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=0)
        time.sleep(5)
        f = open("data/chia_plot_status.json",)
        plot_status = json.load(f)
        for plot in plots:
            info_log=False
            print(f"--> Analizando plot {plot[26:32]}")
        #print(f"{plot[0][0:90]} con un largo de {len(plot[0])}")
            if parametros.check_plot==True:
            ####### Cambia la ruta para poder ejecutar el subprocess
                assert os.path.isdir(parametros.ruta_daemon)
                os.chdir(parametros.ruta_daemon)
                p = subprocess.run([".\chia.exe","plots","check","-n",str(parametros.check_plot_nro_proof),"-g",f"{plots_por_analizar[plot]['ruta']}\{plot}"], capture_output=True)
                proofs = bytes(parametros.check_plot_nro_proof)
                fndproof = p.stderr.decode().find("/ "+str(parametros.check_plot_nro_proof)+",")
                nro_pruebas=int(p.stderr[fndproof-3:fndproof-1].decode())
                            
                assert os.path.isdir(parametros.ruta_actual)
                os.chdir(parametros.ruta_actual)
                print(f"Cantidad de pruebas: {nro_pruebas}/{parametros.check_plot_nro_proof}: {nro_pruebas/parametros.check_plot_nro_proof}")
                nro_pruebas_check=nro_pruebas
                if nro_pruebas/parametros.check_plot_nro_proof<0.7:
                    mensaje_check=f"\n 🔴 Pruebas analizadas: {nro_pruebas}/{parametros.check_plot_nro_proof}: {nro_pruebas/parametros.check_plot_nro_proof}"
                elif nro_pruebas/parametros.check_plot_nro_proof>=0.7 and nro_pruebas/parametros.check_plot_nro_proof<1:
                    mensaje_check=f"\n 🟡 Pruebas analizadas: {nro_pruebas}/{parametros.check_plot_nro_proof}: {nro_pruebas/parametros.check_plot_nro_proof}"
                elif nro_pruebas/parametros.check_plot_nro_proof>=1 and nro_pruebas/parametros.check_plot_nro_proof<1.1:
                    mensaje_check=f"\n 🟢 Pruebas analizadas: {nro_pruebas}/{parametros.check_plot_nro_proof}: {nro_pruebas/parametros.check_plot_nro_proof}"
                elif nro_pruebas/parametros.check_plot_nro_proof>=1.1:
                    mensaje_check=f"\n 🌟 Pruebas analizadas: {nro_pruebas}/{parametros.check_plot_nro_proof}: {nro_pruebas/parametros.check_plot_nro_proof}"
            else:
                mensaje_check=""
                nro_pruebas_check=""
            for i in plot_status:
                if i['PlotName'][i['PlotName'].find("plot-k"):i['PlotName'].find("plot-k")+90]==plot[0:90]:
                    info_log=True
                    if parametros.aviso_telegram==True:
                        mensaje=f"""🚜🧑‍🌾 Acaba de finalizar el plot 🍃{plot[26:32]}🍃 
Tiempo Total: {i['TotalSeconds']}
⏱️ Fase 1: {i['Phase1Seconds']}
⏱️ Fase 2: {i['Phase2Seconds']}
⏱️ Fase 3: {i['Phase3Seconds']}
⏱️ Fase 4: {i['Phase4Seconds']}
⏱️ Fase 5: {i['CopyTimeSeconds']} 
{mensaje_check}"""                       
                        print(mensaje)
                        parametros.bot.send_message(parametros.chat_id, mensaje)
                        fecha_not=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    else:
                        fecha_not=""
                    plots_analizados.setdefault(plot, {
                    "archivo": plot,
                    "alias":plot[26:32],
                    "ruta":plots_por_analizar[plot]["ruta"],
                    "t_fase1":i['Phase1Seconds'],
                    "t_fase2":i['Phase2Seconds'],
                    "t_fase3":i['Phase3Seconds'],
                    "t_fase4":i['Phase4Seconds'],
                    "t_fase5":i['CopyTimeSeconds'],
                    "t_total":i['TotalSeconds'],
                    "Ram":i['Buffer'],
                    "Threads":i['Threads'],
                    "pruebas_aprobadas":nro_pruebas_check,
                    "fecha_notificacion":fecha_not,
                    "fecha_creacion":plots_por_analizar[plot]["fecha_creacion"],
                    "fecha_registro":datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                })
            if info_log==False:
                if parametros.aviso_telegram==True:
                    mensaje=f"🚜🧑‍🌾 Acaba de finalizar el plot 🍃{plot[26:32]}🍃 \n Sin información de logs {mensaje_check}"                       
                    print(mensaje)
                    parametros.bot.send_message(parametros.chat_id, mensaje)
                    fecha_not=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                else:
                    fecha_not=""
                plots_analizados.setdefault(plot, {
                "archivo": plot,
                "alias":plot[26:32],
                "ruta":plots_por_analizar[plot]["ruta"],
                "t_fase1":"",
                "t_fase2":"",
                "t_fase3":"",
                "t_fase4":"",
                "t_fase5":"",
                "t_total":"",
                "Ram":"",
                "Threads":"",
                "pruebas_aprobadas":nro_pruebas_check,
                "fecha_notificacion":fecha_not,
                "fecha_creacion":plots_por_analizar[plot]["fecha_creacion"],
                "fecha_registro":datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            })
            #print(f"fin plot: {plot}")
        with open("data/registro_plots.json", 'w') as outfile:
            json.dump(plots_analizados, outfile, indent=3)

def resumen_diario():
    proofs=0
    with open("data/registro_plots.json", 'r') as json_file:
        plots_analizados = json.load(json_file)
    plots_nuevos=0
    for key, valor in plots_analizados.items():
        proofs=proofs+plots_analizados[key]['pruebas_aprobadas']
        a=plots_analizados[key]['pruebas_aprobadas']/parametros.check_plot_nro_proof
        #print(plots_analizados[key]['fecha_creacion'], (datetime.now()- datetime.fromtimestamp(time.mktime(datetime.strptime(plots_analizados[key]['fecha_creacion'],"%d/%m/%Y %H:%M:%S").timetuple()))).total_seconds()<=24*60*60)
        if (datetime.now()- datetime.fromtimestamp(time.mktime(datetime.strptime(plots_analizados[key]['fecha_creacion'],"%d/%m/%Y %H:%M:%S").timetuple()))).total_seconds()<=24*60*60:
            plots_nuevos=plots_nuevos+1
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

    Total plots: {len(plots_analizados)}
    Plots nuevos últimas 24 horas: {plots_nuevos} 
    Calidad plots: {mensaje_check} (revisa /plots para mayor detalle)
    """
    parametros.bot.send_message(parametros.chat_id, mensaje)
    print(mensaje)
