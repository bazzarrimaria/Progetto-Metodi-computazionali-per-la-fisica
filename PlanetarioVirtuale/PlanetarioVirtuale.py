import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import odeint
import json

# --- 1. MODELLO FISICO (Equazione N-Corpi richiesta) ---
def modello_n_corpi(stato, t, masse, G):
    n = len(masse)
    pos = stato[:3*n].reshape((n, 3))
    vel = stato[3*n:].reshape((n, 3))
    accelerazioni = np.zeros((n, 3))
    
    for i in range(n):
        for j in range(n):
            if i != j: # Un corpo non esercita forza su se stesso
                r_vett = pos[j] - pos[i]
                dist_cubo = np.linalg.norm(r_vett)**3 # Norma al cubo per la formula di Newton
                # Legge di Gravitazione Universale: a = G * M / r^3 * r_vett
                accelerazioni[i] += G * masse[j] / dist_cubo * r_vett
                
    return np.concatenate([vel.flatten(), accelerazioni.flatten()])

# --- 2. METODO DI EULERO (Per confronto stabilità - Rif: L08) ---
def integratore_eulero(f, s0, t, args):
    dt = t[1] - t[0]
    stati = np.zeros((len(t), len(s0)))
    stati[0] = s0
    for i in range(len(t)-1):
        # Formula di Eulero: y(t+dt) = y(t) + f(y,t)*dt
        stati[i+1] = stati[i] + np.array(f(stati[i], t[i], *args)) * dt
    return stati

# --- 3. ANALISI ENERGIA (Studio Conservazione - Rif: L04) ---
def calcola_energia_sistema(stati, masse, G):
    n = len(masse)
    energie = []
    for s in stati:
        pos = s[:3*n].reshape((n, 3))
        vel = s[3*n:].reshape((n, 3))
        # 1. Energia Cinetica (K = 1/2 m v^2)
        K = 0.5 * np.sum(masse * np.sum(vel**2, axis=1))
        U = 0
        for i in range(n):
            for j in range(i + 1, n):
                # 2. Energia Potenziale (U = -G M m / r)
                U -= G * masse[i] * masse[j] / np.linalg.norm(pos[i] - pos[j])
        energie.append(K + U)
    return np.array(energie)

