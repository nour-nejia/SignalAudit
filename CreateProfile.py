# CreateProfile.py
import re, tempfile, os, time
from xml.sax.saxutils import escape
import tkinter as tk
from tkinter import simpledialog
from WIFIdecouv import read_data_from_cmd  # réutilise ta fonction (décodage cp1252 etc.)

def _default_profile_exists(ssid: str) -> bool:
    """Fallback minimal check (utilisé si tu ne fournis pas profile_exists_fn)."""
    if not ssid:
        return False
    out = read_data_from_cmd('netsh wlan show profiles') or ''
    out = out.replace('\r\n', '\n').replace('\r', '\n')
    # recherche simple : ligne contenant "Profile" ou "Profil"
    for line in out.splitlines():
        if ':' in line and ('profile' in line.lower() or 'profil' in line.lower()):
            parts = line.split(':', 1)
            name = parts[1].strip()
            if name and name == ssid:
                return True
    return False

def _make_profile_xml(ssid: str, password: str) -> str:
    ss = escape(ssid); pw = escape(password)
    return f'''<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
  <name>{ss}</name>
  <SSIDConfig><SSID><name>{ss}</name></SSID></SSIDConfig>
  <connectionType>ESS</connectionType>
  <connectionMode>manual</connectionMode>
  <MSM>
    <security>
      <authEncryption>
        <authentication>WPA2PSK</authentication>
        <encryption>AES</encryption>
        <useOneX>false</useOneX>
      </authEncryption>
      <sharedKey>
        <keyType>passPhrase</keyType>
        <protected>false</protected>
        <keyMaterial>{pw}</keyMaterial>
      </sharedKey>
    </security>
  </MSM>
</WLANProfile>
'''

def _add_profile_via_netsh(ssid: str, password: str, overwrite: bool=False):
    """Ajoute le profil via XML temporaire. Retourne (True, out) ou (False, err)."""
    tmp = None
    try:
        if overwrite:
            try:
                read_data_from_cmd(f'netsh wlan delete profile name="{ssid}"')
            except Exception:
                pass
        xml = _make_profile_xml(ssid, password)
        tmp = tempfile.NamedTemporaryFile('w', delete=False, suffix='.xml', encoding='utf-8')
        tmp.write(xml); tmp.close()
        out = read_data_from_cmd(f'netsh wlan add profile filename="{tmp.name}" user=current')
        return True, out
    except Exception as e:
        return False, f"Erreur add_profile: {e}"
    finally:
        try:
            if tmp is not None:
                os.unlink(tmp.name)
        except Exception:
            pass

def _get_interface_state():
    out = read_data_from_cmd('netsh wlan show interfaces') or ''
    out = out.replace('\r\n', '\n').replace('\r', '\n')
    res = {}
    m_ssid = re.search(r'(?mi)^\s*SSID\s*:\s*(.+)$', out, re.MULTILINE)
    m_state = re.search(r'(?mi)^\s*(?:State|État|Etat)\s*:\s*(.+)$', out, re.MULTILINE)
    if m_ssid: res['SSID'] = m_ssid.group(1).strip()
    if m_state: res['State'] = m_state.group(1).strip().lower()
    return res

def _connect_and_wait(ssid: str, timeout: int=12):
    """Lance netsh connect puis poll l'interface. Retourne (True,msg) ou (False,msg)."""
    out = read_data_from_cmd(f'netsh wlan connect name="{ssid}"')
    t0 = time.time()
    while time.time() - t0 < timeout:
        st = _get_interface_state()
        state = st.get('State','')
        if state and ('connect' in state or 'connecté' in state or 'connected' in state):
            cur = st.get('SSID','')
            if cur and cur.strip() == ssid.strip():
                return True, f"Connecté à {ssid}."
        time.sleep(0.6)
    return False, f"Timeout connexion. netsh output:\n{out}"

def _ask_password_simpledialog(prompt_text: str, parent=None):
    """Affiche un simpledialog.askstring au premier plan sans mettre la GUI en topmost.

    Technique: on crée une petite fenêtre Toplevel "ancre" (topmost) qui sert de parent
    au simpledialog. Ainsi, seul le dialog est au-dessus, jamais la fenêtre principale.
    """
    temp_root = None  # root créé si aucun parent n'est fourni
    anchor = None     # Toplevel ancre topmost
    try:
        base_parent = parent
        if base_parent is None:
            # Crée un root invisible si aucun parent n'est fourni
            temp_root = tk.Tk()
            temp_root.withdraw()
            base_parent = temp_root

        # Crée une Toplevel ancre, topmost, quasi invisible
        anchor = tk.Toplevel(base_parent)
        # Transient pour rester liée à la fenêtre de base (si fournie)
        try:
            anchor.transient(base_parent)
        except Exception:
            pass
        # Rendre l'ancre topmost (pas la fenêtre principale)
        try:
            anchor.attributes('-topmost', True)
        except Exception:
            pass
        # La rendre minimalement visible ou invisible
        try:
            anchor.attributes('-alpha', 0.0)  # invisible si supporté
        except Exception:
            # Fallback: rétrécir et déplacer
            try:
                anchor.geometry('1x1+0+0')
            except Exception:
                pass
        # Placer l'ancre au centre de la fenêtre parente (ou de l'écran)
        try:
            base_parent.update_idletasks()
            # Si la fenêtre de base est visible, centrer par rapport à elle
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

        # S'assurer qu'elle est mappée avant d'ouvrir le dialog
        try:
            anchor.deiconify()
            anchor.lift()
            anchor.update_idletasks()
        except Exception:
            pass

        # Ouvre le dialog avec l'ancre comme parent (le dialog sera au-dessus)
        res = simpledialog.askstring("Mot de passe", prompt_text, show='*', parent=anchor)
        return res
    finally:
        # Détruit l'ancre et, si créé, le root temporaire
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

