import parametros
import time
from datetime import datetime
import funciones
import schedule
import json



def main():
    parametros.bot.send_message(parametros.chat_id, "🚜 Plotter activado 🧑‍🌾\n Si tienes alguna consulta, usa el comando /help")
    #echo_bot.echo_bot()
    if parametros.aviso_diario==True:
        parametros.bot.send_message(parametros.chat_id, f"🚜 Enviará un reporte cada día a las {parametros.aviso_diario_hora} horas(s)")
        for hora in parametros.aviso_diario_hora:
            schedule.every().day.at(f"{'{:02d}'.format(hora)}:00").do(funciones.resumen_diario)
                    

    if parametros.aviso_plots_nuevos==True:
        parametros.bot.send_message(parametros.chat_id, f"🚜 Se verificarán plots nuevos cada {parametros.min_busq} minuto(s)")
        schedule.every(parametros.min_busq).minutes.do(funciones.validar_plots_nuevos)
    print(schedule.get_jobs())
    while True:
        schedule.run_pending()
        time.sleep(1)
    
if __name__ == "__main__":
    main()
