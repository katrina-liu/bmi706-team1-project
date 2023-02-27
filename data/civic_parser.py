#!/usr/bin/env python
# coding: utf-8

import pandas as pd

'''
Read 2017-2023 clinical evidence summaries
'''

# replace the character \x{0D} to space manually for clinEvi2017.tsv
clinEvs = [pd.read_csv(r'civic/01-Jan-' + str(year) + '-ClinicalEvidenceSummaries.tsv', sep='\t') 
              for year in range(2017,2024)]

'''
Parse 2017-2023 files
'''

col_name = list(clinEvs[0].columns)
col_name.append('year')
col_name.remove('pubmed_id')

for i in range(0, 7):
    clinEvs[i]['year'] = 2017+i
    clinEvs[i] = clinEvs[i][col_name]


'''
Write the parsed file
'''
pd.concat(clinEvs).to_csv('civic_data.tsv')

