# MIT License
# Copyright (c) 2020 Gianluca Mancusi

import apache_beam as beam
from dateutil import parser


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
        cases_dates = (parser.parse(element['date']), int(
            element['total_cases']))
        region_province = f"{element['region']},{element['province']}"
        return [(region_province, cases_dates)]