## --- ANALISI VELOCITÀ RADIALE (PUNTO 2) ---
def analizza_velocita_radiale(sol, nomi, t):
    # La stella è il primo corpo (indice 0)
    # sol[:, (n_corpi*3) + 0] estrae la velocità lungo l'asse x della stella
    n_corpi = len(nomi)
    v_radiale_stella = sol[:, (n_corpi * 3)] 
    
    plt.figure(figsize=(10, 5))
    tempo_giorni = t / (24 * 3600) # Conversione da secondi a giorni
    
    plt.plot(tempo_giorni, v_radiale_stella, color='royalblue', linewidth=2, label="Oscillazione Stella")
    plt.axhline(0, color='black', linestyle='--', alpha=0.3) # Linea dello zero
    
    plt.title(f"Studio Doppler: Velocità Radiale di {nomi[0]}", fontsize=14)
    plt.xlabel("Tempo (Giorni)", fontsize=12)
    plt.ylabel("Velocità Radiale (m/s)", fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    
    # Calcolo dell'ampiezza del segnale (K)
    K = (np.max(v_radiale_stella) - np.min(v_radiale_stella)) / 2
    plt.legend(loc='upper right')
    
    # Box informativo con il valore K
    plt.text(0.02, 0.95, f"Ampiezza segnale K: {K:.2f} m/s", 
             transform=plt.gca().transAxes, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.show()

# --- 4. ANIMAZIONE (Il Planetario Virtuale) ---
def mostra_animazione(sol, nomi):
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_aspect('equal')
    ax.grid(True, linestyle=':')
    limit = np.max(np.abs(sol[:, :3*len(nomi)])) * 1.2
    ax.set_xlim(-limit, limit); ax.set_ylim(-limit, limit)
    
    linee = [ax.plot([], [], '-', alpha=0.3)[0] for _ in nomi]
    punti = [ax.plot([], [], 'o', label=n)[0] for n in nomi]
    ax.legend(loc='upper right')

    def update(frame):
        idx = frame * (len(sol) // 200) # Seleziona il punto temporale attuale
        for i in range(len(nomi)):
            # x e y contengono la storia delle posizioni fino all'istante attuale
            x, y = sol[:idx, i*3], sol[:idx, i*3+1]
            linee[i].set_data(x, y)
            # Disegna il pianeta (SOLO l'ultimo punto calcolato)
            if idx > 0: punti[i].set_data([x[-1]], [y[-1]])
        return linee + punti

    ani = animation.FuncAnimation(fig, update, frames=200, interval=30, blit=True)
    plt.title("Planetario Virtuale: Simulazione Dinamica")
    plt.show()
    
def mostra_dashboard_generale(sol_odeint, sol_eulero, t, nomi, scelta, masse, G):
    """
    Visualizza i 4 grafici principali: Traiettorie, Energia, Velocità, Distanza.
    """
    n_corpi = len(nomi)
    idx_pos = scelta * 3
    idx_vel = (n_corpi * 3) + (scelta * 3)

    plt.figure(figsize=(14, 10))
    plt.suptitle(f"Analisi Dinamica del Sistema: Focus su {nomi[scelta]}", fontsize=16)

    # --- Quadrante 1: Traiettorie (Stella vs Pianeta) ---
    plt.subplot(2, 2, 1)
    # Stella (Corpo 0)
    plt.plot(sol_odeint[:, 0], sol_odeint[:, 1], color='orange', linewidth=2, label=f"Stella ({nomi[0]})")
    # Pianeta Scelto
    plt.plot(sol_odeint[:, idx_pos], sol_odeint[:, idx_pos+1], color='blue', label=f"{nomi[scelta]}")
    # Confronto Eulero (solo pianeta)
    plt.plot(sol_eulero[:, idx_pos], sol_eulero[:, idx_pos+1], 'r--', alpha=0.5, label="Eulero (Instabile)")
    # Centro di Massa
    plt.plot(0, 0, 'k+', markersize=12, label="Centro di Massa")
    plt.axis('equal')
    plt.legend(loc='upper right', fontsize='x-small')
    plt.title("Piano Orbitale (XY)")
    plt.xlabel("x (m)"); plt.ylabel("y (m)")

    # --- Quadrante 2: Errore Energia ---
    plt.subplot(2, 2, 2)
    E_odeint = calcola_energia_sistema(sol_odeint, masse, G)
    E_eulero = calcola_energia_sistema(sol_eulero, masse, G)
    # Calcolo errore relativo
    err_odeint = np.abs(E_odeint - E_odeint[0]) / (np.abs(E_odeint[0]) + 1e-20)
    err_eulero = np.abs(E_eulero - E_eulero[0]) / (np.abs(E_eulero[0]) + 1e-20)
    
    plt.semilogy(t/(3600*24), err_odeint, label="Odeint (LSODA)", color='green')
    plt.semilogy(t/(3600*24), err_eulero, label="Eulero", color='red', linestyle='--')
    plt.title("Conservazione dell'Energia Totale")
    plt.xlabel("Tempo (Giorni)"); plt.ylabel("Errore Relativo |(E-E0)/E0|")
    plt.legend(); plt.grid(True, alpha=0.3)

    # --- Quadrante 3: Modulo Velocità ---
    plt.subplot(2, 2, 3)
    v_mod = np.linalg.norm(sol_odeint[:, idx_vel : idx_vel+3], axis=1)
    plt.plot(t/(3600*24), v_mod, color='purple')
    plt.title(f"Velocità Scalare di {nomi[scelta]}")
    plt.xlabel("Tempo (Giorni)"); plt.ylabel("v (m/s)")
    plt.grid(True, alpha=0.3)

    # --- Quadrante 4: Distanza dalla Stella ---
    plt.subplot(2, 2, 4)
    # Distanza relativa tra Pianeta e Stella (che si muove!)
    r_vett = sol_odeint[:, idx_pos:idx_pos+3] - sol_odeint[:, 0:3]
    r_mod = np.linalg.norm(r_vett, axis=1)
    plt.plot(t/(3600*24), r_mod, color='brown')
    plt.title(f"Distanza Stella - {nomi[scelta]}")
    plt.xlabel("Tempo (Giorni)"); plt.ylabel("Distanza (m)")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def main():
    # --- 1. CONFIGURAZIONE ARGPARSE ---
    parser = argparse.ArgumentParser(description="Simulatore N-Corpi per l'esame di Metodi Computazionali.")
    
    # Argomento obbligatorio: il file JSON
    parser.add_argument("file", help="Percorso del file JSON con i dati del sistema")
    
    # Argomenti opzionali: sovrascrivono il JSON se presenti
    parser.add_argument("-t", "--tempo", type=float, help="Durata simulazione in anni")
    parser.add_argument("-p", "--punti", type=int, help="Numero di punti per l'integrazione")
    parser.add_argument("--no-menu", action="store_true", help="Esegue e mostra tutto senza menu interattivo")

    args = parser.parse_args()

    # --- 2. CARICAMENTO DATI ---
    try:
        with open(args.file, 'r') as f:
            conf = json.load(f)
    except Exception as e:
        print(f"Errore caricamento file: {e}")
        sys.exit(1)

    # Priorità: argparse > json > default
    G = conf['G']
    nomi = [c['nome'] for c in conf['corpi']]
    n_corpi = len(nomi)
    anni = args.tempo if args.tempo else float(conf.get('durata_anni', 1.0))
    n_punti = args.punti if args.punti else int(conf.get('punti_simulazione', 10000))

    # --- 3. PREPARAZIONE FISICA & CM (come prima) ---
    masse = np.array([c['massa'] for c in conf['corpi']])
    pos_iniziali = np.array([v for c in conf['corpi'] for v in c['posizione']]).flatten()
    vel_raw = np.array([v for c in conf['corpi'] for v in c['velocita']]).reshape(n_corpi, 3)
    
    # Rimozione velocità Centro di Massa
    v_cm = np.sum(masse[:, np.newaxis] * vel_raw, axis=0) / np.sum(masse)
    vel_corrette = (vel_raw - v_cm).flatten()
    s0 = np.concatenate([pos_iniziali, vel_corrette])
    t = np.linspace(0, anni * 365.25 * 24 * 3600, n_punti)

    # --- 4. INTEGRAZIONE ---
    print(f"\n> Simulazione: {args.file} | Corpi: {n_corpi} | Anni: {anni}")
    sol_odeint = odeint(modello_n_corpi, s0, t, args=(masse, G))
    sol_eulero = integratore_eulero(modello_n_corpi, s0, t, args=(masse, G))

    # --- 5. GESTIONE OUTPUT ---
    if args.no_menu:
        mostra_dashboard_generale(sol_odeint, sol_eulero, t, nomi, 1, masse, G)
        analizza_velocita_radiale(sol_odeint, nomi, t)
        mostra_animazione(sol_odeint, nomi)
    else:
        pianeta_idx = 1
        while True:
            print("\n" + "="*40)
            print(f" MENU PRINCIPALE- Target attuale: {nomi[pianeta_idx].upper()}")
            print("="*40)
            print("1. Dashboard Generale (Traiettorie, Energia, Distanze)")
            print("2. Analisi Spettroscopia Doppler (Velocità Radiale Stella)")
            print("3. Animazione 2D del Sistema")
            print("4. Cambia Pianeta target (per grafici 1 e 3)")
            print("0. Esci")
        
            scelta_menu = input("\nCosa vuoi visualizzare? [0-4]: ")

            if scelta_menu == '0':
                print("Chiusura programma. Arrivederci!")
                break

            elif scelta_menu == '1':
            # Chiede quale pianeta se non è stato definito, default 1
                if 'pianeta_idx' not in locals(): pianeta_idx = 1
                mostra_dashboard_generale(sol_odeint, sol_eulero, t, nomi, pianeta_idx, masse, G)

            elif scelta_menu == '2':
                print(f"\nGenerazione grafico velocità radiale per: {nomi[0]}...")
                analizza_velocita_radiale(sol_odeint, nomi, t)

            elif scelta_menu == '3':
                print("\nAvvio animazione (chiudi la finestra per tornare al menu)...")
                mostra_animazione(sol_odeint, nomi)

            elif scelta_menu == '4':
                print("\nPianeti disponibili:")
                for i, nome in enumerate(nomi):
                    print(f"[{i}] {nome}")
                try:
                    p = int(input("Seleziona indice nuovo pianeta target: "))
                    if 0 <= p < n_corpi:
                        pianeta_idx = p
                        print(f"Target impostato su: {nomi[p]}")
                    else:
                        print("Indice non valido.")
                except:
                    print("Input non valido.")
            else:
                print("Opzione non valida, riprova.")

if __name__ == "__main__":
    main()