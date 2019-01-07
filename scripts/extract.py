import json
import sys

with open('mappings.out') as f:
  d = f.read()
all = json.loads(d)

if len(sys.argv)==1:
  for i in all.keys():
     print(i)
else:
  s = 'kbaseci.' + sys.argv[1] 
  part = { 'schema': all[s]['mappings']['data']['properties']['key']['properties'] }
  print(json.dumps(part, indent=4))
