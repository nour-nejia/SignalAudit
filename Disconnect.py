from ReadFromCmd import read_data_from_cmd
def disconnect():
  out=read_data_from_cmd("netsh wlan disconnect")
  if len(out)==0:
    return"L'interface wi-fi est déja non connectée à aucun point d'accès"
  return out 