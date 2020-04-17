# COVID-19-Apache-Beam-Statistics
Elaborazione statistica sui dati del COVID-19 usando Apache Beam per Google Cloud Dataflow in Python. Progetto per l'esame di Sistemi ed Applicazioni Cloud (2019-20), corso *Magistrale di Ingegneria Informatica presso il Dipartimento di Ingegneria Enzo Ferrari*. 

## Tipologia di dati accettata
La tipologia di dati accettata segue lo schema dei dati per provincia proposto dal repository [pcm-dpc/COVID-19](https://github.com/pcm-dpc/COVID-19) italiano.

## Input CLI
```
usage: covid.py [-h] [--input INPUT] [--output OUTPUT] [--ntop NTOP]

optional arguments:
  -h, --help       show this help message and exit
  --input INPUT    Input for the pipeline
  --output OUTPUT  Output for the pipeline
  --ntop NTOP      Number of top day cases to show
```

### Dati per Provincia
**Directory:**  datasets<br>
**File complessivo:** dpc-covid19-ita-province.csv<br>

| Nome campo              | Descrizione                         | Formato            | Esempio              |
|-------------------------|-------------------------------------|--------------------|----------------------|
| **data** ( * )                   | Data dell'informazione              | YYYY-MM-DD HH:MM:SS (ISO 8601) Ora italiana           | 2020-03-05 12:15:45 |                   |
|   stato                    | Stato di riferimento                | ISO 3166-1 alpha-3 | ITA                  |
|   codice_regione            | Codice della Regione (ISTAT 2019)   | Numero             | 13                   |
| **denominazione_regione** ( * )  | Denominazione della Regione         | Testo              | Abruzzo              |
|   codice_provincia          | Codice della Provincia (ISTAT 2019) | Numero             | 067                  |
| **denominazione_provincia** ( * )| Denominazione della provincia       | Testo              | Teramo               |
|   sigla_provincia           | Sigla della Provincia               | Testo              | TE                   |
|   lat                       | Latitudine                          | Latitude                        | WGS84              | 42.6589177           |
|   long                      | Longitudine                         |WGS84              | 13.70439971          |
| **totale_casi** ( * )             | Totale casi positivi                | Numero             | 3                    |
|   note_it                       | Note in lingua italiana (separate da ;)                   | Testo                        | pd-IT-000                   |
|   note_en                       | Note in lingua inglese (separate da ;)                    | Testo                        | pd-EN-000                   |

*Le Province autonome di Trento e Bolzano sono indicate in "denominazione regione" e con il codice 04 del Trentino Alto Adige.*<br>
*Ogni Regione ha una Provincia denominata "In fase di definizione/aggiornamento" con il codice provincia da 979 a 999, utile ad indicare i dati ancora non assegnati alle Province.*<br>
( * ) Dati utilizzati dalla pipeline per la produzione delle informazioni di output.

## Com'è definito l'output
Un esempio di output è il seguente, per ogni Regione-Provincia:
```python
...
('Emilia-Romagna,Modena', {'statistica_casi': [{'media': 1245.2692307692307, 'varianza': 1375365.1198224854, 'stddev': 1172.7596172372603}], 'top_3_casi': [[3217, 3180, 3132]], 'ultimi_dati': [{'data': '2020-04-15', 'casi': 3217}]})
...
```

Il significato dei campi è il seguente:
```python
...
('REGIONE,PROVINCIA', {'statistica_casi': [{'media': MEDIA_STATISTICA, 'varianza': VARIANZA_STATISTICA, 'stddev': DEVIZIONE_STANDARD}], 'top_<ntop>_casi': [[TOP_1_CASI_IN_UNA_GIORNATA, TOP_2_CASI_IN_UNA_GIORNATA, ..., TOP_<ntop>_CASI_IN_UNA_GIORNATA]], 'ultimi_dati': [{'data': 'ULTIMA_DATA_DEL_DATASET', 'casi': ULTIMI_CASI_DEL_DATASET}]})
...
```
