import telebot
import pathlib
import os

## Ingresar paratmetros ##
# --- Telegram ---
token_bot=""
chat_id=""


# --- ubicación carpetas farmeo ---
path = [""]
blockchain={'Chia':{'', ''}, 
'Signum':{''}, 
'Temporales':{''}}

aviso_telegram=True
check_plot=True
check_plot_nro_proof=50

#---- Funcionamiento ----

version_chia="app-1.1.7"
ruta_daemon=f"C:\\Users\\{os.getlogin()}\\AppData\Local\chia-blockchain\\{version_chia}\\resources\\app.asar.unpacked\\daemon"  
ruta_actual=str(pathlib.Path().absolute()).replace('\\','\\\\')+'\\\\'  
bot = telebot.TeleBot(token_bot)
zero_plots_nuevos=False
