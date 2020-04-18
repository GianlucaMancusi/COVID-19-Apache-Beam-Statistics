# MIT License
# Copyright (c) 2020 Gianluca Mancusi

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import json


class CovidOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument('--input', help='Input dataset for the pipeline')
        parser.add_argument(
            '--output', help='Output JSON file name for the pipeline')
        parser.add_argument(
            '--ntop', type=int, help='Number of top day cases to show', default='3')


class Split(beam.DoFn):
    def process(self, element):
        data, __, ___, denominazione_regione, \
            ____, denominazione_provincia, \
            _____, ______, _______, total_cases, \
            ________, _________ = element.split(",")
        return [{'region': denominazione_regione,
                 'province': denominazione_provincia,
                 'date': data,
                 'total_cases': total_cases}]


class DeleteDataNotUpToDate(beam.DoFn):
    def process(self, element):
        return None if 'In fase di definizione/aggiornamento' in element["province"] else [element]


class CollectLocationKey(beam.DoFn):
    def process(self, element):
        return [(f"{element['region']},{element['province']}", int(element['total_cases']))]


class CollectLocationKeyWithDate(beam.DoFn):
    def process(self, element):
        from dateutil import parser
        cases_dates = (parser.parse(element['date']), int(
            element['total_cases']))
        region_province = f"{element['region']},{element['province']}"
        return [(region_province, cases_dates)]


class MeanVarStddev(beam.CombineFn):
    '''
    This CombineFn type function calculates mean,
    variance and standard deviation of the COVID-19 cases.
    '''

    def create_accumulator(self):
        return (0.0, 0.0, 0)  # x, x^2, count

    def add_input(self, sum_count, input):
        (sum, sumsq, count) = sum_count
        return sum + input, sumsq + input*input, count + 1

    def merge_accumulators(self, accumulators):
        sums, sumsqs, counts = zip(*accumulators)
        return sum(sums), sum(sumsqs), sum(counts)

    def extract_output(self, sum_count):
        import numpy as np
        (sum, sumsq, count) = sum_count
        mean, variance, stddev = 0, 0, 0
        if count:
            mean = sum / count
            variance = (sumsq / count) - mean*mean  # E(x^2) - E(x)*E(x)
            stddev = np.sqrt(variance) if variance > 0 else 0
        return {
            'mean': mean if count else float('NaN'),
            'variance': variance if count else float('NaN'),
            'stddev': stddev if count else float('NaN')
        }


class GetLastDatesOnly(beam.CombineFn):
    '''
    This CombineFn type function calculates the maximum date 
    and returns only that with the value of COVID-19 cases.
    '''

    def create_accumulator(self):
        from datetime import datetime
        return (datetime.min, 0.0)  # dates, cases

    def add_input(self, dates_cases, input):
        (max_date, cases_max_date) = dates_cases
        (input_date, input_cases) = input
        # only takes the most recent date with its number of cases
        return (max_date, cases_max_date) if max_date > input_date else (input_date, input_cases)

    def merge_accumulators(self, accumulators):
        import numpy as np
        (dates, cases) = zip(*accumulators)
        # takes the index of the most recent date
        index = np.argmax(dates)
        return (dates[index], cases[index])

    def extract_output(self, dates_cases):
        (date, cases) = dates_cases
        return {'date': "{:%Y-%m-%d}".format(date), 'cases': cases}


def covid_pipeline():
    """
    Statistical processing of COVID-19 data using Apache Beam for Google Cloud Dataflow in Python. 
    Project for the exam of "Sistemi ed Applicazioni Cloud" (2019-20), 
    Magistrale di Ingegneria Informatica at the Dipartimento di Ingegneria Enzo Ferrari.

    see more: https://github.com/GianlucaMancusi/COVID-19-Apache-Beam-Statistics
    """
    options = CovidOptions()
    with beam.Pipeline(options=options) as p:
        csv_formatted_data = (p
                              | "Reading the input dataset" >> beam.io.ReadFromText(options.input, skip_header_lines=1)
                              | "Splitting the data row by row" >> beam.ParDo(Split())
                              | "Deleting data not up to date" >> beam.ParDo(DeleteDataNotUpToDate())
                              )

        grouped_by_location = (csv_formatted_data
                               | "Colleting Location as Key" >> beam.ParDo(CollectLocationKey())
                               | "Grouping by location" >> beam.GroupByKey()
                               )
        grouped_by_location_and_date = (csv_formatted_data
                                        | "Colleting Location and Date as Key" >> beam.ParDo(CollectLocationKeyWithDate())
                                        | "Grouping by location with date" >> beam.GroupByKey()
                                        )

        variance_cases = (grouped_by_location
                          | "Calculating variance and stddev" >> beam.CombineValues(MeanVarStddev())
                          )

        top_cases = (grouped_by_location
                     | "Calculating top 3" >> beam.CombineValues(beam.combiners.TopCombineFn(n=int(options.ntop)))
                     )

        last_dates = (grouped_by_location_and_date
                      | "Calculating last date and last cases" >> beam.CombineValues(GetLastDatesOnly())
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
