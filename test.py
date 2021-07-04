import json
import os
import parametros
cmd = f"\"C:\\Program Files (x86)\\ChiaPlotStatus\\ChiaPlotStatus\\ChiaPlotStatusCli.exe\" -o {parametros.ruta_actual}\data\chia_plot_status.json -f json"
print(cmd)
#if os.path.isfile(f"data/registro_log1.json")==False: open(f"data/registro_log1.json","w").close()
#with open("data/registro_log1.json", 'r') as json_file:
#        log = json.load(json_file)