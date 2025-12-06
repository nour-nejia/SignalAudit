import re 
from ReadFromCmd import read_data_from_cmd

def InfoAP():
  out=read_data_from_cmd("netsh wlan show interfaces")
  return out

def GetMySignal():
  out=InfoAP()
  m = re.search(r'Signal.*?:.*?([0-9]*)%', out)
  if m:
      signal_strength = int(m.group(1))
  else:
      signal_strength = None

  return signal_strength
