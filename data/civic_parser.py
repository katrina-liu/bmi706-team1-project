#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd


# In[3]:


'''
Read 2017-2023 clinical evidence summaries
'''

# replace the character \x{0D} to space manually for clinEvi2017.tsv
clinEvs = [pd.read_csv(r'civic/01-Jan-' + str(year) + '-ClinicalEvidenceSummaries.tsv', sep='\t') 
              for year in range(2017,2024)]


# In[4]:


'''
Parse 2017-2023 files
'''

col_name = list(clinEvs[0].columns)
col_name.append('year')
col_name.remove('pubmed_id')

for i in range(0, 7):
    clinEvs[i]['year'] = 2017+i
    clinEvs[i] = clinEvs[i][col_name]


# In[7]:


clinEvs[0].columns


# In[12]:


'''
Get unique rows without year
'''
unique = pd.concat(clinEvs).drop_duplicates(
    subset=["entrez_id", "doid",'evidence_id', 'variant_id', 'gene_id'], keep=False)
unique.to_csv('civic_data_unique.tsv')


# In[5]:


'''
Write the parsed file
'''
pd.concat(clinEvs).to_csv('civic_data.tsv')

