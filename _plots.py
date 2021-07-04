import parametros
from datetime import datetime,  time
import time
import json
import matplotlib.pyplot as plt
import pyautogui


############## Registra plots creados en directorio ##############
def bot_plots():
    with open("data/registro_plots.json", 'r') as json_file:
        plots_analizados = json.load(json_file)
    cont_1=cont_2=cont_3=cont_4=0
    for key, valor in plots_analizados.items():
        a=plots_analizados[key]['pruebas_aprobadas']/parametros.check_plot_nro_proof
        if a<=0.7:
            cont_1=cont_1+1
        elif a>0.7 and a<=1:
            cont_2=cont_2+1
        elif a>1 and a<=1.1:
            cont_3=cont_3+1
        elif a>1.1:
            cont_4=cont_4+1

    # Data to plot
    labels = 'Malo [∞ - 0,7]', 'Regular [0,7 - 1]', 'Bueno [1 - 1,1]', 'Excelente [1,1 - ∞]'
    sizes = [cont_1, cont_2, cont_3, cont_4]
    colors = ['red', 'yellow', 'green', 'lightskyblue']
    explode = (0.1, 0, 0, 0)  # explode 1st slice

    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')
    plt.savefig('img/distr_calidad_plots.png')
    parametros.bot.send_photo(parametros.chat_id, photo=open('img/distr_calidad_plots.png', 'rb'))
    if cont_1>0:
        parametros.bot.send_message(parametros.chat_id, f"Tienes {cont_1} plots de baja calidad.\nUsa el comando /recomendacion para conocer más detalles.")

def bot_recomendacion():
    with open("data/registro_plots.json", 'r') as json_file:
        plots_analizados = json.load(json_file)
    cont_1=0
    mensaje_rec=""
    parametros.bot.send_message(parametros.chat_id, f"Tienes 1 o más plot(s) de baja calidad. Es recomendable eliminarlo(s) y crear nuevo(s) plot(s) en su lugar")

    for key, valor in plots_analizados.items():
        a=plots_analizados[key]['pruebas_aprobadas']/parametros.check_plot_nro_proof
        if a<=0.7:
            cont_1=cont_1+1
            mensaje_rec= f"Plot: {plots_analizados[key]['alias']} \n Puntaje: {round(a,3)} \n Fecha creación: {plots_analizados[key]['fecha_creacion']}"
            parametros.bot.send_message(parametros.chat_id, mensaje_rec)


def bot_estado_granja():
    parametros.bot.send_photo(parametros.chat_id, photo=open('img/estado_harvester.png', 'rb'))
def bot_analisis_log():
    parametros.bot.send_photo(parametros.chat_id, photo=open('img/analisis_log.png', 'rb'))
def bot_ver_pantalla():
# Capturar pantalla.
    screenshot = pyautogui.screenshot()
# Guardar imagen.
    screenshot.save("img/screenshot.png")
    parametros.bot.send_photo(parametros.chat_id, photo=open('img/screenshot.png', 'rb'))