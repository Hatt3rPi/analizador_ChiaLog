print("Iniciando análisis de log")
from time import process_time 
t1=process_time()
import re
from datetime import datetime,timedelta
from file_read_backwards import FileReadBackwards
import json
import plotly.graph_objs as go
from plotly.subplots import make_subplots
# Libraries
import matplotlib.pyplot as plt
import pandas as pd
from math import pi
import parametros
from telebot import types
import numpy as np
import os

def grafico_log():
    log={}
    if os.path.isfile("data/registro_log.json")==False: open("data/registro_log.json","w").close()
    with open("data/registro_log.json", 'r') as json_file:
        log = json.load(json_file)
    #print(log['chia']['INFO']['harvester']['chia.harvester.harvester']['contador'])
    # Set data
    
    labels= ['full_node.full_node','full_node.mempool_manager']
    chia= [log['chia']['INFO']['full_node']['chia.full_node.full_node']['contador'], log['chia']['INFO']['full_node']['chia.full_node.mempool_manager']['contador']]
    chaingreen= [log['chaingreen']['INFO']['full_node']['chaingreen.full_node.full_node']['contador'], log['chaingreen']['INFO']['full_node']['chaingreen.full_node.mempool_manager']['contador']]
    flax= [log['flax']['INFO']['full_node']['flax.full_node.full_node']['contador'], log['flax']['INFO']['full_node']['flax.full_node.mempool_manager']['contador']]
    spare= [log['spare-blockchain']['INFO']['full_node']['spare.full_node.full_node']['contador'], log['spare-blockchain']['INFO']['full_node']['spare.full_node.mempool_manager']['contador']]
    
    x = np.arange(len(labels))  # the label locations
    width = 0.15  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - 2*width, chia, width, label='chia')
    rects2 = ax.bar(x - width, chaingreen, width, label='chaingreen')
    rects3 = ax.bar(x , flax, width, label='flax')
    rects4 = ax.bar(x + width, spare, width, label='spare')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    ax.bar_label(rects3, padding=3)
    ax.bar_label(rects4, padding=3)

    fig.tight_layout()

    plt.show()

    #plt.savefig('img/test.png')


if __name__ == "__main__":
    grafico_log()

