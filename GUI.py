import matplotlib
from matplotlib import pyplot as plt  
import customtkinter as ctk 
from WIFIdecouv import AllDSignalsInfo
from AnalyseAP import InfoAP
from BestAP import Trier_AP 
from CourbeAP import  start_update
from WIFIdecouv_courbe import start_updateALL
from CourbeAP import start_update, stop_update
from Disconnect import disconnect
from ConnectToBest import connect 
from WIFIdecouv_courbe import start_updateALL, stop_updateALL

matplotlib.use('TkAgg')

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue") 

# Fenêtre principale
root = ctk.CTk()
root.title("Analyseur et capteur wifi ")
root.update_idletasks()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")

# Cadre principal
main_frame = ctk.CTkFrame(root, corner_radius=25, fg_color="#FFFFFF")  
main_frame.pack(fill="both", expand=True)

# Barre latérale
# --- Barre d'outils en haut (toolbar) ---
toolbar = ctk.CTkFrame(main_frame, height=60, fg_color="transparent")
toolbar.pack(side="top", fill="x", padx=10, pady=(10, 0))

# Frame gauche pour les actions principales
toolbar_left = ctk.CTkFrame(toolbar, fg_color="transparent")
toolbar_left.pack(side="left", anchor="w", padx=(10, 0))


# Frame droit pour affichage courbes  
toolbar_right = ctk.CTkFrame(toolbar, fg_color="transparent")
toolbar_right.pack(side="right", anchor="e", padx=(0, 10))


center_frame = ctk.CTkFrame(main_frame, corner_radius=20, fg_color="#FDFDFD")  
center_frame.pack(side="left", fill="both", expand=True, padx=25, pady=25)

# Titre
welcome_label = ctk.CTkLabel(
    center_frame,
    text="Bienvenue dans notre inspecteur Wi‑Fi",
    font=ctk.CTkFont(size=40, weight="bold"),
    text_color="#000000"
)

welcome_label.pack(pady=(40, 30))

# Zone d'affichage des résultats
result_text = ctk.CTkTextbox(center_frame, height=250, font=("Consolas", 14), wrap="word")
result_text.pack(fill="both", expand=True, padx=40, pady=(0, 30))
result_text.insert("end", "\nRésultats et messages s'afficheront ici...")

#style des boutons de courbes
ONE_style = {
    "font": ctk.CTkFont(size=16),
    "fg_color": "#D60000",
    "hover_color": "#D60000",
    "text_color": "white",
    "corner_radius": 8,
    "height": 40,
    "width": 90
}
ALL_style = {
    "font": ctk.CTkFont(size=16),
    "fg_color":  "#0414F6",
    "hover_color": "#0414F6",
    "text_color": "white",
    "corner_radius": 8,
    "height": 40,
    "width": 90
}

# boutons d'affichage courbes création 
btn_ALL = ctk.CTkButton(
    toolbar_right,
    text="▶ Tous les AP",
    command=lambda: root.after(0, start_updateALL),
    **ALL_style
)
btn_ALL.pack(side="left", padx=6, pady=10)

btn_ONE = ctk.CTkButton(
    toolbar_right,
    text="▶ AP Connecté",
    command=lambda: root.after(0, start_update),
    **ONE_style
)
btn_ONE.pack(side="left", padx=6, pady=10)

# les fonctions qui controlent les actions des boutons principaux ( ceux des diff fonctionnalités )
def DiscoverAP():
    data= AllDSignalsInfo()
    show_result(str(data))

def BestAP():
    data=Trier_AP()
    show_result(str(data))

def AnalyzeAP():
    data=InfoAP()
    show_result(str(data))

def Disconnect():
    data=disconnect()
    show_result(str(data))

def Connect():
    data=connect(root)
    show_result(str(data))

#creation et style de ces boutons de fonctionnalités 
tb_btn_style = {
    "font": ctk.CTkFont(size=14,weight="bold"),
    "fg_color": "#787778",
    "hover_color": "#787778",
    "text_color": "white",
    "corner_radius": 8,
    "height": 40,
    "width": 90
}

discover_btn = ctk.CTkButton(toolbar_left, text="Découvrir Wi‑Fi à proximité", command=DiscoverAP, **tb_btn_style)
discover_btn.pack(side="left", padx=8, pady=10)

analyze_btn = ctk.CTkButton(toolbar_left, text="Analyser Wi‑Fi actuel", command=AnalyzeAP, **tb_btn_style)
analyze_btn.pack(side="left", padx=8, pady=10)

tri_btn = ctk.CTkButton(toolbar_left, text="Trier  Wi‑Fi par signal décroissant ", command=BestAP, **tb_btn_style)
tri_btn.pack(side="left", padx=8, pady=10)

connect_btn = ctk.CTkButton(toolbar_left, text="Se connecter au Wi‑Fi le plus puissant", command=Connect, **tb_btn_style)
connect_btn.pack(side="left", padx=8, pady=10)

disconnect_btn = ctk.CTkButton(toolbar_left, text="Se déconnecter du Wi‑Fi", command=Disconnect, **tb_btn_style)
disconnect_btn.pack(side="left", padx=8, pady=10)

#controler l'affichage du resultat dans zone de texte du GUI 
result_text.configure(state="disabled")
def show_result(msg):
    # Recréer le champ de texte si nécessaire
    if not any(isinstance(widget, ctk.CTkTextbox) for widget in center_frame.winfo_children()):
        global result_text
        result_text = ctk.CTkTextbox(center_frame, height=250, font=("Consolas", 14), wrap="word")
        result_text.pack(fill="both", expand=True, padx=40, pady=(0, 30))
    result_text.configure(state="normal")
    result_text.delete("1.0", "end")
    result_text.insert("end", msg)
    result_text.configure(state="disabled")

#controler l'affichage de GUI avant les courbes et permettre  d'executer courbes de facon normal apres la fermeture de GUI
def _on_app_close():
    try: stop_update()
    except Exception: pass
    try: stop_updateALL()
    except Exception: pass
    try: plt.close('all')
    except Exception: pass
    try: root.destroy()
    except Exception:
        try: root.quit()
        except Exception: pass

root.protocol("WM_DELETE_WINDOW", _on_app_close)