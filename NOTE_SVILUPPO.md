# Note di sviluppo — Visualizzatore dati UCC

## Sessione 2026-04-29

### Contesto
LP ha proposto di rendere pubblici i dati giornalieri delle stazioni UCC (temperatura aria, roccia, acqua). Il file Excel di prova è `Data/FSV/UCC_FVG_03_datipronti.xlsx`, che contiene i dati della stazione **FVG-01 Torri di Slivia** (337 giorni, mar 2025 – mar 2026).

### Cosa è stato costruito

#### `make_station_csv.py`
Script Python che converte l'Excel di una stazione in CSV + file meta JSON.
- Per aggiornare i dati: `python3 make_station_csv.py fvg03`
- Per aggiungere una nuova stazione: aggiungere un blocco in `STATIONS` nel file
- Output: `data/fvg03.csv` e `data/fvg03_meta.json`

#### `dati.html`
Pagina generica per visualizzare i dati di qualsiasi stazione.
- URL: `dati.html?station=fvg03`
- Funzionalità: selettore sensore, date picker, grafico (Chart.js) con banda min/max, statistiche periodo, tabella opzionale
- Nessun backend: funziona su GitHub Pages

#### `ucc_data.js`
Aggiunto campo `dati_url` alla stazione FVG-01:
```json
"dati_url": "dati.html?station=fvg03"
```

#### `mappa_ucc.html`
Sostituito il popup Leaflet con un **drawer laterale**:
- Si apre a destra cliccando un marker
- Mostra tutte le info della stazione
- Bottone "📊 Visualizza dati" in cima (solo se disponibile)
- Si chiude con ✕ o cliccando sulla mappa

### Come aggiungere una nuova stazione

1. Mettere l'Excel in `Data/<cartella>/`
2. Aggiungere un blocco in `STATIONS` dentro `make_station_csv.py` con `column_map` e `sensors`
3. Eseguire: `python3 make_station_csv.py <chiave>`
4. Aggiungere `"dati_url": "dati.html?station=<chiave>"` alla stazione in `ucc_data.js`
5. `git add data/<chiave>.csv data/<chiave>_meta.json ucc_data.js && git commit && git push`

### Come aggiornare i dati

Sostituire l'Excel con la versione aggiornata, poi:
```bash
python3 make_station_csv.py fvg03
git add data/fvg03.csv && git commit -m "Aggiorna dati FVG-01" && git push
```

### Decisioni prese
- Dati in formato CSV (non JS), caricati con `fetch()` → serve server HTTP locale (`python3 -m http.server 8080`)
- Pagina generica parametrica (`?station=`) invece di una pagina per stazione
- Il nome chiave del CSV è `fvg03` anche se i dati sono di FVG-01 (dal nome file originale); da allineare in futuro
- Drawer laterale invece di popup per non coprire la mappa

### Da discutere
- Scansione dati: annuale vs mensile (proposta Franco)
- Rinominare `fvg03` → `fvg01` per coerenza con la stazione
- Aggiungere altre stazioni quando disponibili i dati
