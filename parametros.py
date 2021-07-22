import telebot
import pathlib
import os



## Ingresar paratmetros ##
# --- Telegram ---

token_bot="1842675017:AAEY-RLslqtlCdwFK80pyjQdkT3EyitLe8k"
chat_id="-599355307"
#chat_id="-599355307" 1567062024

# --- ubicación carpetas farmeo ---
path = ["C:\Plots","E:\Plots","F:\Plots","G:\Plots","H:\Plots"]
blockchain={'Chia':{"C:\\Plots","E:\\Plots","F:\\Plots","G:\\Plots","H:\\Plots"}, 
'Signum':{'E:\\Plots Signum\\NW','I:\\plots_signum'}, 
'Temporales':{'D:\\Plots'}}




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

#"app-1.1.7"
version_chia="app-1.2.2"
finger_print="3571905713"
ruta_log_signum=r"C:\Users\gesti\Downloads\BTDEX\log\btdex.log"
ruta_log_bhd=fr"C:\Users\{os.getlogin()}\.config\foxy-miner\logs\foxy-miner.log"
ruta_daemon=f"C:\\Users\\{os.getlogin()}\\AppData\Local\chia-blockchain\\{version_chia}\\resources\\app.asar.unpacked\\daemon"  
ruta_actual=str(pathlib.Path().absolute()).replace('\\','\\\\')+'\\\\'  
bot = telebot.TeleBot(token_bot)
zero_plots_nuevos=False