# -------------------------
# Fonction publique demandée
# -------------------------
def create_profile_and_connect(
    ssid: str,
    prompt_password_fn=None,
    max_attempts: int = 5,
    profile_exists_fn=None,
    parent_for_dialog=None,
    overwrite=False
):
    """
    ssid: chaîne (nom du réseau)
    prompt_password_fn: callable(prompt_text)->str|None. Si None, on utilisera simpledialog (parent_for_dialog peut être ton CTk root).
    max_attempts: int|None (None = infini)
    profile_exists_fn: callable(ssid)->bool (si tu veux réutiliser ta fonction existante)
    parent_for_dialog: passe ton root CTk si tu veux que le dialog soit modal à ton app
    overwrite: si True supprime profil existant avant ajout

    Retour: (True, message) ou (False, message). Si utilisateur annule -> retourne (False, "utilisateur a annulé l'opération")
    """
    if not ssid:
        return False, "SSID vide."

    exists_fn = profile_exists_fn or _default_profile_exists

    # si profil existe -> tente connexion directe
    try:
        if exists_fn(ssid) and not overwrite:
            ok, msg = _connect_and_wait(ssid)
            return ok, msg
    except Exception as e:
        # si check échoue, on continue pour tenter la création
        pass

    attempts = 0
    while True:
        if max_attempts is not None and attempts >= max_attempts:
            return False, f"Nombre maximal de tentatives ({max_attempts}) atteint."
        attempts += 1

        # obtenir mot de passe
        if prompt_password_fn:
            pwd = prompt_password_fn(f"Entrez le mot de passe pour '{ssid}' (tentative {attempts})")
        else:
            pwd = _ask_password_simpledialog(f"Entrez le mot de passe pour '{ssid}' (tentative {attempts})", parent=parent_for_dialog)

        if pwd is None:
            return False, "utilisateur a annulé l'opération"

        # essayer d'ajouter le profil
        ok_add, out_add = _add_profile_via_netsh(ssid, pwd, overwrite=overwrite)
        if not ok_add:
            # échec ajout : on boucle (tu peux afficher out_add via ta GUI si besoin)
            try: read_data_from_cmd(f'netsh wlan delete profile name="{ssid}"')
            except Exception: pass
            continue

        # profil ajouté -> tenter connexion
        ok_conn, out_conn = _connect_and_wait(ssid)
        if ok_conn:
            return True, f"Profil ajouté et connecté: {ssid}\n{out_conn}"
        else:
            # suppression profil et nouvelle boucle
            try: read_data_from_cmd(f'netsh wlan delete profile name="{ssid}"')
            except Exception: pass
            continue

def create_profile(
    ssid: str,
    password: str,
    timeout: int = 12,
    cleanup: bool = True,
    retries: int = 4,
    parent_for_dialog=None,
):
    """
    Crée un profil pour (ssid, password), tente la connexion, et retourne (True, msg) ou (False, msg).
    - ssid: nom du réseau
    - password: mot de passe clair WPA2-PSK
    - timeout: secondes d'attente pour la confirmation de connexion
    - cleanup: si True, supprime le profil ajouté en cas d'échec de connexion
    """
    if not ssid:
        return False, "SSID vide"
    if password is None or str(password).strip() == "":
        return False, "Mot de passe vide"

    # 1) Premier essai avec le mot de passe fourni
    ok_add, add_out = _add_profile_via_netsh(ssid, password, overwrite=False)
    if ok_add:
        conn_out = read_data_from_cmd(f'netsh wlan connect name="{ssid}"') or ''
        ok_conn, msg = _connect_and_wait(ssid, timeout=timeout)
        if ok_conn:
            return True, f"Profil ajouté et connecté: {ssid}\n{msg}"
        # échec connexion -> cleanup avant nouvelle tentative
        if cleanup:
            try:
                read_data_from_cmd(f'netsh wlan delete profile name="{ssid}"')
            except Exception:
                pass
        last_error = (
            f"Échec connexion pour {ssid} : {msg}\n"
            f"(add output):\n{add_out}\n"
            f"(connect output):\n{conn_out}"
        )
    else:
        # impossible d'ajouter le profil dès le départ
        last_error = add_out

    # 2) Boucle de réessais via simpledialog (si retries > 0)
    attempts = 0
    while attempts < max(0, retries):
        attempts += 1
        prompt = f"Entrez le mot de passe pour '{ssid}' (tentative {attempts}/{retries})"
        new_pwd = _ask_password_simpledialog(prompt, parent=parent_for_dialog)
        if new_pwd is None:
            return False, "Connexion annulée par l'utilisateur."
        ok_add, add_out = _add_profile_via_netsh(ssid, new_pwd, overwrite=False)
        if not ok_add:
            # réessayer à l'itération suivante
            last_error = add_out
            continue
        conn_out = read_data_from_cmd(f'netsh wlan connect name="{ssid}"') or ''
        ok_conn, msg = _connect_and_wait(ssid, timeout=timeout)
        if ok_conn:
            return True, f"Profil ajouté et connecté: {ssid}\n{msg}"
        # sinon échec -> supprimer profil et réessayer
        if cleanup:
            try:
                read_data_from_cmd(f'netsh wlan delete profile name="{ssid}"')
            except Exception:
                pass
        last_error = (
            f"Échec connexion pour {ssid} : {msg}\n"
            f"(add output):\n{add_out}\n"
            f"(connect output):\n{conn_out}"
        )

    # 3) Toutes les tentatives ont échoué
    return False, last_error
