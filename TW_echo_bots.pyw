from numpy import true_divide
import parametros
import _plots
import telebot
import funciones

    #parametros.bot.send_message(parametros.chat_id, "🚜 Plotter activado 🧑‍🌾\n Si tienes alguna consulta, usa el comando /help")

bot = telebot.TeleBot(parametros.token_bot)
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, """Hola, las funciones disponibles son: 
/resumen_diario -> Análisis de las últimas 24 horas de tu granja
/plots -> Conoce el estado de tus plots
/plots_nuevos -> Analiza si existen plots nuevos
/estado_granja -> Conoce la salud de conexión de la granja
/analisis_log -> Conoce el comportamiento de los archivos log de la última hora
/ver_pantalla -> obten una captura de pantalla de la granja
""")

@bot.message_handler(commands=['plots'])
def send_welcome(message):
    bot.reply_to(message, "La distribución de calidad de tus plots es la siguiente (dale unos segundos):")
    _plots.bot_plots()
@bot.message_handler(commands=['recomendacion'])
def send_welcome(message):
    _plots.bot_recomendacion()
@bot.message_handler(commands=['resumen_diario'])
def send_welcome(message):
    funciones.resumen_diario()	
@bot.message_handler(commands=['plots_nuevos'])
def send_welcome(message):
    funciones.validar_plots_nuevos()
    if parametros.zero_plots_nuevos==True:
        parametros.zero_plots_nuevos=False
        bot.reply_to(message, "No se encontraron nuevos plots")
@bot.message_handler(commands=['estado_granja'])
def send_welcome(message):
    _plots.bot_estado_granja()
@bot.message_handler(commands=['analisis_log'])
def send_welcome(message):
    _plots.bot_analisis_log()
@bot.message_handler(commands=['ver_pantalla'])
def send_welcome(message):
    _plots.bot_ver_pantalla()					
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)
bot.polling()

