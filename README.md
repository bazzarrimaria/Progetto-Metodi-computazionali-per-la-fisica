# Progetto di Metodi Computazionali per la Fisica - 2025

Documentazione per il progetto finale del corso di "Metodi Computazionali per la Fisica" 
per la Laurea Triennale in Fisica dell'Università degli Studi di Perugia.

Il progetto consiste in un simulatore dinamico N-Corpi focalizzato sullo studio della stabilità dei sistemi planetari e sulla rilevazione di esopianeti tramite la tecnica della velocità radiale.

Lo script principale `PlanetarioVirtuale.py` può essere eseguito da terminale tramite l'interprete Python:

    $ python3 PlanetarioVirtuale.py nome-file-sistema.json

Il programma supporta l'utilizzo di argomenti da riga di comando per personalizzare la simulazione tramite il modulo `argparse`.

Sistemi e Analisi Disponibili
=========================================

* [Descrizione del Progetto](Presentazione_Esame.pdf)
  * Presentazione in formato PDF con l'analisi fisica e numerica dei risultati.

* Configurazione dei Sistemi (Input JSON)
  * [sistema.json](PlanetarioVirtuale/sistema.json) - Sistema Solare Interno (Benchmark stabilità)
  * [sistema2.json](PlanetarioVirtuale/sistema2.json) - Hot Jupiter (Analisi Spettroscopia Doppler)
  * [sistema3.json](PlanetarioVirtuale/sistema3.json) - Orbita Eccentrica (Leggi di Keplero)
  * [sistema4.json](PlanetarioVirtuale/sistema4.json) - Sistema N-Corpi Massicci (Interazioni reciproche)

* Metodologie Numeriche Implementate
  * **L04 / L08**: Integrazione tramite `scipy.integrate.odeint` (LSODA) e confronto con il metodo di Eulero.
  * **Analisi Energetica**: Studio della conservazione dell'energia meccanica totale del sistema.
  * **L07a (argparse)**: Gestione dinamica degli ingressi (durata, risoluzione, target).

Istruzioni per l'Esecuzione
=========================================

L'interfaccia a riga di comando permette i seguenti utilizzi:

1. **Esecuzione standard**:
   `$ python3 PlanetarioVirtuale.py sistema.json`

2. **Esecuzione con parametri personalizzati**:
   `$ python3 PlanetarioVirtuale.py sistema.json --tempo 5 --punti 50000`

3. **Modalità automatica (No-Menu)**:
   `$ python3 PlanetarioVirtuale.py sistema.json --no-menu`

=========================================
