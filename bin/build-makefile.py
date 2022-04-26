#!/usr/bin/env python3
# coding: utf-8

# Copyright 2022, Robert Dyer, Samuel W. Flint,
#                 and University of Nebraska Board of Regents
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from utilities import get_query_config, build_replacements

configuration = get_query_config()

print('# DO NOT EDIT - this file is automatically generated')
print('PYTHON:=python3')
print('BOATOCSV:=${PYTHON} bin/boa-to-csv.py')
print('DOWNLOAD:=${PYTHON} bin/download.py')

for target in configuration['queries']:
    query_info = configuration['queries'][target]
    substitution_files = [x for (_, x) in build_replacements(configuration['substitutions'], query_info['substitutions'], only_files = True)]

    string = f'{query_info["query"]}'
    for file_name in substitution_files:
        string += f' {file_name}'

    print('')
    print(f'{target}: {string}')
    print(f'\t${{DOWNLOAD}} {target}')

    if 'csv' in query_info:
        csv_info = query_info['csv']
        new_target = csv_info['output']
        print('')
        print(f'{new_target}: {target}')

        print(f'\tmkdir -p $(shell dirname {new_target})')
        string = '\t${BOATOCSV}'
        if 'tests' in csv_info:
            for test in csv_info['tests']:
                string += f' -t "{test}"'
        if 'drop' in csv_info:
            string += f' -d {csv_info["drop"]}'
        if 'header' in csv_info:
            string += f' --header {csv_info["header"]}'
        if 'index' in csv_info:
            string += f' --numidx {csv_info["index"]}'
        string += f' {target} > {new_target}'
        print(string)
