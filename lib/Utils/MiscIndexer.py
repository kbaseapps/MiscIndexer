# Special Indexer for Narrative Objects
from Utils.WorkspaceAdminUtils import WorkspaceAdminUtils
import json
import os


class MiscIndexer:
    def __init__(self, config):
        self.ws = WorkspaceAdminUtils(config)
        ldir = os.path.dirname(os.path.abspath(__file__))
        self.schema_dir = '/'.join(ldir.split('/')[0:-2])

    def _tf(self, val):
        if val == 0:
            return False
        else:
            return True

    def _guid(self, upa):
        (wsid, objid, ver) = upa.split('/')
        return "WS:%s:%s:%s" % (wsid, objid, ver)

    def assembly_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = dict()
        rec['name'] = data.get('name', '')
        rec['dna_size'] = int(data['dna_size'])
        rec['gc_content'] = float(data.get('gc_content'))
        rec['external_source_id'] = data.get('external_source_id', '')
        rec['contig_count'] = len(data['contigs'])
        rec['contigs'] = len(data['contigs'])
        schema = self.mapping('assembly_schema.json')
        return {'data': rec, 'schema': schema}

    def assemblycontig_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = {}
        rec['parent'] = {}
        features_rec = []
        for id in data['contigs']:
            feature = data['contigs'][id]
            frec = {}
            frec['contig_id'] = feature['contig_id']
            frec['description'] = feature['description']
            frec['gc_content'] = feature['gc_content']
            frec['length'] = feature['length']
            frec['guid'] = '%s:%s' % (self._guid(upa), frec['contig_id'])
            features_rec.append(frec)
        rec['features'] = features_rec
        rec['schema'] = self.mapping('assemblycontig_schema.json')
        return rec

    def narrative_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = dict()
        rec['title'] = data['metadata'].get('name', '')
        rec['source'] = []
        rec['code_output'] = []
        rec['app_output'] = []
        rec['app_info'] = []
        rec['app_input'] = []
        rec['job_ids'] = []
        if 'cells' in data:
            cells = data['cells']
        elif 'worksheets' in data and 'cells' in data['worksheets']:
            cells = data['worksheets']['cells']
        else:
            cells = []
        for cell in cells:
            rec['source'].append(cell.get('source'))
            # Skip output since it isn't used
            # - path: cells/[*]/outputs/[*]/data
            if 'metadata' in cell and 'kbase' in cell['metadata']:
                kb = cell['metadata']['kbase']
            # - path: cells/[*]/metadata/kbase/outputCell/widget/params
            # - path: cells/[*]/metadata/kbase/appCell/app/spec/info
                if 'appCell' in kb:
                    ac = kb['appCell']
                    rec['app_info'].append(ac['app']['spec']['info'])
                    rec['app_input'].append(ac['params'])
                if 'outputCell' in kb:
                    rec['job_ids'].append(kb['outputCell'].get('jobid'))
            # - path: cells/[*]/metadata/kbase/outputCell/jobId
        schema = self.mapping('narrative_schema.json')
        return {'data': rec, 'schema': schema}

    def ontologyterm_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = {}
        rec['parent'] = {
            'ontology_id': data['ontology'],
            'ontology_name': data['default_namespace']
        }
        features_rec = []
        for name in data['term_hash'].keys():
            feature = data['term_hash'][name]
            frec = {}
            frec['guid'] = '%s:%s' % (self._guid(upa), feature['id'])
            frec['id'] = feature['id']
            frec['name'] = feature['name']
            frec['namespace'] = feature['namespace']
            frec['definition'] = feature['def']
            frec['synonyms'] = feature.get('synonym')
            features_rec.append(frec)
        rec['features'] = features_rec
        rec['schema'] = self.mapping('ontologyterm_schema.json')
        return rec

    def pairedend_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = dict()
        rec['technology'] = data['sequencing_tech']
        rec['files'] = [data['lib1']['file']['file_name']]
        if 'lib2' in data:
            data['files'].append(data['lib2']['file']['file_name'])
        rec['phred_type'] = data['phred_type']
        rec['read_count'] = int(data['read_count'])
        rec['read_length'] = int(data.get('read_length_mean'))
        if data.get('insert_size_mean') is not None:
            rec['insert_size'] = int(data.get('insert_size_mean'))
        else:
            rec['insert_size'] = None
        rec['quality'] = float(data.get('qual_mean'))
        rec['gc_content'] = float(data.get('gc_content'))
        schema = self.mapping('pairedendlibrary_schema.json')
        return {'data': rec, 'schema': schema}

    def singleend_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = dict()
        rec['technology'] = data['sequencing_tech']
        rec['file'] = data['lib']['file']['file_name']
        rec['phred_type'] = data['phred_type']
        rec['read_count'] = int(data['read_count'])
        rec['read_length'] = int(data.get('read_length_mean'))
        rec['quality'] = float(data.get('qual_mean'))
        rec['gc_content'] = float(data.get('gc_content'))
        schema = self.mapping('singleendlibrary_schema.json')
        return {'data': rec, 'schema': schema}

    def pangenome_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = dict()
        rec['name'] = data['name']
        rec['type'] = data['type']
        rec['genomes'] = len(data['genome_refs'])
        rec['orthologs'] = len(data['orthologs'])
        rec['genome_names'] = []
        schema = self.mapping('pangenome_schema.json')
        return {'data': rec, 'schema': schema}

    def pangenomeorthologyfamily_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = {}
        rec['parent'] = {}
        features_rec = []
        for feature in data['orthologs']:
            frec = {}
            frec['guid'] = '%s:%s' % (self._guid(upa), feature['id'])
            frec['function'] = feature['function']
            frec['id'] = feature['id']
            genes = []
            for g in feature['orthologs']:
                genes.append(g[0])
            frec['ortholog_genes'] = genes
            features_rec.append(frec)
        rec['features'] = features_rec
        rec['schema'] = self.mapping('pangenome_schema.json')
        return rec

    def rnaseqsampleset_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = dict()
        rec['sampleset_desc'] = data['sampleset_desc']
        rec['num_replicates'] = int(data.get('num_replicates', 0))
        rec['source'] = data['source']
        rec['num_samples'] = int(data['num_samples'])
        schema = self.mapping('rnaseqsampleset_schema.json')
        return {'data': rec, 'schema': schema}

    def taxon_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = dict()
        rec['scientific_name'] = data['scientific_name']
        rec['scientific_lineage'] = data['scientific_lineage']
        rec['domain'] = data['domain']
        rec['genetic_code'] = int(data['genetic_code'])
        rec['aliases'] = data['aliases']
        schema = self.mapping('taxon_schema.json')
        return {'data': rec, 'schema': schema}

    def tree_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = dict()
        rec['labels'] = data['default_node_labels']
        rec['type'] = data['type']
        schema = self.mapping('tree_schema.json')
        return {'data': rec, 'schema': schema}

    def mapping(self, filename):
        with open(os.path.join(self.schema_dir, filename)) as f:
            schema = json.loads(f.read())
        return schema
