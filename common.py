# coding: utf-8

# Copyright 2022, Robert Dyer,
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
import pandas as pd

def get_dir(subdir):
    if subdir is None:
        return ''
    return subdir + '/'

def get_df(filename, subdir=None, **kwargs):
    try:
        df = pd.read_parquet(f'data/parquet/{get_dir(subdir)}{filename}.parquet')
    except:
        df = pd.read_csv(f'data/csv/{get_dir(subdir)}{filename}.csv', header=None, index_col=False, **kwargs)
        df.to_parquet(f'data/parquet/{get_dir(subdir)}{filename}.parquet', compression='gzip')
    return df

def get_deduped_df(filename, subdir=None, ts=False, **kwargs):
    try:
        df = pd.read_parquet(f'data/parquet/{get_dir(subdir)}{filename}-deduped.parquet')
    except:
        if ts:
            df = remove_dupes(get_df(filename, subdir, **kwargs), subdir, names=['var', 'hash', 'project', 'ts', 'file'])
        else:
            df = remove_dupes(get_df(filename, subdir, **kwargs), subdir)
        df.to_parquet(f'data/parquet/{get_dir(subdir)}{filename}-deduped.parquet', compression='gzip')
    return df

def remove_dupes(df, subdir=None, names=['var', 'hash', 'project', 'file']):
    df2 = get_df('dupes', subdir, names).drop(columns=['var'])

    df2 = df2[df2.duplicated(subset=['hash'])]
    df3 = pd.merge(df, df2, how='left', left_on=['project', 'file'], right_on=['project', 'file'])
    # df4 consists of rows in df3 where 'hash' is 'NaN' (meaning that they did not exist in df2.duplicated(subset=['hash']))
    df4 = df3[pd.isnull(df3['hash'])]
    return df4.drop(columns=['hash'])
