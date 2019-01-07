from Workspace.WorkspaceClient import Workspace
import json
wsid = 15792
upa = '15792/2'

ws = Workspace('https://ci.kbase.us/services/ws')

#upa = '15792/206394/1'
#d = ws.get_objects2({'objects': [{'ref': upa}]})
#with open('./test/mock_data/assembly_object.json', 'w') as f:
#    f.write(json.dumps(d, indent=2))

upa = '15767/5/1'
d = ws.get_objects2({'objects': [{'ref': upa}]})
with open('./test/mock_data/pairedend_object.json', 'w') as f:
    f.write(json.dumps(d, indent=2))

upa = '15767/7/1'
d = ws.get_objects2({'objects': [{'ref': upa}]})
with open('./test/mock_data/singleend_object.json', 'w') as f:
    f.write(json.dumps(d, indent=2))

upa = '38012/63/1'
d = ws.get_objects2({'objects': [{'ref': upa}]})
with open('./test/mock_data/pangenome_object.json', 'w') as f:
    f.write(json.dumps(d, indent=2))

upa = '16962/14/1'
d = ws.get_objects2({'objects': [{'ref': upa}]})
with open('./test/mock_data/rnaseqsampleset_object.json', 'w') as f:
    f.write(json.dumps(d, indent=2))

upa = '35753/6/1'
d = ws.get_objects2({'objects': [{'ref': upa}]})
with open('./test/mock_data/taxon_object.json', 'w') as f:
    f.write(json.dumps(d, indent=2))

upa = '35753/3/1'
d = ws.get_objects2({'objects': [{'ref': upa}]})
with open('./test/mock_data/tree_object.json', 'w') as f:
    f.write(json.dumps(d, indent=2))

upa = '6308/2/3'
d = ws.get_objects2({'objects': [{'ref': upa}]})
with open('./test/mock_data/ontology_object.json', 'w') as f:
    f.write(json.dumps(d, indent=2))
