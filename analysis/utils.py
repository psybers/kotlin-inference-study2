#!/usr/bin/env python
# coding: utf-8

import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

# Set default plot style
def set_style():
    sns.set_style('whitegrid')
    sns.set_palette('colorblind')

def save_figure(figure, filename, x=None, y=None):
    '''Save a FIGURE to FILENAME with size of X, Y inches.'''
    fig = figure.get_figure()
    plt.tight_layout()
    if x is not None:
        fig.set(figwidth = x)
    if y is not None:
        fig.set(figheight = y)
    fig.savefig(filename, dpi=600)
    plt.close(fig)

colsepname = ''
def save_table(df, filename, decimals=2, colsep=False, **kwargs):
    global colsepname
    if not colsep is False:
        colsepname = colsepname + 'A'

    pd.options.display.float_format = ('{:,.' + str(decimals) + 'f}').format

    with pd.option_context("max_colwidth", 1000):
        tab1 = df.style.format_index("\\textbf{{{0}}}", axis = 1).to_latex(**kwargs)
    # print(tab1)
    with open(filename,'w',encoding='utf-8') as f:
        f.write('% DO NOT EDIT\n')
        f.write('% this file was automatically generated\n')
        if not colsep is False:
            f.write('\\newcommand{\\oldtabcolsep' + colsepname + '}{\\tabcolsep}\n')
            f.write('\\renewcommand{\\tabcolsep}{' + colsep + '}\n')
        f.write(tab1)
        if not colsep is False:
            f.write('\\renewcommand{\\tabcolsep}{\\oldtabcolsep' + colsepname +'}\n')


def load_data_csv(language, file, **kwargs):
    return pd.read_csv(f"data-csv/{language}/{file}", on_bad_lines='skip', **kwargs)
