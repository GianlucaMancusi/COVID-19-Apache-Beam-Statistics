# COVID-19 Apache Beam statistics on Google Dataflow
Statistical processing of COVID-19 data using Apache Beam for Google Cloud Dataflow in Python. Project for the exam of "Sistemi ed Applicazioni Cloud" (2019-20), *Magistrale di Ingegneria Informatica at the Dipartimento di Ingegneria Enzo Ferrari*.

## How to install
Run the *pip* command to download all the dependencies in the *requirements.txt* using your preferred virtualenv:<br>
`pip install -r requirements.txt`

## Accepted dataset
The type of data accepted follows the data scheme by province proposed by the repository [pcm-dpc/COVID-19](https://github.com/pcm-dpc/COVID-19) Italian. In particular, the file on which it runs is the following: [dpc-covid19-ita-province.csv](https://github.com/pcm-dpc/COVID-19/blob/master/dati-province/dpc-covid19-ita-province.csv)

## Input CLI
```
usage: covid_pipeline.py [-h] [--input INPUT] [--output OUTPUT] [--ntop NTOP]

optional arguments:
  -h, --help       show this help message and exit
  --input INPUT    Input dataset for the pipeline
  --output OUTPUT  Output file name for the pipeline
  --ntop NTOP      Number of top day cases to show
```

### Input dataset format: Data by Province
**Directory:**  datasets<br>
**Overall file:** dpc-covid19-ita-province.csv<br>
Notice: this table is taken from [pcm-dpc/COVID-19](https://github.com/pcm-dpc/COVID-19) italian repository.

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

## The output
The output is printed as [JSON Lines](http://jsonlines.org/examples/) format.
An example of output is the following, for each Region-Province:
```json
...
["Emilia-Romagna,Modena", {"cases_statistics": [{"mean": 1320.6851851851852, "variance": 1472316.4749657065, "stddev": 1213.3904874217972}], "top_3_cases": [[3301, 3262, 3217]], "last_data": [{"date": "2020-04-17", "cases": 3301}]}]
...
```

The meaning of the fields is as follows:
```json
...
["REGION,PROVINCE", {"cases_statistics": [{"mean": MEAN, "variance": VARIANCE, "stddev": STANDARD_DEV}], "top_<ntop>_cases": [[TOP_1, TOP_2,...., TOP_N]], "last_data": [{"date": "LAST_UPDATE_DATA", "cases": LAST_TOTAL_CASES}]}]
...
```

### Pipeline result on Google Dataflow
![Pipeline on Google Dataflow](https://raw.githubusercontent.com/GianlucaMancusi/COVID-19-Apache-Beam-Statistics/master/readme_images/pipeline.png)

### Complete output example
```json
["Abruzzo,Chieti", {"cases_statistics": [{"mean": 168.59259259259258, "variance": 30226.167352537726, "stddev": 173.85674376491045}], "top_3_cases": [[553, 499, 469]], "last_data": [{"date": "2020-04-17", "cases": 553}]}]
["Abruzzo,L'Aquila", {"cases_statistics": [{"mean": 79.79629629629629, "variance": 7423.939986282579, "stddev": 86.16228865508727}], "top_3_cases": [[233, 232, 229]], "last_data": [{"date": "2020-04-17", "cases": 233}]}]
["Abruzzo,Pescara", {"cases_statistics": [{"mean": 372.6666666666667, "variance": 125296.44444444441, "stddev": 353.97237808117796}], "top_3_cases": [[1042, 1005, 971]], "last_data": [{"date": "2020-04-17", "cases": 1042}]}]
["Abruzzo,Teramo", {"cases_statistics": [{"mean": 220.92592592592592, "variance": 55050.40192043896, "stddev": 234.62822063945967}], "top_3_cases": [[615, 610, 605]], "last_data": [{"date": "2020-04-17", "cases": 615}]}]
["Basilicata,Matera", {"cases_statistics": [{"mean": 56.75925925925926, "variance": 4136.738340192044, "stddev": 64.31748082902536}], "top_3_cases": [[170, 169, 155]], "last_data": [{"date": "2020-04-17", "cases": 170}]}]
["Basilicata,Potenza", {"cases_statistics": [{"mean": 69.05555555555556, "variance": 4353.941358024691, "stddev": 65.98440238438695}], "top_3_cases": [[167, 167, 165]], "last_data": [{"date": "2020-04-17", "cases": 167}]}]
["P.A. Bolzano,Bolzano", {"cases_statistics": [{"mean": 839.5370370370371, "variance": 659240.1004801097, "stddev": 811.9360199425258}], "top_3_cases": [[2296, 2267, 2224]], "last_data": [{"date": "2020-04-17", "cases": 2296}]}]
["Calabria,Catanzaro", {"cases_statistics": [{"mean": 72.85185185185185, "variance": 5652.089163237312, "stddev": 75.18037751459694}], "top_3_cases": [[195, 194, 190]], "last_data": [{"date": "2020-04-17", "cases": 195}]}]
["Calabria,Cosenza", {"cases_statistics": [{"mean": 113.12962962962963, "variance": 14344.557270233194, "stddev": 119.76876583748032}], "top_3_cases": [[367, 357, 318]], "last_data": [{"date": "2020-04-17", "cases": 367}]}]
["Calabria,Crotone", {"cases_statistics": [{"mean": 53.7037037037037, "variance": 2310.986282578875, "stddev": 48.072718693442695}], "top_3_cases": [[117, 117, 117]], "last_data": [{"date": "2020-04-17", "cases": 117}]}]
["Calabria,Reggio di Calabria", {"cases_statistics": [{"mean": 110.12962962962963, "variance": 11111.668381344307, "stddev": 105.41189867061644}], "top_3_cases": [[276, 269, 268]], "last_data": [{"date": "2020-04-17", "cases": 240}]}]
["Calabria,Vibo Valentia", {"cases_statistics": [{"mean": 26.64814814814815, "variance": 710.005829903978, "stddev": 26.645934584922667}], "top_3_cases": [[70, 70, 68]], "last_data": [{"date": "2020-04-17", "cases": 70}]}]
["Campania,Avellino", {"cases_statistics": [{"mean": 161.57407407407408, "variance": 25366.72599451303, "stddev": 159.26935045548794}], "top_3_cases": [[423, 416, 407]], "last_data": [{"date": "2020-04-17", "cases": 423}]}]
["Campania,Benevento", {"cases_statistics": [{"mean": 46.7962962962963, "variance": 3563.643689986283, "stddev": 59.69626194315924}], "top_3_cases": [[164, 157, 157]], "last_data": [{"date": "2020-04-17", "cases": 164}]}]
["Campania,Caserta", {"cases_statistics": [{"mean": 151.92592592592592, "variance": 20036.58710562414, "stddev": 141.5506520847719}], "top_3_cases": [[393, 393, 390]], "last_data": [{"date": "2020-04-17", "cases": 393}]}]
["Campania,Napoli", {"cases_statistics": [{"mean": 731.3888888888889, "variance": 532379.3858024691, "stddev": 729.6433277995962}], "top_3_cases": [[2109, 2072, 2026]], "last_data": [{"date": "2020-04-17", "cases": 2109}]}]
["Campania,Salerno", {"cases_statistics": [{"mean": 214.72222222222223, "variance": 45202.53395061729, "stddev": 212.6088755217366}], "top_3_cases": [[599, 587, 564]], "last_data": [{"date": "2020-04-17", "cases": 599}]}]
["Emilia-Romagna,Bologna", {"cases_statistics": [{"mean": 1222.5555555555557, "variance": 1556419.172839506, "stddev": 1247.5652980263221}], "top_3_cases": [[3619, 3490, 3380]], "last_data": [{"date": "2020-04-17", "cases": 3619}]}]
["Emilia-Romagna,Ferrara", {"cases_statistics": [{"mean": 226.57407407407408, "variance": 57960.98525377228, "stddev": 240.75087799169557}], "top_3_cases": [[744, 709, 649]], "last_data": [{"date": "2020-04-17", "cases": 744}]}]
["Emilia-Romagna,Forl\u00ec-Cesena", {"cases_statistics": [{"mean": 470.55555555555554, "variance": 226322.83950617287, "stddev": 475.7340007884373}], "top_3_cases": [[1380, 1347, 1324]], "last_data": [{"date": "2020-04-17", "cases": 1380}]}]
["Emilia-Romagna,Modena", {"cases_statistics": [{"mean": 1320.6851851851852, "variance": 1472316.4749657065, "stddev": 1213.3904874217972}], "top_3_cases": [[3301, 3262, 3217]], "last_data": [{"date": "2020-04-17", "cases": 3301}]}]
["Emilia-Romagna,Parma", {"cases_statistics": [{"mean": 1232.9259259259259, "variance": 920155.8093278466, "stddev": 959.247522450721}], "top_3_cases": [[2725, 2698, 2616]], "last_data": [{"date": "2020-04-17", "cases": 2725}]}]
["Emilia-Romagna,Piacenza", {"cases_statistics": [{"mean": 1666.851851851852, "variance": 1325836.7558299033, "stddev": 1151.4498494636678}], "top_3_cases": [[3274, 3249, 3223]], "last_data": [{"date": "2020-04-17", "cases": 3274}]}]
["Emilia-Romagna,Ravenna", {"cases_statistics": [{"mean": 352.9259259259259, "variance": 107512.84636488341, "stddev": 327.89151615264984}], "top_3_cases": [[910, 904, 889]], "last_data": [{"date": "2020-04-17", "cases": 910}]}]
["Emilia-Romagna,Reggio nell'Emilia", {"cases_statistics": [{"mean": 1494.2407407407406, "variance": 2219186.256858711, "stddev": 1489.6933432283006}], "top_3_cases": [[4090, 4053, 3982]], "last_data": [{"date": "2020-04-17", "cases": 4090}]}]
["Emilia-Romagna,Rimini", {"cases_statistics": [{"mean": 857.6296296296297, "variance": 440659.8628257887, "stddev": 663.8221620477797}], "top_3_cases": [[1791, 1774, 1749]], "last_data": [{"date": "2020-04-17", "cases": 1791}]}]
["Friuli Venezia Giulia,Gorizia", {"cases_statistics": [{"mean": 57.2037037037037, "variance": 2524.1622085048016, "stddev": 50.24104107703981}], "top_3_cases": [[132, 132, 130]], "last_data": [{"date": "2020-04-17", "cases": 132}]}]
["Friuli Venezia Giulia,Pordenone", {"cases_statistics": [{"mean": 226.87037037037038, "variance": 48438.18689986282, "stddev": 220.08677129682926}], "top_3_cases": [[574, 573, 557]], "last_data": [{"date": "2020-04-17", "cases": 574}]}]
["Friuli Venezia Giulia,Trieste", {"cases_statistics": [{"mean": 363.462962962963, "variance": 115884.47085048008, "stddev": 340.4180824375816}], "top_3_cases": [[1067, 1011, 961]], "last_data": [{"date": "2020-04-17", "cases": 1067}]}]
["Friuli Venezia Giulia,Udine", {"cases_statistics": [{"mean": 376.0740740740741, "variance": 115351.73525377229, "stddev": 339.6347085528396}], "top_3_cases": [[897, 895, 891]], "last_data": [{"date": "2020-04-17", "cases": 897}]}]
["Lazio,Frosinone", {"cases_statistics": [{"mean": 175.1851851851852, "variance": 34869.78052126201, "stddev": 186.7345188262256}], "top_3_cases": [[502, 497, 479]], "last_data": [{"date": "2020-04-17", "cases": 502}]}]
["Lazio,Latina", {"cases_statistics": [{"mean": 161.61111111111111, "variance": 25405.53395061728, "stddev": 159.39113510674702}], "top_3_cases": [[430, 421, 419]], "last_data": [{"date": "2020-04-17", "cases": 430}]}]
["Lazio,Rieti", {"cases_statistics": [{"mean": 91.07407407407408, "variance": 12454.216735253773, "stddev": 111.59846206491277}], "top_3_cases": [[278, 277, 277]], "last_data": [{"date": "2020-04-17", "cases": 278}]}]
["Lazio,Roma", {"cases_statistics": [{"mean": 1363.7407407407406, "variance": 1723717.9327846367, "stddev": 1312.9043882875237}], "top_3_cases": [[3888, 3767, 3665]], "last_data": [{"date": "2020-04-17", "cases": 3888}]}]
["Lazio,Viterbo", {"cases_statistics": [{"mean": 119.46296296296296, "variance": 14875.618998628257, "stddev": 121.96564679707257}], "top_3_cases": [[346, 338, 326]], "last_data": [{"date": "2020-04-17", "cases": 346}]}]
["Liguria,Genova", {"cases_statistics": [{"mean": 1009.2962962962963, "variance": 1353509.4307270234, "stddev": 1163.4042421819784}], "top_3_cases": [[3557, 3522, 3487]], "last_data": [{"date": "2020-04-17", "cases": 3557}]}]
["Liguria,Imperia", {"cases_statistics": [{"mean": 279.25925925925924, "variance": 119034.30315500688, "stddev": 345.0134825698945}], "top_3_cases": [[1083, 1048, 1036]], "last_data": [{"date": "2020-04-17", "cases": 1083}]}]
["Liguria,La Spezia", {"cases_statistics": [{"mean": 215.38888888888889, "variance": 60152.23765432099, "stddev": 245.25953122013627}], "top_3_cases": [[725, 720, 696]], "last_data": [{"date": "2020-04-17", "cases": 725}]}]
["Liguria,Savona", {"cases_statistics": [{"mean": 257.3703703703704, "variance": 73948.01097393689, "stddev": 271.9338356548094}], "top_3_cases": [[812, 797, 797]], "last_data": [{"date": "2020-04-17", "cases": 812}]}]
["Lombardia,Bergamo", {"cases_statistics": [{"mean": 5434.722222222223, "variance": 15982127.311728396, "stddev": 3997.7652897247976}], "top_3_cases": [[10590, 10518, 10472]], "last_data": [{"date": "2020-04-17", "cases": 10590}]}]
["Lombardia,Brescia", {"cases_statistics": [{"mean": 5168.611111111111, "variance": 17431862.34876543, "stddev": 4175.1481828511705}], "top_3_cases": [[11567, 11355, 11187]], "last_data": [{"date": "2020-04-17", "cases": 11567}]}]
["Lombardia,Como", {"cases_statistics": [{"mean": 731.8518518518518, "variance": 545330.3854595335, "stddev": 738.4648843780817}], "top_3_cases": [[2285, 2233, 2154]], "last_data": [{"date": "2020-04-17", "cases": 2285}]}]
["Lombardia,Cremona", {"cases_statistics": [{"mean": 2550.685185185185, "variance": 3117790.289780521, "stddev": 1765.7265614416408}], "top_3_cases": [[5313, 5273, 5202]], "last_data": [{"date": "2020-04-17", "cases": 5313}]}]
["Lombardia,Lecco", {"cases_statistics": [{"mean": 871.2222222222222, "variance": 566270.8024691358, "stddev": 752.5096693525844}], "top_3_cases": [[2005, 1986, 1982]], "last_data": [{"date": "2020-04-17", "cases": 2005}]}]
["Lombardia,Lodi", {"cases_statistics": [{"mean": 1535.2962962962963, "variance": 658387.801097394, "stddev": 811.4109939465906}], "top_3_cases": [[2678, 2626, 2587]], "last_data": [{"date": "2020-04-17", "cases": 2678}]}]
["Lombardia,Mantova", {"cases_statistics": [{"mean": 1054.1296296296296, "variance": 931285.5943072704, "stddev": 965.031395503416}], "top_3_cases": [[2748, 2691, 2655]], "last_data": [{"date": "2020-04-17", "cases": 2748}]}]
["Lombardia,Milano", {"cases_statistics": [{"mean": 5765.814814814815, "variance": 27957030.33607682, "stddev": 5287.440811590879}], "top_3_cases": [[15277, 14952, 14675]], "last_data": [{"date": "2020-04-17", "cases": 15277}]}]
["Lombardia,Monza e della Brianza", {"cases_statistics": [{"mean": 1477.8148148148148, "variance": 2102541.817558299, "stddev": 1450.0144197759894}], "top_3_cases": [[3975, 3932, 3878]], "last_data": [{"date": "2020-04-17", "cases": 3975}]}]
["Lombardia,Pavia", {"cases_statistics": [{"mean": 1420.9444444444443, "variance": 1332542.2006172843, "stddev": 1154.3579170332243}], "top_3_cases": [[3448, 3390, 3316]], "last_data": [{"date": "2020-04-17", "cases": 3448}]}]
["Lombardia,Sondrio", {"cases_statistics": [{"mean": 292.2037037037037, "variance": 88286.93998628258, "stddev": 297.1311831267169}], "top_3_cases": [[866, 864, 859]], "last_data": [{"date": "2020-04-17", "cases": 866}]}]
["Lombardia,Varese", {"cases_statistics": [{"mean": 628.5, "variance": 415903.3981481482, "stddev": 644.9057281092704}], "top_3_cases": [[2021, 1953, 1884]], "last_data": [{"date": "2020-04-17", "cases": 2021}]}]
["Marche,Ancona", {"cases_statistics": [{"mean": 696.0, "variance": 375032.2962962963, "stddev": 612.3988049435566}], "top_3_cases": [[1686, 1664, 1647]], "last_data": [{"date": "2020-04-17", "cases": 1686}]}]
["Marche,Ascoli Piceno", {"cases_statistics": [{"mean": 103.66666666666667, "variance": 11567.703703703703, "stddev": 107.55325984694143}], "top_3_cases": [[268, 266, 259]], "last_data": [{"date": "2020-04-17", "cases": 268}]}]
["Marche,Fermo", {"cases_statistics": [{"mean": 150.11111111111111, "variance": 20971.135802469136, "stddev": 144.8141422737059}], "top_3_cases": [[379, 378, 367]], "last_data": [{"date": "2020-04-17", "cases": 379}]}]
["Marche,Macerata", {"cases_statistics": [{"mean": 327.4259259259259, "variance": 96506.31858710563, "stddev": 310.6546612994977}], "top_3_cases": [[895, 871, 846]], "last_data": [{"date": "2020-04-17", "cases": 895}]}]
["Marche,Pesaro e Urbino", {"cases_statistics": [{"mean": 1086.037037037037, "variance": 652661.5171467764, "stddev": 807.8746914879661}], "top_3_cases": [[2277, 2249, 2230]], "last_data": [{"date": "2020-04-17", "cases": 2277}]}]
["Molise,Campobasso", {"cases_statistics": [{"mean": 77.16666666666667, "variance": 5352.583333333332, "stddev": 73.16135136349882}], "top_3_cases": [[202, 197, 197]], "last_data": [{"date": "2020-04-17", "cases": 202}]}]
["Molise,Isernia", {"cases_statistics": [{"mean": 14.185185185185185, "variance": 370.076817558299, "stddev": 19.237380735388562}], "top_3_cases": [[50, 50, 50]], "last_data": [{"date": "2020-04-17", "cases": 50}]}]
["Piemonte,Alessandria", {"cases_statistics": [{"mean": 903.3148148148148, "variance": 769388.6601508918, "stddev": 877.1480263620798}], "top_3_cases": [[2696, 2580, 2407]], "last_data": [{"date": "2020-04-17", "cases": 2696}]}]
["Piemonte,Asti", {"cases_statistics": [{"mean": 301.962962962963, "variance": 88378.25788751712, "stddev": 297.2848093790147}], "top_3_cases": [[957, 925, 897]], "last_data": [{"date": "2020-04-17", "cases": 957}]}]
["Piemonte,Biella", {"cases_statistics": [{"mean": 281.72222222222223, "variance": 71552.23765432098, "stddev": 267.49250018331537}], "top_3_cases": [[728, 719, 717]], "last_data": [{"date": "2020-04-17", "cases": 728}]}]
["Piemonte,Cuneo", {"cases_statistics": [{"mean": 528.9444444444445, "variance": 354576.4598765432, "stddev": 595.4632313388822}], "top_3_cases": [[1897, 1814, 1791]], "last_data": [{"date": "2020-04-17", "cases": 1897}]}]
["Piemonte,Novara", {"cases_statistics": [{"mean": 547.3333333333334, "variance": 343152.40740740736, "stddev": 585.7921196187325}], "top_3_cases": [[1855, 1825, 1708]], "last_data": [{"date": "2020-04-17", "cases": 1855}]}]
["Piemonte,Torino", {"cases_statistics": [{"mean": 2961.6111111111113, "variance": 9563641.163580246, "stddev": 3092.5137289234863}], "top_3_cases": [[9503, 9116, 8656]], "last_data": [{"date": "2020-04-17", "cases": 9503}]}]
["Piemonte,Verbano-Cusio-Ossola", {"cases_statistics": [{"mean": 292.9259259259259, "variance": 102700.17969821674, "stddev": 320.4686875471873}], "top_3_cases": [[917, 910, 904]], "last_data": [{"date": "2020-04-17", "cases": 917}]}]
["Piemonte,Vercelli", {"cases_statistics": [{"mean": 311.4259259259259, "variance": 95740.72599451304, "stddev": 309.4199831854967}], "top_3_cases": [[935, 912, 847]], "last_data": [{"date": "2020-04-17", "cases": 935}]}]
["Puglia,Bari", {"cases_statistics": [{"mean": 369.14814814814815, "variance": 143176.94101508916, "stddev": 378.3872897113342}], "top_3_cases": [[1050, 1029, 1013]], "last_data": [{"date": "2020-04-17", "cases": 1050}]}]
["Puglia,Barletta-Andria-Trani", {"cases_statistics": [{"mean": 89.79629629629629, "variance": 10977.56961591221, "stddev": 104.77389758862753}], "top_3_cases": [[333, 330, 315]], "last_data": [{"date": "2020-04-17", "cases": 333}]}]
["Puglia,Brindisi", {"cases_statistics": [{"mean": 131.64814814814815, "variance": 18772.70953360768, "stddev": 137.01353777495012}], "top_3_cases": [[439, 428, 417]], "last_data": [{"date": "2020-04-17", "cases": 439}]}]
["Puglia,Foggia", {"cases_statistics": [{"mean": 286.037037037037, "variance": 80705.14677640607, "stddev": 284.08651283791363}], "top_3_cases": [[807, 780, 756]], "last_data": [{"date": "2020-04-17", "cases": 807}]}]
["Puglia,Lecce", {"cases_statistics": [{"mean": 172.61111111111111, "variance": 28354.64506172839, "stddev": 168.38837567281297}], "top_3_cases": [[434, 427, 426]], "last_data": [{"date": "2020-04-17", "cases": 434}]}]
["Puglia,Taranto", {"cases_statistics": [{"mean": 82.03703703703704, "variance": 7701.183813443073, "stddev": 87.75638901779786}], "top_3_cases": [[235, 235, 228]], "last_data": [{"date": "2020-04-17", "cases": 235}]}]
["Sardegna,Cagliari", {"cases_statistics": [{"mean": 74.38888888888889, "variance": 5132.126543209878, "stddev": 71.63886196199573}], "top_3_cases": [[211, 208, 207]], "last_data": [{"date": "2020-04-17", "cases": 211}]}]
["Sardegna,Nuoro", {"cases_statistics": [{"mean": 32.629629629629626, "variance": 735.3443072702332, "stddev": 27.11723266246453}], "top_3_cases": [[67, 67, 67]], "last_data": [{"date": "2020-04-17", "cases": 67}]}]
["Sardegna,Oristano", {"cases_statistics": [{"mean": 11.203703703703704, "variance": 173.6807270233196, "stddev": 13.178798390722866}], "top_3_cases": [[40, 39, 38]], "last_data": [{"date": "2020-04-17", "cases": 40}]}]
["Sardegna,Sassari", {"cases_statistics": [{"mean": 290.9259259259259, "variance": 84002.40192043895, "stddev": 289.8316786005956}], "top_3_cases": [[774, 764, 763]], "last_data": [{"date": "2020-04-17", "cases": 774}]}]
["Sardegna,Sud Sardegna", {"cases_statistics": [{"mean": 31.314814814814813, "variance": 1171.5120027434841, "stddev": 34.22735751914664}], "top_3_cases": [[86, 86, 86]], "last_data": [{"date": "2020-04-17", "cases": 86}]}]
["Sicilia,Agrigento", {"cases_statistics": [{"mean": 52.75925925925926, "variance": 2370.03463648834, "stddev": 48.68300151478275}], "top_3_cases": [[132, 132, 131]], "last_data": [{"date": "2020-04-17", "cases": 132}]}]
["Sicilia,Caltanissetta", {"cases_statistics": [{"mean": 46.24074074074074, "variance": 2502.4050068587107, "stddev": 50.024044287309586}], "top_3_cases": [[138, 138, 137]], "last_data": [{"date": "2020-04-17", "cases": 138}]}]
["Sicilia,Catania", {"cases_statistics": [{"mean": 292.35185185185185, "variance": 74805.41323731138, "stddev": 273.5057828224321}], "top_3_cases": [[745, 735, 725]], "last_data": [{"date": "2020-04-17", "cases": 745}]}]
["Sicilia,Enna", {"cases_statistics": [{"mean": 120.31481481481481, "variance": 18233.73422496571, "stddev": 135.03234510651774}], "top_3_cases": [[358, 341, 340]], "last_data": [{"date": "2020-04-17", "cases": 358}]}]
["Sicilia,Messina", {"cases_statistics": [{"mean": 168.27777777777777, "variance": 31111.126543209877, "stddev": 176.38346448352203}], "top_3_cases": [[467, 456, 449]], "last_data": [{"date": "2020-04-17", "cases": 467}]}]
["Sicilia,Palermo", {"cases_statistics": [{"mean": 152.87037037037038, "variance": 21952.779492455415, "stddev": 148.16470393604348}], "top_3_cases": [[404, 399, 393]], "last_data": [{"date": "2020-04-17", "cases": 404}]}]
["Sicilia,Ragusa", {"cases_statistics": [{"mean": 23.814814814814813, "variance": 657.6694101508917, "stddev": 25.645066000127425}], "top_3_cases": [[69, 69, 68]], "last_data": [{"date": "2020-04-17", "cases": 69}]}]
["Sicilia,Siracusa", {"cases_statistics": [{"mean": 58.94444444444444, "variance": 3293.496913580247, "stddev": 57.388996450367095}], "top_3_cases": [[177, 174, 158]], "last_data": [{"date": "2020-04-17", "cases": 177}]}]
["Sicilia,Trapani", {"cases_statistics": [{"mean": 48.2962962962963, "variance": 2428.7270233196155, "stddev": 49.28211666841853}], "top_3_cases": [[135, 135, 134]], "last_data": [{"date": "2020-04-17", "cases": 135}]}]
["Toscana,Arezzo", {"cases_statistics": [{"mean": 193.6851851851852, "variance": 33029.697187928665, "stddev": 181.74074168421527}], "top_3_cases": [[541, 530, 522]], "last_data": [{"date": "2020-04-17", "cases": 541}]}]
["Toscana,Firenze", {"cases_statistics": [{"mean": 810.9814814814815, "variance": 723887.8700274347, "stddev": 850.8160024514317}], "top_3_cases": [[2494, 2443, 2372]], "last_data": [{"date": "2020-04-17", "cases": 2494}]}]
["Toscana,Grosseto", {"cases_statistics": [{"mean": 144.14814814814815, "variance": 18170.570644718795, "stddev": 134.79825905670592}], "top_3_cases": [[376, 368, 368]], "last_data": [{"date": "2020-04-17", "cases": 376}]}]
["Toscana,Livorno", {"cases_statistics": [{"mean": 164.90740740740742, "variance": 24592.34327846365, "stddev": 156.81946077723788}], "top_3_cases": [[475, 465, 415]], "last_data": [{"date": "2020-04-17", "cases": 475}]}]
["Toscana,Lucca", {"cases_statistics": [{"mean": 434.35185185185185, "variance": 168248.37620027436, "stddev": 410.1809066744506}], "top_3_cases": [[1158, 1134, 1073]], "last_data": [{"date": "2020-04-17", "cases": 1158}]}]
["Toscana,Massa Carrara", {"cases_statistics": [{"mean": 345.462962962963, "variance": 106468.80418381341, "stddev": 326.2955779409421}], "top_3_cases": [[912, 893, 881]], "last_data": [{"date": "2020-04-17", "cases": 912}]}]
["Toscana,Pisa", {"cases_statistics": [{"mean": 282.75925925925924, "variance": 70427.99759945131, "stddev": 265.3827379455026}], "top_3_cases": [[766, 750, 733]], "last_data": [{"date": "2020-04-17", "cases": 766}]}]
["Toscana,Pistoia", {"cases_statistics": [{"mean": 212.5185185185185, "variance": 35839.43484224967, "stddev": 189.31306041118683}], "top_3_cases": [[547, 536, 516]], "last_data": [{"date": "2020-04-17", "cases": 547}]}]
["Toscana,Prato", {"cases_statistics": [{"mean": 161.16666666666666, "variance": 24139.69444444445, "stddev": 155.36954155961345}], "top_3_cases": [[449, 440, 411]], "last_data": [{"date": "2020-04-17", "cases": 449}]}]
["Toscana,Siena", {"cases_statistics": [{"mean": 171.05555555555554, "variance": 22048.756172839516, "stddev": 148.48823580620626}], "top_3_cases": [[392, 384, 375]], "last_data": [{"date": "2020-04-17", "cases": 392}]}]
["P.A. Trento,Trento", {"cases_statistics": [{"mean": 1173.7962962962963, "variance": 1347966.0140603567, "stddev": 1161.0193857383936}], "top_3_cases": [[3376, 3294, 3220]], "last_data": [{"date": "2020-04-17", "cases": 3376}]}]
["Umbria,Perugia", {"cases_statistics": [{"mean": 435.5, "variance": 162838.10185185185, "stddev": 403.5320332412928}], "top_3_cases": [[967, 963, 958]], "last_data": [{"date": "2020-04-17", "cases": 967}]}]
["Umbria,Terni", {"cases_statistics": [{"mean": 139.72222222222223, "variance": 15154.978395061731, "stddev": 123.1055579373317}], "top_3_cases": [[322, 318, 317]], "last_data": [{"date": "2020-04-17", "cases": 322}]}]
["Valle d'Aosta,Aosta", {"cases_statistics": [{"mean": 380.72222222222223, "variance": 132554.8672839506, "stddev": 364.0808526741699}], "top_3_cases": [[993, 971, 958]], "last_data": [{"date": "2020-04-17", "cases": 993}]}]
["Veneto,Belluno", {"cases_statistics": [{"mean": 280.22222222222223, "variance": 68711.24691358024, "stddev": 262.1283023894601}], "top_3_cases": [[807, 755, 723]], "last_data": [{"date": "2020-04-17", "cases": 807}]}]
["Veneto,Padova", {"cases_statistics": [{"mean": 1485.8148148148148, "variance": 1522004.7434842247, "stddev": 1233.6955635343043}], "top_3_cases": [[3591, 3537, 3450]], "last_data": [{"date": "2020-04-17", "cases": 3591}]}]
["Veneto,Rovigo", {"cases_statistics": [{"mean": 102.03703703703704, "variance": 10619.443072702332, "stddev": 103.0506820584043}], "top_3_cases": [[301, 297, 291]], "last_data": [{"date": "2020-04-17", "cases": 301}]}]
["Veneto,Treviso", {"cases_statistics": [{"mean": 937.8148148148148, "variance": 582878.7064471879, "stddev": 763.4649346546231}], "top_3_cases": [[2237, 2135, 2033]], "last_data": [{"date": "2020-04-17", "cases": 2237}]}]
["Veneto,Venezia", {"cases_statistics": [{"mean": 801.925925925926, "variance": 491369.0685871056, "stddev": 700.9772240145222}], "top_3_cases": [[2096, 2036, 2013]], "last_data": [{"date": "2020-04-17", "cases": 2096}]}]
["Veneto,Verona", {"cases_statistics": [{"mean": 1358.0555555555557, "variance": 1751735.8672839503, "stddev": 1323.531589076721}], "top_3_cases": [[3805, 3730, 3649]], "last_data": [{"date": "2020-04-17", "cases": 3805}]}]
["Veneto,Vicenza", {"cases_statistics": [{"mean": 818.3518518518518, "variance": 612272.6354595338, "stddev": 782.4785207656079}], "top_3_cases": [[2200, 2170, 2136]], "last_data": [{"date": "2020-04-17", "cases": 2200}]}]
```

### Execution on Google Dataflow
In order to execute the pipeline on Dataflow you have to store the csv input on Google Cloud Storage and execute the following command:
```powershell
python .\covid_pipeline.py --project PROJECT_NAME --runner DataflowRunner --temp_location gs://GOOGLE_STORAGE/temp --output gs://GOOGLE_STORAGE/results/output --job_name dataflow-covid --input gs://GOOGLE_STORAGE/dpc-covid19-ita-province.csv --region europe-west2
```
more info [here](https://cloud.google.com/dataflow/docs/quickstarts/quickstart-python).

### Author
- *Gianluca Mancusi*
