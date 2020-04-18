# COVID-19-Apache-Beam-Statistics
Statistical processing of COVID-19 data using Apache Beam for Google Cloud Dataflow in Python. Project for the examination of Cloud Systems and Applications (2019-20), course *Magistrale di Ingegneria Informatica at the Dipartimento di Ingegneria Enzo Ferrari*. 

## Type of data accepted
The type of data accepted follows the data scheme by province proposed by the repository [pcm-dpc/COVID-19](https://github.com/pcm-dpc/COVID-19) Italian.

## Input CLI
```
usage: covid.py [-h] [--input INPUT] [--output OUTPUT] [--ntop NTOP]

optional arguments:
  -h, --help       show this help message and exit
  --input INPUT    Input for the pipeline
  --output OUTPUT  Output for the pipeline
  --ntop NTOP      Number of top day cases to show
```

### Data by Province
**Directory:**  datasets<br>
**Overall file:** dpc-covid19-ita-province.csv<br>

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

*The Autonomous Provinces of Trento and Bolzano are indicated in "denominazione_regione" and with the code 04 of Trentino Alto Adige.*<br>.
*Each Region has a Province named "In fase di definizione/aggiornamento" with the province code from 979 to 999, useful to indicate the data not yet assigned to the Provinces.*<br>.
( * ) These are the data used by the pipeline to compute the output.

## How is the output
Un esempio di output è il seguente, per ogni Regione-Provincia:
```python
...
('Emilia-Romagna,Modena', {'cases_statistics': [{'mean': 1245.2692307692307, 'variance': 1375365.1198224854, 'stddev': 1172.7596172372603}], 'top_3_cases': [[3217, 3180, 3132]], 'last_data': [{'date': '2020-04-15', 'cases': 3217}]})
...
```

The meaning of the fields is as follows:
```python
...
('REGION,PROVINCE', {'cases_statistics': [{'mean': STATISTIC_MEAN, 'variance': STATISTIC_VARIANCE, 'stddev': STANDARD_DEVIATION}], 'top_<ntop>_cases': [[TOP_1_DAY_CASES, TOP_2_DAY_CASES, ..., TOP_<ntop>_DAY_CASES]], 'last_data': [{'date': 'YYYY-MM-DD_LAST_DATE_IN_THE_DATASET', 'cases': LAST_CASES_IN_THE_DATASET}]})
...
```


### Complete example output
```python
('Abruzzo,Chieti', {'cases_statistics': [{'mean': 154.84615384615384, 'variance': 26258.630177514795, 'stddev': 162.04514857753315}], 'top_3_cases': [[469, 469, 465]], 'last_data': [{'date': '2020-04-15', 'cases': 469}]})
("Abruzzo,L'Aquila", {'cases_statistics': [{'mean': 73.92307692307692, 'variance': 6778.1094674556225, 'stddev': 82.32927466858689}], 'top_3_cases': [[229, 228, 220]], 'last_data': [{'date': '2020-04-15', 'cases': 229}]})
('Abruzzo,Pescara', {'cases_statistics': [{'mean': 347.63461538461536, 'variance': 113184.07803254439, 'stddev': 336.4284144250369}], 'top_3_cases': [[971, 947, 930]], 'last_data': [{'date': '2020-04-15', 'cases': 971}]})
('Abruzzo,Teramo', {'cases_statistics': [{'mean': 205.8653846153846, 'variance': 51043.34726331361, 'stddev': 225.92774788262201}], 'top_3_cases': [[605, 601, 599]], 'last_data': [{'date': '2020-04-15', 'cases': 605}]})
('Basilicata,Matera', {'cases_statistics': [{'mean': 52.42307692307692, 'variance': 3788.1671597633144, 'stddev': 61.54808818934439}], 'top_3_cases': [[155, 155, 155]], 'last_data': [{'date': '2020-04-15', 'cases': 155}]})
('Basilicata,Potenza', {'cases_statistics': [{'mean': 65.28846153846153, 'variance': 4138.243713017753, 'stddev': 64.32918243703827}], 'top_3_cases': [[165, 164, 164]], 'last_data': [{'date': '2020-04-15', 'cases': 165}]})
('P.A. Bolzano,Bolzano', {'cases_statistics': [{'mean': 784.0769230769231, 'variance': 601540.147928994, 'stddev': 775.5901932908861}], 'top_3_cases': [[2224, 2184, 2149]], 'last_data': [{'date': '2020-04-15', 'cases': 2224}]})
('Calabria,Catanzaro', {'cases_statistics': [{'mean': 68.17307692307692, 'variance': 5278.412352071006, 'stddev': 72.65268303422116}], 'top_3_cases': [[190, 184, 183]], 'last_data': [{'date': '2020-04-15', 'cases': 190}]})
('Calabria,Cosenza', {'cases_statistics': [{'mean': 103.5576923076923, 'variance': 12421.515902366864, 'stddev': 111.45185463852481}], 'top_3_cases': [[318, 317, 295]], 'last_data': [{'date': '2020-04-15', 'cases': 318}]})
('Calabria,Crotone', {'cases_statistics': [{'mean': 51.26923076923077, 'variance': 2239.8505917159764, 'stddev': 47.327059825389284}], 'top_3_cases': [[117, 117, 117]], 'last_data': [{'date': '2020-04-15', 'cases': 117}]})
('Calabria,Reggio di Calabria', {'cases_statistics': [{'mean': 104.57692307692308, 'variance': 10698.474852071004, 'stddev': 103.4334319843976}], 'top_3_cases': [[276, 268, 263]], 'last_data': [{'date': '2020-04-15', 'cases': 276}]})
('Calabria,Vibo Valentia', {'cases_statistics': [{'mean': 24.98076923076923, 'variance': 662.2496301775147, 'stddev': 25.73421127949164}], 'top_3_cases': [[68, 68, 68]], 'last_data': [{'date': '2020-04-15', 'cases': 68}]})
('Campania,Avellino', {'cases_statistics': [{'mean': 151.65384615384616, 'variance': 23684.803254437866, 'stddev': 153.89867853376086}], 'top_3_cases': [[407, 402, 401]], 'last_data': [{'date': '2020-04-15', 'cases': 407}]})
('Campania,Benevento', {'cases_statistics': [{'mean': 42.42307692307692, 'variance': 3183.8594674556216, 'stddev': 56.425698643930154}], 'top_3_cases': [[157, 157, 156]], 'last_data': [{'date': '2020-04-15', 'cases': 157}]})
('Campania,Caserta', {'cases_statistics': [{'mean': 142.65384615384616, 'variance': 18485.995562130174, 'stddev': 135.96321400338465}], 'top_3_cases': [[390, 387, 381]], 'last_data': [{'date': '2020-04-15', 'cases': 390}]})
('Campania,Napoli', {'cases_statistics': [{'mean': 679.1153846153846, 'variance': 479064.33284023666, 'stddev': 692.1447340262271}], 'top_3_cases': [[2026, 2010, 1932]], 'last_data': [{'date': '2020-04-15', 'cases': 2026}]})
('Campania,Salerno', {'cases_statistics': [{'mean': 200.17307692307693, 'variance': 41224.412352071005, 'stddev': 203.03795790952736}], 'top_3_cases': [[564, 557, 541]], 'last_data': [{'date': '2020-04-15', 'cases': 564}]})
('Emilia-Romagna,Bologna', {'cases_statistics': [{'mean': 1132.8653846153845, 'variance': 1398924.6164940828, 'stddev': 1182.7614368477198}], 'top_3_cases': [[3380, 3320, 3292]], 'last_data': [{'date': '2020-04-15', 'cases': 3380}]})
('Emilia-Romagna,Ferrara', {'cases_statistics': [{'mean': 207.34615384615384, 'variance': 50196.226331360944, 'stddev': 224.04514351210773}], 'top_3_cases': [[649, 635, 618]], 'last_data': [{'date': '2020-04-15', 'cases': 649}]})
('Emilia-Romagna,Forlì-Cesena', {'cases_statistics': [{'mean': 436.21153846153845, 'variance': 203170.2821745562, 'stddev': 450.7441426957828}], 'top_3_cases': [[1324, 1301, 1245]], 'last_data': [{'date': '2020-04-15', 'cases': 1324}]})
('Emilia-Romagna,Modena', {'cases_statistics': [{'mean': 1245.2692307692307, 'variance': 1375365.1198224854, 'stddev': 1172.7596172372603}], 'top_3_cases': [[3217, 3180, 3132]], 'last_data': [{'date': '2020-04-15', 'cases': 3217}]})
('Emilia-Romagna,Parma', {'cases_statistics': [{'mean': 1176.0576923076924, 'variance': 868221.5159023667, 'stddev': 931.7840500364699}], 'top_3_cases': [[2616, 2582, 2573]], 'last_data': [{'date': '2020-04-15', 'cases': 2616}]})
('Emilia-Romagna,Piacenza', {'cases_statistics': [{'mean': 1605.5192307692307, 'variance': 1275258.8265532549, 'stddev': 1129.2735835718706}], 'top_3_cases': [[3223, 3167, 3138]], 'last_data': [{'date': '2020-04-15', 'cases': 3223}]})
('Emilia-Romagna,Ravenna', {'cases_statistics': [{'mean': 331.61538461538464, 'variance': 99385.8520710059, 'stddev': 315.2552173573118}], 'top_3_cases': [[889, 880, 827]], 'last_data': [{'date': '2020-04-15', 'cases': 889}]})
("Emilia-Romagna,Reggio nell'Emilia", {'cases_statistics': [{'mean': 1395.1153846153845, 'variance': 2039228.8328402366, 'stddev': 1428.0156976869116}], 'top_3_cases': [[3982, 3947, 3888]], 'last_data': [{'date': '2020-04-15', 'cases': 3982}]})
('Emilia-Romagna,Rimini', {'cases_statistics': [{'mean': 822.0576923076923, 'variance': 423440.7466715978, 'stddev': 650.7232489097019}], 'top_3_cases': [[1749, 1740, 1727]], 'last_data': [{'date': '2020-04-15', 'cases': 1749}]})
('Friuli Venezia Giulia,Gorizia', {'cases_statistics': [{'mean': 54.32692307692308, 'variance': 2397.7969674556207, 'stddev': 48.967305086717}], 'top_3_cases': [[130, 129, 127]], 'last_data': [{'date': '2020-04-15', 'cases': 130}]})
('Friuli Venezia Giulia,Pordenone', {'cases_statistics': [{'mean': 213.53846153846155, 'variance': 45502.210059171586, 'stddev': 213.3124704727119}], 'top_3_cases': [[557, 551, 547]], 'last_data': [{'date': '2020-04-15', 'cases': 557}]})
('Friuli Venezia Giulia,Trieste', {'cases_statistics': [{'mean': 337.4807692307692, 'variance': 102084.40347633135, 'stddev': 319.506499896843}], 'top_3_cases': [[961, 945, 916]], 'last_data': [{'date': '2020-04-15', 'cases': 961}]})
('Friuli Venezia Giulia,Udine', {'cases_statistics': [{'mean': 356.0769230769231, 'variance': 108991.37869822484, 'stddev': 330.1384235411335}], 'top_3_cases': [[891, 890, 884]], 'last_data': [{'date': '2020-04-15', 'cases': 891}]})
('Lazio,Frosinone', {'cases_statistics': [{'mean': 162.71153846153845, 'variance': 32009.705251479292, 'stddev': 178.91256314602194}], 'top_3_cases': [[479, 473, 473]], 'last_data': [{'date': '2020-04-15', 'cases': 479}]})
('Lazio,Latina', {'cases_statistics': [{'mean': 151.46153846153845, 'variance': 23600.517751479292, 'stddev': 153.62460008566106}], 'top_3_cases': [[419, 410, 404]], 'last_data': [{'date': '2020-04-15', 'cases': 419}]})
('Lazio,Rieti', {'cases_statistics': [{'mean': 83.90384615384616, 'variance': 11545.086908284024, 'stddev': 107.44806609839017}], 'top_3_cases': [[277, 276, 276]], 'last_data': [{'date': '2020-04-15', 'cases': 277}]})
('Lazio,Roma', {'cases_statistics': [{'mean': 1268.9807692307693, 'variance': 1547428.7880917161, 'stddev': 1243.9569076506293}], 'top_3_cases': [[3665, 3560, 3431]], 'last_data': [{'date': '2020-04-15', 'cases': 3665}]})
('Lazio,Viterbo', {'cases_statistics': [{'mean': 110.90384615384616, 'variance': 13469.163831360944, 'stddev': 116.0567267820394}], 'top_3_cases': [[326, 326, 318]], 'last_data': [{'date': '2020-04-15', 'cases': 326}]})
('Liguria,Genova', {'cases_statistics': [{'mean': 911.9807692307693, 'variance': 1149857.288091716, 'stddev': 1072.313987641547}], 'top_3_cases': [[3487, 3472, 3086]], 'last_data': [{'date': '2020-04-15', 'cases': 3487}]})
('Liguria,Imperia', {'cases_statistics': [{'mean': 249.01923076923077, 'variance': 98910.3650147929, 'stddev': 314.5001828533537}], 'top_3_cases': [[1036, 979, 899]], 'last_data': [{'date': '2020-04-15', 'cases': 1036}]})
('Liguria,La Spezia', {'cases_statistics': [{'mean': 195.8846153846154, 'variance': 52194.29437869822, 'stddev': 228.4607064216913}], 'top_3_cases': [[696, 670, 670]], 'last_data': [{'date': '2020-04-15', 'cases': 696}]})
('Liguria,Savona', {'cases_statistics': [{'mean': 237.25, 'variance': 65823.61057692308, 'stddev': 256.56112444585807}], 'top_3_cases': [[797, 797, 771]], 'last_data': [{'date': '2020-04-15', 'cases': 717}]})
('Lombardia,Bergamo', {'cases_statistics': [{'mean': 5237.826923076923, 'variance': 15550045.181582838, 'stddev': 3943.3545594560524}], 'top_3_cases': [[10472, 10426, 10391]], 'last_data': [{'date': '2020-04-15', 'cases': 10472}]})
('Lombardia,Brescia', {'cases_statistics': [{'mean': 4926.596153846154, 'variance': 16520462.971523665, 'stddev': 4064.537239529694}], 'top_3_cases': [[11187, 11093, 11058]], 'last_data': [{'date': '2020-04-15', 'cases': 11187}]})
('Lombardia,Como', {'cases_statistics': [{'mean': 673.1153846153846, 'variance': 473129.37130177504, 'stddev': 687.8440021558486}], 'top_3_cases': [[2154, 2106, 2015]], 'last_data': [{'date': '2020-04-15', 'cases': 2154}]})
('Lombardia,Cremona', {'cases_statistics': [{'mean': 2445.2115384615386, 'variance': 2937323.2821745556, 'stddev': 1713.8620954366647}], 'top_3_cases': [[5202, 5172, 4945]], 'last_data': [{'date': '2020-04-15', 'cases': 5202}]})
('Lombardia,Lecco', {'cases_statistics': [{'mean': 827.9807692307693, 'variance': 537561.7496301774, 'stddev': 733.1860266195595}], 'top_3_cases': [[1982, 1970, 1911]], 'last_data': [{'date': '2020-04-15', 'cases': 1982}]})
('Lombardia,Lodi', {'cases_statistics': [{'mean': 1492.3461538461538, 'variance': 633877.1109467456, 'stddev': 796.1639975198235}], 'top_3_cases': [[2587, 2569, 2559]], 'last_data': [{'date': '2020-04-15', 'cases': 2587}]})
('Lombardia,Mantova', {'cases_statistics': [{'mean': 990.0769230769231, 'variance': 856298.801775148, 'stddev': 925.364145499029}], 'top_3_cases': [[2655, 2631, 2571]], 'last_data': [{'date': '2020-04-15', 'cases': 2655}]})
('Lombardia,Milano', {'cases_statistics': [{'mean': 5406.25, 'variance': 25540539.995192304, 'stddev': 5053.76493272019}], 'top_3_cases': [[14675, 14350, 14161]], 'last_data': [{'date': '2020-04-15', 'cases': 14675}]})
('Lombardia,Monza e della Brianza', {'cases_statistics': [{'mean': 1382.5961538461538, 'variance': 1938593.009985207, 'stddev': 1392.333656127441}], 'top_3_cases': [[3878, 3821, 3720]], 'last_data': [{'date': '2020-04-15', 'cases': 3878}]})
('Lombardia,Pavia', {'cases_statistics': [{'mean': 1344.0961538461538, 'variance': 1224308.6638313609, 'stddev': 1106.484823136477}], 'top_3_cases': [[3316, 3246, 3193]], 'last_data': [{'date': '2020-04-15', 'cases': 3316}]})
('Lombardia,Sondrio', {'cases_statistics': [{'mean': 270.1730769230769, 'variance': 78578.1431213018, 'stddev': 280.3179322150151}], 'top_3_cases': [[859, 849, 796]], 'last_data': [{'date': '2020-04-15', 'cases': 859}]})
('Lombardia,Varese', {'cases_statistics': [{'mean': 576.25, 'variance': 358143.5336538461, 'stddev': 598.4509450688888}], 'top_3_cases': [[1884, 1813, 1711]], 'last_data': [{'date': '2020-04-15', 'cases': 1884}]})
('Marche,Ancona', {'cases_statistics': [{'mean': 658.3461538461538, 'variance': 351171.0340236686, 'stddev': 592.5968562384285}], 'top_3_cases': [[1647, 1629, 1605]], 'last_data': [{'date': '2020-04-15', 'cases': 1647}]})
('Marche,Ascoli Piceno', {'cases_statistics': [{'mean': 97.38461538461539, 'variance': 10947.044378698223, 'stddev': 104.62812422431276}], 'top_3_cases': [[259, 254, 254]], 'last_data': [{'date': '2020-04-15', 'cases': 259}]})
('Marche,Fermo', {'cases_statistics': [{'mean': 141.32692307692307, 'variance': 19694.335428994087, 'stddev': 140.33650782670233}], 'top_3_cases': [[367, 363, 363]], 'last_data': [{'date': '2020-04-15', 'cases': 367}]})
('Marche,Macerata', {'cases_statistics': [{'mean': 306.0576923076923, 'variance': 87884.32359467456, 'stddev': 296.45290282720214}], 'top_3_cases': [[846, 837, 834]], 'last_data': [{'date': '2020-04-15', 'cases': 846}]})
('Marche,Pesaro e Urbino', {'cases_statistics': [{'mean': 1040.7692307692307, 'variance': 622428.6390532546, 'stddev': 788.9414674443565}], 'top_3_cases': [[2230, 2195, 2181]], 'last_data': [{'date': '2020-04-15', 'cases': 2230}]})
('Molise,Campobasso', {'cases_statistics': [{'mean': 72.46153846153847, 'variance': 4960.479289940828, 'stddev': 70.43067009436179}], 'top_3_cases': [[197, 191, 191]], 'last_data': [{'date': '2020-04-15', 'cases': 197}]})
('Molise,Isernia', {'cases_statistics': [{'mean': 12.807692307692308, 'variance': 333.0784023668639, 'stddev': 18.25043567608357}], 'top_3_cases': [[50, 50, 50]], 'last_data': [{'date': '2020-04-15', 'cases': 50}]})
('Piemonte,Alessandria', {'cases_statistics': [{'mean': 836.5961538461538, 'variance': 678663.8946005917, 'stddev': 823.810593887085}], 'top_3_cases': [[2407, 2367, 2315]], 'last_data': [{'date': '2020-04-15', 'cases': 2407}]})
('Piemonte,Asti', {'cases_statistics': [{'mean': 277.38461538461536, 'variance': 75457.00591715978, 'stddev': 274.6943863954263}], 'top_3_cases': [[897, 868, 793]], 'last_data': [{'date': '2020-04-15', 'cases': 897}]})
('Piemonte,Biella', {'cases_statistics': [{'mean': 264.7307692307692, 'variance': 66508.31213017752, 'stddev': 257.8920551901076}], 'top_3_cases': [[717, 702, 679]], 'last_data': [{'date': '2020-04-15', 'cases': 717}]})
('Piemonte,Cuneo', {'cases_statistics': [{'mean': 477.9230769230769, 'variance': 297861.91715976334, 'stddev': 545.7672738079514}], 'top_3_cases': [[1791, 1747, 1607]], 'last_data': [{'date': '2020-04-15', 'cases': 1791}]})
('Piemonte,Novara', {'cases_statistics': [{'mean': 497.61538461538464, 'variance': 289601.31360946747, 'stddev': 538.1461823793489}], 'top_3_cases': [[1708, 1638, 1612]], 'last_data': [{'date': '2020-04-15', 'cases': 1708}]})
('Piemonte,Torino', {'cases_statistics': [{'mean': 2717.4615384615386, 'variance': 8320590.056213018, 'stddev': 2884.5433011506375}], 'top_3_cases': [[8656, 8339, 8129]], 'last_data': [{'date': '2020-04-15', 'cases': 8656}]})
('Piemonte,Verbano-Cusio-Ossola', {'cases_statistics': [{'mean': 269.0576923076923, 'variance': 91268.01590236685, 'stddev': 302.105968001903}], 'top_3_cases': [[904, 893, 876]], 'last_data': [{'date': '2020-04-15', 'cases': 904}]})
('Piemonte,Vercelli', {'cases_statistics': [{'mean': 287.88461538461536, 'variance': 84454.75591715977, 'stddev': 290.61100446672657}], 'top_3_cases': [[847, 839, 830]], 'last_data': [{'date': '2020-04-15', 'cases': 847}]})
('Puglia,Bari', {'cases_statistics': [{'mean': 343.36538461538464, 'variance': 130731.23187869819, 'stddev': 361.56774175622775}], 'top_3_cases': [[1013, 989, 962]], 'last_data': [{'date': '2020-04-15', 'cases': 1013}]})
('Puglia,Barletta-Andria-Trani', {'cases_statistics': [{'mean': 80.5, 'variance': 9066.326923076924, 'stddev': 95.2172616865079}], 'top_3_cases': [[315, 306, 301]], 'last_data': [{'date': '2020-04-15', 'cases': 315}]})
('Puglia,Brindisi', {'cases_statistics': [{'mean': 120.03846153846153, 'variance': 15854.383136094673, 'stddev': 125.91418957406934}], 'top_3_cases': [[417, 403, 379]], 'last_data': [{'date': '2020-04-15', 'cases': 417}]})
('Puglia,Foggia', {'cases_statistics': [{'mean': 266.5192307692308, 'variance': 73516.67270710057, 'stddev': 271.1395815942419}], 'top_3_cases': [[756, 742, 739]], 'last_data': [{'date': '2020-04-15', 'cases': 756}]})
('Puglia,Lecce', {'cases_statistics': [{'mean': 162.69230769230768, 'variance': 26788.40532544379, 'stddev': 163.6716387326888}], 'top_3_cases': [[426, 425, 424]], 'last_data': [{'date': '2020-04-15', 'cases': 426}]})
('Puglia,Taranto', {'cases_statistics': [{'mean': 76.15384615384616, 'variance': 7062.860946745561, 'stddev': 84.04082904603905}], 'top_3_cases': [[228, 226, 225]], 'last_data': [{'date': '2020-04-15', 'cases': 228}]})
('Sardegna,Cagliari', {'cases_statistics': [{'mean': 69.1923076923077, 'variance': 4600.3091715976325, 'stddev': 67.82557903621341}], 'top_3_cases': [[207, 201, 197]], 'last_data': [{'date': '2020-04-15', 'cases': 207}]})
('Sardegna,Nuoro', {'cases_statistics': [{'mean': 31.307692307692307, 'variance': 716.4437869822485, 'stddev': 26.766467585063378}], 'top_3_cases': [[67, 67, 67]], 'last_data': [{'date': '2020-04-15', 'cases': 67}]})
('Sardegna,Oristano', {'cases_statistics': [{'mean': 10.115384615384615, 'variance': 148.3713017751479, 'stddev': 12.180775910226242}], 'top_3_cases': [[38, 35, 35]], 'last_data': [{'date': '2020-04-15', 'cases': 38}]})
('Sardegna,Sassari', {'cases_statistics': [{'mean': 272.53846153846155, 'variance': 78103.63313609468, 'stddev': 279.47027236558574}], 'top_3_cases': [[763, 749, 745]], 'last_data': [{'date': '2020-04-15', 'cases': 763}]})
('Sardegna,Sud Sardegna', {'cases_statistics': [{'mean': 29.21153846153846, 'variance': 1097.1283284023668, 'stddev': 33.122927533694345}], 'top_3_cases': [[86, 86, 84]], 'last_data': [{'date': '2020-04-15', 'cases': 86}]})
('Sicilia,Agrigento', {'cases_statistics': [{'mean': 49.71153846153846, 'variance': 2210.3975591715975, 'stddev': 47.014865299941015}], 'top_3_cases': [[131, 130, 128]], 'last_data': [{'date': '2020-04-15', 'cases': 131}]})
('Sicilia,Caltanissetta', {'cases_statistics': [{'mean': 42.71153846153846, 'variance': 2262.359097633136, 'stddev': 47.564262820242845}], 'top_3_cases': [[137, 135, 131]], 'last_data': [{'date': '2020-04-15', 'cases': 137}]})
('Sicilia,Catania', {'cases_statistics': [{'mean': 275.13461538461536, 'variance': 69677.8857248521, 'stddev': 263.96569043126055}], 'top_3_cases': [[725, 715, 704]], 'last_data': [{'date': '2020-04-15', 'cases': 725}]})
('Sicilia,Enna', {'cases_statistics': [{'mean': 111.5, 'variance': 16834.326923076922, 'stddev': 129.74716537588372}], 'top_3_cases': [[340, 335, 327]], 'last_data': [{'date': '2020-04-15', 'cases': 340}]})
('Sicilia,Messina', {'cases_statistics': [{'mean': 157.0, 'variance': 28872.46153846154, 'stddev': 169.91898522078554}], 'top_3_cases': [[449, 439, 436]], 'last_data': [{'date': '2020-04-15', 'cases': 449}]})
('Sicilia,Palermo', {'cases_statistics': [{'mean': 143.30769230769232, 'variance': 20327.86686390532, 'stddev': 142.5758284699946}], 'top_3_cases': [[393, 391, 385]], 'last_data': [{'date': '2020-04-15', 'cases': 393}]})
('Sicilia,Ragusa', {'cases_statistics': [{'mean': 22.076923076923077, 'variance': 601.4171597633137, 'stddev': 24.523808019214997}], 'top_3_cases': [[68, 67, 67]], 'last_data': [{'date': '2020-04-15', 'cases': 68}]})
('Sicilia,Siracusa', {'cases_statistics': [{'mean': 54.46153846153846, 'variance': 2877.479289940829, 'stddev': 53.642140989531995}], 'top_3_cases': [[158, 156, 149]], 'last_data': [{'date': '2020-04-15', 'cases': 158}]})
('Sicilia,Trapani', {'cases_statistics': [{'mean': 44.96153846153846, 'variance': 2221.883136094675, 'stddev': 47.136855390391446}], 'top_3_cases': [[134, 133, 131]], 'last_data': [{'date': '2020-04-15', 'cases': 134}]})
('Toscana,Arezzo', {'cases_statistics': [{'mean': 180.53846153846155, 'variance': 29632.32544378698, 'stddev': 172.14042361916907}], 'top_3_cases': [[522, 487, 453]], 'last_data': [{'date': '2020-04-15', 'cases': 522}]})
('Toscana,Firenze', {'cases_statistics': [{'mean': 747.2307692307693, 'variance': 641972.5621301773, 'stddev': 801.2319028409798}], 'top_3_cases': [[2372, 2311, 2269]], 'last_data': [{'date': '2020-04-15', 'cases': 2372}]})
('Toscana,Grosseto', {'cases_statistics': [{'mean': 135.3846153846154, 'variance': 16795.23668639053, 'stddev': 129.59643778434085}], 'top_3_cases': [[368, 368, 368]], 'last_data': [{'date': '2020-04-15', 'cases': 368}]})
('Toscana,Livorno', {'cases_statistics': [{'mean': 153.17307692307693, 'variance': 21819.489275147924, 'stddev': 147.7142148716498}], 'top_3_cases': [[415, 410, 404]], 'last_data': [{'date': '2020-04-15', 'cases': 415}]})
('Toscana,Lucca', {'cases_statistics': [{'mean': 406.9807692307692, 'variance': 154486.1727071006, 'stddev': 393.0472906751815}], 'top_3_cases': [[1073, 1061, 1060]], 'last_data': [{'date': '2020-04-15', 'cases': 1073}]})
('Toscana,Massa Carrara', {'cases_statistics': [{'mean': 324.03846153846155, 'variance': 98167.03698224851, 'stddev': 313.3161932972002}], 'top_3_cases': [[881, 873, 867]], 'last_data': [{'date': '2020-04-15', 'cases': 881}]})
('Toscana,Pisa', {'cases_statistics': [{'mean': 264.4807692307692, 'variance': 64113.518860946744, 'stddev': 253.20647476110628}], 'top_3_cases': [[733, 727, 694]], 'last_data': [{'date': '2020-04-15', 'cases': 733}]})
('Toscana,Pistoia', {'cases_statistics': [{'mean': 199.8653846153846, 'variance': 32893.96264792899, 'stddev': 181.3669282088909}], 'top_3_cases': [[516, 513, 509]], 'last_data': [{'date': '2020-04-15', 'cases': 516}]})
('Toscana,Prato', {'cases_statistics': [{'mean': 150.26923076923077, 'variance': 21861.004437869822, 'stddev': 147.85467337175996}], 'top_3_cases': [[411, 404, 394]], 'last_data': [{'date': '2020-04-15', 'cases': 411}]})
('Toscana,Siena', {'cases_statistics': [{'mean': 162.71153846153845, 'variance': 21016.359097633136, 'stddev': 144.9702007228835}], 'top_3_cases': [[375, 373, 372]], 'last_data': [{'date': '2020-04-15', 'cases': 375}]})
('P.A. Trento,Trento', {'cases_statistics': [{'mean': 1090.673076923077, 'variance': 1213190.5277366864, 'stddev': 1101.4492851405762}], 'top_3_cases': [[3220, 3141, 3126]], 'last_data': [{'date': '2020-04-15', 'cases': 3220}]})
('Umbria,Perugia', {'cases_statistics': [{'mean': 415.13461538461536, 'variance': 157902.73187869822, 'stddev': 397.3697671925963}], 'top_3_cases': [[958, 957, 956]], 'last_data': [{'date': '2020-04-15', 'cases': 958}]})
('Umbria,Terni', {'cases_statistics': [{'mean': 132.78846153846155, 'variance': 14439.628328402367, 'stddev': 120.16500459119688}], 'top_3_cases': [[317, 317, 317]], 'last_data': [{'date': '2020-04-15', 'cases': 317}]})
("Valle d'Aosta,Aosta", {'cases_statistics': [{'mean': 357.59615384615387, 'variance': 123208.47152366863, 'stddev': 351.01064303474993}], 'top_3_cases': [[958, 947, 927]], 'last_data': [{'date': '2020-04-15', 'cases': 958}]})
('Veneto,Belluno', {'cases_statistics': [{'mean': 260.96153846153845, 'variance': 61311.69082840238, 'stddev': 247.61197634283036}], 'top_3_cases': [[723, 698, 686]], 'last_data': [{'date': '2020-04-15', 'cases': 723}]})
('Veneto,Padova', {'cases_statistics': [{'mean': 1405.8846153846155, 'variance': 1408016.7559171594, 'stddev': 1186.598818437453}], 'top_3_cases': [[3450, 3407, 3354]], 'last_data': [{'date': '2020-04-15', 'cases': 3450}]})
('Veneto,Rovigo', {'cases_statistics': [{'mean': 94.46153846153847, 'variance': 9478.248520710058, 'stddev': 97.35629676970082}], 'top_3_cases': [[291, 287, 280]], 'last_data': [{'date': '2020-04-15', 'cases': 291}]})
('Veneto,Treviso', {'cases_statistics': [{'mean': 889.8076923076923, 'variance': 542970.6168639055, 'stddev': 736.8653994210241}], 'top_3_cases': [[2033, 2032, 1983]], 'last_data': [{'date': '2020-04-15', 'cases': 2033}]})
('Veneto,Venezia', {'cases_statistics': [{'mean': 753.3076923076923, 'variance': 446412.4822485207, 'stddev': 668.1410646327022}], 'top_3_cases': [[2013, 2008, 1983]], 'last_data': [{'date': '2020-04-15', 'cases': 2013}]})
('Veneto,Verona', {'cases_statistics': [{'mean': 1265.3846153846155, 'variance': 1587182.8520710059, 'stddev': 1259.8344542323828}], 'top_3_cases': [[3649, 3572, 3547]], 'last_data': [{'date': '2020-04-15', 'cases': 3649}]})
('Veneto,Vicenza', {'cases_statistics': [{'mean': 765.7884615384615, 'variance': 561214.3590976332, 'stddev': 749.1424157646082}], 'top_3_cases': [[2136, 2089, 2080]], 'last_data': [{'date': '2020-04-15', 'cases': 2136}]})
```
