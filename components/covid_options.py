# MIT License
# Copyright (c) 2020 Gianluca Mancusi

from apache_beam.options.pipeline_options import PipelineOptions


class CovidOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument('--input', help='Input dataset for the pipeline')
        parser.add_argument(
            '--output', help='Output file name for the pipeline')
        parser.add_argument(
            '--ntop', type=int, help='Number of top day cases to show', default='3')
