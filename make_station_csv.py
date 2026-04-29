#!/usr/bin/env python3
"""
Converte Excel stazione UCC → CSV + meta.json per dati.html
Uso: python3 make_station_csv.py [station_id]
     python3 make_station_csv.py fvg03
     python3 make_station_csv.py          # tutte le stazioni
"""

import pandas as pd
import json
import sys
from pathlib import Path

# ─── Configurazione stazioni ────────────────────────────────────────────────
STATIONS = {
    'fvg03': {
        'excel': 'Data/FSV/UCC_FVG_03_datipronti.xlsx',
        'name': 'Grotta Arnaldo Germoni',
        'station_id': 'FVG-03',
        'column_map': {
            'Date':                       'date',
            'Prepotto_ext_T_mean':        'ext_mean',
            'Prepotto_ext_T_max':         'ext_max',
            'Prepotto_ext_T_min':         'ext_min',
            'Slivia_5_air_int_1_mean':    'air1_mean',
            'Slivia_5_air_int_1_max':     'air1_max',
            'Slivia_5_air_int_1_min':     'air1_min',
            'Slivia_5_air_int_2_mean':    'air2_mean',
            'Slivia_5_air_int_2_max':     'air2_max',
            'Slivia_5_air_int_2_min':     'air2_min',
            'Slivia_5_water_mean':        'water_mean',
            'Slivia_5_water_max':         'water_max',
            'Slivia_5_water_min':         'water_min',
            'Slivia_5_rock40_mean':       'rock_mean',
            'Slivia_5_rock40_max':        'rock_max',
            'Slivia_5_rock40_min':        'rock_min',
        },
        'sensors': {
            'ext':   'T esterna (Prepotto)',
            'air1':  'T aria interna 1',
            'air2':  'T aria interna 2',
            'water': 'T acqua',
            'rock':  'T roccia 40cm',
        },
    },
    # ── Aggiungere nuove stazioni qui ──
    # 'fvg01': {
    #     'excel': 'Data/.../UCC_FVG_01_datipronti.xlsx',
    #     'name': 'Grotta delle Torri di Slivia',
    #     'station_id': 'FVG-01',
    #     'column_map': { ... },
    #     'sensors': { ... },
    # },
}
# ────────────────────────────────────────────────────────────────────────────


def convert(station_key):
    cfg = STATIONS[station_key]
    excel_path = Path(cfg['excel'])
    if not excel_path.exists():
        print(f"  ERRORE: {excel_path} non trovato")
        return

    df = pd.read_excel(excel_path)
    df = df.rename(columns=cfg['column_map'])
    df = df[list(cfg['column_map'].values())]  # mantieni solo colonne mappate
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

    numeric_cols = [c for c in df.columns if c != 'date']
    df[numeric_cols] = df[numeric_cols].round(2)
    df = df.sort_values('date').reset_index(drop=True)

    out_dir = Path('data')
    out_dir.mkdir(exist_ok=True)

    csv_path = out_dir / f'{station_key}.csv'
    df.to_csv(csv_path, index=False)
    print(f"  CSV: {csv_path}  ({len(df)} righe)")

    meta = {
        'station_id': cfg['station_id'],
        'name': cfg['name'],
        'sensors': cfg['sensors'],
        'date_min': df['date'].min(),
        'date_max': df['date'].max(),
    }
    meta_path = out_dir / f'{station_key}_meta.json'
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    print(f"  Meta: {meta_path}")


def main():
    targets = sys.argv[1:] if len(sys.argv) > 1 else list(STATIONS.keys())
    for key in targets:
        if key not in STATIONS:
            print(f"Stazione sconosciuta: {key}. Disponibili: {list(STATIONS.keys())}")
            continue
        print(f"Elaborazione {key}...")
        convert(key)
    print("Fatto.")


if __name__ == '__main__':
    main()
