from WIFIdecouv import GetDSignal
from ReadFromCmd import read_data_from_cmd
from tkinter import messagebox, simpledialog
import tkinter as tk
import re 
from CreateProfile import create_profile

#cette fonction elle permet d'afficher la boite de dialogue au centre et on top 
def _ask_password_topmost(prompt_text: str, parent=None):
  """Show a password simpledialog on top using a transient, invisible Toplevel anchor.
  Returns the entered string or None if cancelled.
  """
  temp_root = None
  anchor = None
  try:
    base_parent = parent
    if base_parent is None:
      temp_root = tk.Tk()
      temp_root.withdraw()
      base_parent = temp_root
    anchor = tk.Toplevel(base_parent)
    try:
      anchor.transient(base_parent)
    except Exception:
      pass
    try:
      anchor.attributes('-topmost', True)
    except Exception:
      pass
    try:
      anchor.attributes('-alpha', 0.0)
    except Exception:
      try:
        anchor.geometry('1x1+0+0')
      except Exception:
        pass
    try:
      anchor.deiconify()
      anchor.lift()
      anchor.update_idletasks()
    except Exception:
      pass
    # Position the anchor at the center of the parent (or screen) so dialog centers
    try:
      base_parent.update_idletasks()
      if hasattr(base_parent, 'winfo_viewable') and base_parent.winfo_viewable():
        px, py = base_parent.winfo_rootx(), base_parent.winfo_rooty()
        pw, ph = base_parent.winfo_width(), base_parent.winfo_height()
        cx = px + (pw // 2)
        cy = py + (ph // 2)
      else:
        sw, sh = anchor.winfo_screenwidth(), anchor.winfo_screenheight()
        cx, cy = (sw // 2), (sh // 2)
      anchor.geometry(f"1x1+{cx}+{cy}")
    except Exception:
      pass
    return simpledialog.askstring("Mot de passe requis", prompt_text, show='*', parent=anchor)
  finally:
    if anchor is not None:
      try:
        anchor.destroy()
      except Exception:
        pass
    if temp_root is not None:
      try:
        temp_root.destroy()
      except Exception:
        pass

#cette fonction controle la connexion au meilleur AP
def connect(parent=None):
  WifiList= GetDSignal()
  sorted_wifi = sorted(
  WifiList,
  key=lambda t: int(t[1].strip()) if (t[1] and t[1].strip().isdigit()) else -999,
  reverse=True)
  best_ssid = sorted_wifi[0][0]
  saved_Profiles= read_data_from_cmd("netsh wlan show profiles")
  text = saved_Profiles.replace('\r\n', '\n').replace('\r', '\n').replace('’', "'")
  pattern = r"(?mi)^\s*(?:Profil\s+d['’]utilisateur\s+actuel|Profil\s+Tous\s+les\s+utilisateurs|Current\s+User\s+Profile|All\s+User\s+Profile)\s*:\s*(.+)$"
  ssid_list = [m.strip() for m in re.findall(pattern, text)]
  ssid_list = list(dict.fromkeys(ssid_list))
  print(ssid_list)
  if best_ssid in ssid_list:
    out=read_data_from_cmd(f'netsh wlan connect name="{best_ssid}"')
    return out
  else:
    pwd = _ask_password_topmost(
      f"Entrez le mot de passe pour SSID {best_ssid}: \n Vous avez 5 tentatives \n Après votre saisie attendez le temps de configuration.\n",
      parent=parent,
    )
    if pwd is None:
        messagebox.showinfo("Annulé", "Vous avez annulé la saisie.")
        return "Connexion annulée par l'utilisateur."
    ok, msg = create_profile(best_ssid, pwd, timeout=12, cleanup=True, retries=4, parent_for_dialog=parent)
    if ok:
        return msg
    else:
        messagebox.showerror("Échec", msg)
        return msg
