import json
import os
import parametros

if os.path.isfile(f"data/registro_log1.json")==False: open(f"data/registro_log1.json","w").close()
#with open("data/registro_log1.json", 'r') as json_file:
#        log = json.load(json_file)