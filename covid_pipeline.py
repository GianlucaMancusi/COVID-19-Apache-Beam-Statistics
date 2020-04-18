# MIT License
# Copyright (c) 2020 Gianluca Mancusi

import apache_beam as beam
import numpy as np
import json

# All the data extraction and data processing logic is present in these files
from components import covid_options
from components import par_do as CovidParDo
from components import combines as CovidCombines


def covid_pipeline():
    """
    Statistical processing of COVID-19 data using Apache Beam for Google Cloud Dataflow in Python. 
    Project for the exam of "Sistemi ed Applicazioni Cloud" (2019-20), 
    Magistrale di Ingegneria Informatica at the Dipartimento di Ingegneria Enzo Ferrari.

    see more: https://github.com/GianlucaMancusi/COVID-19-Apache-Beam-Statistics
    """
    options = covid_options.CovidOptions()
    with beam.Pipeline(options=options) as p:
        csv_formatted_data = (p
                              | "Reading the input dataset" >> beam.io.ReadFromText(options.input, skip_header_lines=1)
                              | "Splitting the data row by row" >> beam.ParDo(CovidParDo.Split())
                              | "Deleting data not up to date" >> beam.ParDo(CovidParDo.DeleteDataNotUpToDate())
                              )

        grouped_by_location = (csv_formatted_data
                               | "Colleting Location as Key" >> beam.ParDo(CovidParDo.CollectLocationKey())
                               | "Grouping by location" >> beam.GroupByKey()
                               )
        grouped_by_location_and_date = (csv_formatted_data
                                        | "Colleting Location and Date as Key" >> beam.ParDo(CovidParDo.CollectLocationKeyWithDate())
                                        | "Grouping by location with date" >> beam.GroupByKey()
                                        )

        variance_cases = (grouped_by_location
                          | "Calculating variance and stddev" >> beam.CombineValues(CovidCombines.MeanVarStddev())
                          )

        top_cases = (grouped_by_location
                     | "Calculating top 3" >> beam.CombineValues(beam.combiners.TopCombineFn(n=int(options.ntop)))
                     )

        last_dates = (grouped_by_location_and_date
                      | "Calculating last date and last cases" >> beam.CombineValues(CovidCombines.GetLastDatesOnly())
                      )

        output_pipe = (
            {
                'cases_statistics': variance_cases,
                f'top_{options.ntop}_cases': top_cases,
                'last_data': last_dates
            }
            | "CoGrouping by key" >> beam.CoGroupByKey()
            | 'format json' >> beam.Map(json.dumps)
            | "Writing out" >> beam.io.WriteToText(options.output))


if __name__ == "__main__":
    covid_pipeline()
