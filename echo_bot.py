import telebot
import _plots
import funciones
def echo_bot():
	bot = telebot.TeleBot("1842675017:AAEY-RLslqtlCdwFK80pyjQdkT3EyitLe8k")
	@bot.message_handler(commands=['help'])
	def send_welcome(message):
		bot.reply_to(message, """Hola, las funciones disponibles son: 
/plots -> Conoce el estado de tus plots
/resumen_diario -> Análisis de las últimas 24 horas de tu granja
/plots_nuevos -> Analiza si existen plots nuevos
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
	@bot.message_handler(commands=['estado_granja'])
	def send_welcome(message):
		_plots.bot_estado_granja()				
	@bot.message_handler(func=lambda message: True)
	def echo_all(message):
		bot.reply_to(message, message.text)
	bot.polling()

if __name__ == "__main__":
    echo_bot()