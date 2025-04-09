#!/usr/bin/env python
# encoding: utf-8

import pandas as pd


input_file = '/home/shmily/Downloads/i.xlsx'
output_file = '/home/shmily/Downloads/o.csv'

xlsx_file = pd.read_excel(input_file)
xlsx_file.to_csv(output_file, index=False, encoding='utf-8')
