#!/usr/bin/python
from Workspace.WorkspaceClient import Workspace
import json
import os
wsid = 15792
upa = '15792/2'

ws = Workspace('https://ci.kbase.us/services/ws')


def grab(upa, file):
    if not os.path.exists(file):
        d = ws.get_objects2({'objects': [{'ref': upa}]})
        with open(file, 'w') as f:
            f.write(json.dumps(d, indent=4))


grab('15767/5/1', './test/mock_data/pairedend_object.json')

grab('15767/7/1', './test/mock_data/singleend_object.json')

grab('38012/63/1', './test/mock_data/pangenome_object.json')

# upa = '16962/14/1'
# d = ws.get_objects2({'objects': [{'ref': upa}]})
# with open('./test/mock_data/rnaseqsampleset_object.json', 'w') as f:
#     f.write(json.dumps(d, indent=2))
#
# upa = '35753/6/1'
# d = ws.get_objects2({'objects': [{'ref': upa}]})
# with open('./test/mock_data/taxon_object.json', 'w') as f:
#     f.write(json.dumps(d, indent=2))
#
# upa = '35753/3/1'
# d = ws.get_objects2({'objects': [{'ref': upa}]})
# with open('./test/mock_data/tree_object.json', 'w') as f:
#     f.write(json.dumps(d, indent=2))
#
# upa = '6308/2/3'
# d = ws.get_objects2({'objects': [{'ref': upa}]})
# with open('./test/mock_data/ontology_object.json', 'w') as f:
#     f.write(json.dumps(d, indent=2))

grab('4/2/37', './test/mock_data/narrative2_object.json')
