from WIFIdecouv import GetDSignal

def Trier_AP():
  WifiList= GetDSignal()
  sorted_wifi = sorted(
    WifiList,
    key=lambda t: int(t[1].strip()) if (t[1] and t[1].strip().isdigit()) else -999,
    reverse=True)
  out = f"\nLe point d'accès ayant le signal le plus puissant est : {sorted_wifi[0][0]} avec une puissance de signal de {sorted_wifi[0][1]} %"
  final=out + "\n\n" + "Liste des points d'accès triés par puissance de signal (du plus fort au plus faible):\n\n"
  for ssid, signal in sorted_wifi:
      final += f"\nSSID: {ssid}, Signal: {signal} %\n"
  return final


  

