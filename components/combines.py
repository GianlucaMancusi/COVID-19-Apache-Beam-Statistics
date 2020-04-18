# MIT License
# Copyright (c) 2020 Gianluca Mancusi

from datetime import datetime
import apache_beam as beam
import numpy as np


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
        return (datetime.min, 0.0)  # dates, cases

    def add_input(self, dates_cases, input):
        (max_date, cases_max_date) = dates_cases
        (input_date, input_cases) = input
        # only takes the most recent date with its number of cases
        return (max_date, cases_max_date) if max_date > input_date else (input_date, input_cases)

    def merge_accumulators(self, accumulators):
        (dates, cases) = zip(*accumulators)
        # takes the index of the most recent date
        index = np.argmax(dates)
        return (dates[index], cases[index])

    def extract_output(self, dates_cases):
        (date, cases) = dates_cases
        return {'date': "{:%Y-%m-%d}".format(date), 'cases': cases}
