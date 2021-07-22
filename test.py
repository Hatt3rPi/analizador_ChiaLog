import parametros
from datetime import datetime, time
import time
import json
import shutil
import string
from ctypes import windll
import os
import pandas as pd
from pandas.core.indexes.base import Index
from tabulate import tabulate
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import requests
import websocket
import numpy as np
import asyncio

def actualiza_wallet_bhd():
    wallets={}
    balances={}
    try:   
        ws = websocket.WebSocket()
        ws.connect("wss://api.foxypool.io/socket.io/?EIO=4&transport=websocket")
        print(ws)
        
        greeting = ws.recv()
        print(f"< {greeting}")
        
        ws.close()
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e,"excepcion")

if __name__ == '__main__':
    actualiza_wallet_bhd()

