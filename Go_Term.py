import requests, sys
import re
import pandas as pd
requestURL = "https://www.ebi.ac.uk/QuickGO/services/annotation/downloadStats?aspect=biological_process&geneProductId=P13021"

r = requests.get(requestURL, headers={ "Accept" : "application/json"})

if not r.ok:
  r.raise_for_status()
  sys.exit()

responseBody = r.text

with open('filz.txt', 'w') as f:
        f.write('%s'%responseBody)
	
print(responseBody)

