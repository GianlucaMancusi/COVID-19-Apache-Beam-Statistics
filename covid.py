import apache_beam as beam
import numpy as np
from apache_beam.options.pipeline_options import PipelineOptions
from dateutil import parser
from datetime import datetime

input_filename = "dpc-covid19-ita-province.csv"
output_filename = "output.txt"

# cose da fare:
# - Opzioni per cambiare parametri
# - Sistemare l'output


class NewOptions(PipelineOptions):
  @classmethod
  def _add_argparse_args(cls, parser):
    parser.add_argument('--input', help='Input for the pipeline')
    parser.add_argument('--output', help='Output for the pipeline')
    parser.add_argument('--ntop', help='Number of top day cases to show', default='3')

class Split(beam.DoFn):
    def process(self, element):
        data, __, ___, denominazione_regione, \
            ____, denominazione_provincia, \
            _____, ______, _______, totale_casi, \
            ________, _________ = element.split(",")
        return [{'regione': denominazione_regione,
                 'provincia': denominazione_provincia,
                 'data': data,
                 'totale_casi': totale_casi}]


class DeleteDatiInAggiornamento(beam.DoFn):
    def process(self, element):
        return None if 'In fase di definizione/aggiornamento' in element["provincia"] else [element]


class CollectRegioneProvincia(beam.DoFn):
    def process(self, element):
        return [(f"{element['regione']},{element['provincia']}", int(element['totale_casi']))]


class CollectRegioneProvinciaConData(beam.DoFn):
    def process(self, element):
        data_casi = (parser.parse(element['data']), int(
            element['totale_casi']))
        regione_provincia = f"{element['regione']},{element['provincia']}"
        return [(regione_provincia, data_casi)]


class Stddev(beam.CombineFn):
    def create_accumulator(self):
        return (0.0, 0.0, 0)  # x, x^2, count

    def add_input(self, sum_count, input):
        (sum, sumsq, count) = sum_count
        return sum + input, sumsq + input*input, count + 1

    def merge_accumulators(self, accumulators):
        sums, sumsqs, counts = zip(*accumulators)
        return sum(sums), sum(sumsqs), sum(counts)

    def extract_output(self, sum_count):
        (sum, sumsq, count) = sum_count
        mean, variance, stddev = 0, 0, 0
        if count:
            mean = sum / count
            variance = (sumsq / count) - mean*mean  # E(x^2) - E(x)*E(x)
            stddev = np.sqrt(variance) if variance > 0 else 0
        return {
            'media': mean if count else float('NaN'),
            'varianza': variance if count else float('NaN'),
            'stddev': stddev if count else float('NaN')
        }


class GetLastDatesOnly(beam.CombineFn):
    def create_accumulator(self):
        return (datetime.min, 0.0)  # data, casi

    def add_input(self, data_casi, input):
        (data_max, casi_data_max) = data_casi
        (data_input, casi_input) = input
        # prende solo la data più recente con il suo numero di casi
        return (data_max, casi_data_max) if data_max > data_input else (data_input, casi_input)

    def merge_accumulators(self, accumulators):
        (date, casi_date) = zip(*accumulators)
        # prende l'indice della data più recente
        index = np.argmax(date)
        return (date[index], casi_date[index])

    def extract_output(self, data_casi):
        (data, casi) = data_casi
        return {'data': "{:%Y-%m-%d}".format(data), 'casi': casi}

new_options = NewOptions()
with beam.Pipeline(options=new_options) as p:
    csv_formatted_data = (p
                          | beam.io.ReadFromText(new_options.input, skip_header_lines=1)
                          | beam.ParDo(Split())
                          | beam.ParDo(DeleteDatiInAggiornamento())
                          )

    grouped_by_regione_provincia = (csv_formatted_data
                                    | beam.ParDo(CollectRegioneProvincia())
                                    | "Grouping by regione_provincia" >> beam.GroupByKey()
                                    )
    grouped_by_regione_provincia_con_data = (csv_formatted_data
                                             | beam.ParDo(CollectRegioneProvinciaConData())
                                             | "Grouping by regione_provincia_con_data" >> beam.GroupByKey()
                                             )

    # mean_cases = (grouped_by_regione_provincia
    #              | "Calculating mean" >> beam.CombineValues(beam.combiners.MeanCombineFn())
    #              )

    variance_cases = (grouped_by_regione_provincia
                      | "Calculating variance and stddev" >> beam.CombineValues(Stddev())
                      )

    top_cases = (grouped_by_regione_provincia
                 | "Calculating top 3" >> beam.CombineValues(beam.combiners.TopCombineFn(n=int(new_options.ntop)))
                 )

    last_dates = (grouped_by_regione_provincia_con_data
                  | beam.CombineValues(GetLastDatesOnly())
                  )

    output_pipe = (
        {
            'statistica_casi': variance_cases,
            f'top_{new_options.ntop}_casi': top_cases,
            'ultimi_dati': last_dates
        }
        | beam.CoGroupByKey()
        | beam.io.WriteToText(new_options.output))
