from ast import pattern
import subprocess
import re
from ReadFromCmd import read_data_from_cmd
import numpy as np



def AllDSignalsInfo():
    out = read_data_from_cmd("netsh wlan show networks mode=bssid")
    print(out)
    return out

def GetDSignal():
    out = read_data_from_cmd('netsh wlan show networks mode=bssid | findstr "SSID Signal"')
    ssid_blocks = re.findall(r'(?m)^\s*SSID\s+\d+\s*:\s*(.*)$', out)
    ssid_blocks = [s.strip() for s in ssid_blocks if s.strip()]
    signal_blocks = re.findall(r'Signal.*?:.*?([0-9]*)%', out)
    print(ssid_blocks)
    print (signal_blocks)
    result = list(zip(ssid_blocks, signal_blocks))
    print(result)
    WifiList= [t for t in result if "BSSID" not in t[0]]
    print(WifiList)
    return WifiList
