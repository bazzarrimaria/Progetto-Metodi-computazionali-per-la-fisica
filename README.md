# Progetto di Metodi Computazionali per la Fisica - 2025

Documentazione per il progetto finale del corso di "Metodi Computazionali per la Fisica" 
per la Laurea Triennale in Fisica dell'Università degli Studi di Perugia.

## Descrizione del progetto

Il progetto consiste nello sviluppo di un simulatore dinamico N-Corpi per lo studio numerico di sistemi planetari.

* Gli obiettivi principali sono:
  * integrazione numerica delle equazioni del moto gravitazionale;
  * analisi della stabilità numerica dei metodi di integrazione;
  * studio della conservazione dell’energia meccanica totale;
  * simulazione della rilevazione di esopianeti tramite tecnica della velocità radiale (effetto Doppler).


Il codice implementa un sistema configurabile tramite file JSON esterni, permettendo la simulazione di sistemi planetari generici.

Lo script principale **[PlanetarioVirtuale.py](PlanetarioVirtuale/PlanetarioVirtuale.py)** può essere eseguito da terminale tramite l'interprete Python:
  ```bash
    $ python3 PlanetarioVirtuale.py nome-file-sistema.json
  ```
Il programma supporta l'utilizzo di argomenti da riga di comando per personalizzare la simulazione tramite il modulo `argparse`.

## Modello Fisico

Il sistema è descritto dall’equazione gravitazionale N-Corpi:

$$m_i \ddot{\mathbf{r}}_i = \sum_{j \neq i} G \frac{m_i m_j}{|\mathbf{r}_{ij}|^3} \mathbf{r}_{ij}$$

Le equazioni del moto sono integrate numericamente a partire da condizioni iniziali assegnate (posizioni e velocità).

La velocità del centro di massa viene rimossa inizialmente per evitare drift globale del sistema.

## Metodi Numerici

  * LSODA (scipy.integrate.odeint)
  Metodo adattivo per l’integrazione delle ODE.

  * Metodo di Eulero esplicito (confronto stabilità)
  Implementato per confronto della stabilità numerica.

## Analisi Energetica

Per ogni simulazione viene calcolata:

  * Energia cinetica totale
  * Energia potenziale gravitazionale
  * Energia meccanica totale

Errore relativo:
$$\frac{|E(t) - E(0)|}{|E(0)|}$$

per confrontare la stabilità dei diversi metodi di integrazione.

## Tecnica della Velocità Radiale (Effetto Doppler)

La velocità radiale della stella viene calcolata come: 

  * componente x della velocità della stella.

Ipotesi modellistiche:

  * l’asse x coincide con la linea di vista dell’osservatore;

  * l’inclinazione orbitale non è parametrizzata;

  * il caso simulato corrisponde a proiezione massima del segnale Doppler.

L’ampiezza del segnale *K* viene calcolata come semidifferenza tra valore massimo e minimo della velocità radiale.

$$K = \frac{v_{max} - v_{min}}{2}$$

## Configurazione dei Sistemi (Input JSON)

Sono forniti diversi sistemi di test:

* Configurazione dei Sistemi (Input JSON)
  * [sistema.json](PlanetarioVirtuale/sistema.json) - Sistema Solare Interno (Benchmark stabilità)
  * [sistema2.json](PlanetarioVirtuale/sistema2.json) - Hot Jupiter (Analisi Spettroscopia Doppler)
  * [sistema3.json](PlanetarioVirtuale/sistema3.json) - Orbita Eccentrica (Leggi di Keplero)
  * [sistema4.json](PlanetarioVirtuale/sistema4.json) - Sistema N-Corpi Massicci (Interazioni reciproche)

  Ogni file JSON contiene:

    * costante gravitazionale
    * masse
    * posizioni iniziali
    * velocità iniziali
    * durata della simulazione
    * numero di punti temporali


## Output e Visualizzazioni

Il programma fornisce:

  * Traiettorie orbitali nel piano XY
  * Analisi dell’energia totale
  * Andamento della velocità scalare
  * Distanza stella–pianeta
  * Grafico della velocità radiale
  * Animazione 2D del sistema

Il progetto integra modellizzazione fisica, metodi numerici e visualizzazione grafica in un’unica applicazione modulare e configurabile.


## Istruzioni per l'Esecuzione

L'interfaccia a riga di comando permette i seguenti utilizzi:

1. **Esecuzione standard**:

  ```bash
    $ python3 PlanetarioVirtuale.py sistema.json
  ```

2. **Esecuzione con parametri personalizzati**:

  ```bash
   $ python3 PlanetarioVirtuale.py sistema.json --tempo 5 --punti 50000
  ```
  
3. **Modalità automatica (No-Menu)**:

  ```bash
   $ python3 PlanetarioVirtuale.py sistema.json --no-menu
  ```


