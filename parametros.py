import telebot
import pathlib
import os



## Ingresar paratmetros ##
# --- Telegram ---
token_bot="1842675017:AAEOrbcCcdjUjA2RHJIkdExDOcYWip9mx24"
chat_id="-599355307"
#chat_id="-599355307" 1567062024

# --- ubicación carpetas farmeo ---
path = ["C:\CHIA","E:\Plots"]
blockchain={'Chia':{'C:\\CHIA\\', 'E:\\Plots\\'}, 
'Signum':{'E:\\Plots Signum\\'}, 
'Temporales':{'E:\\Plotter', 'F:\\Plots','D:\\Plots', 'C:\\Plots'}}




aviso_telegram=True
check_plot=True
# -- obsoletos---
"""min_busq=1
aviso_plots_nuevos=True
aviso_diario=True
aviso_diario_hora=[23,00]
"""
check_plot_nro_proof=50

#---- Funcionamiento ----


version_chia="app-1.1.7"
ruta_daemon=f"C:\\Users\\{os.getlogin()}\\AppData\Local\chia-blockchain\\{version_chia}\\resources\\app.asar.unpacked\\daemon"  
ruta_actual=str(pathlib.Path().absolute()).replace('\\','\\\\')+'\\\\'  
bot = telebot.TeleBot(token_bot)
zero_plots_nuevos=False
