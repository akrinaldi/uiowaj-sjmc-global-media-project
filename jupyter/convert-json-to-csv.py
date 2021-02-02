#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import glob
import json
import pandas as pd

jsons = glob.glob("./uiowaj-sjmc-global-media-project/jupyter/outputs*/*/*.json")
records = []

def flatten_json(y):
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + ':')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + ':')
                i += 1
        else:
            out[name[:-1]] = x
    flatten(y)
    return out

for idx, file in enumerate(jsons):
    p = file.split("/")
    issn_year = p[-1].split(".")[0]
    issn, year = issn_year.split("_")[0], issn_year.split("_")[1]
    print(file, issn, year)
    with open(file) as fp:
        data = json.load(fp)
        entries = data["search-results"]["entry"]
        if len(entries) < 2:
            continue
        for entry in entries:
            record = flatten_json(entry)
            record["issn-from-folder"] = issn
            record["year-from-folder"] = year
            records.append(record)
            
df = pd.DataFrame.from_records(records)
df.to_csv(index=False, path_or_buf='records.csv')


# In[ ]:




