# Special Indexer for Narrative Objects
import json
import os

from Utils.WorkspaceAdminUtils import WorkspaceAdminUtils


class MiscIndexer:
    def __init__(self, config):
        self.ws = WorkspaceAdminUtils(config)
        self.schema_dir = config['schema-dir']

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
        rec = {'name': data.get('name', ''),
               'dna_size': int(data['dna_size']),
               'gc_content': float(data.get('gc_content')),
               'external_source_id': data.get('external_source_id', ''),
               'contig_count': len(data['contigs']),
               'contigs': len(data['contigs'])}
        schema = self.mapping('assembly_schema.json')
        return {'data': rec, 'schema': schema}

    def assemblycontig_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = {'parent': {}}
        features_rec = []
        for _id in data['contigs']:
            feature = data['contigs'][_id]
            frec = {'contig_id': feature['contig_id'],
                    'description': feature.get('description'),
                    'gc_content': feature['gc_content'],
                    'length': feature['length'],
                    'guid': f'{self._guid(upa)}:{feature["contig_id"]}'}
            features_rec.append(frec)
        rec['documents'] = features_rec
        rec['schema'] = self.mapping('assemblycontig_schema.json')
        return rec

    def narrative_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = {'title': data['metadata'].get('name', ''),
               'source': [],
               'code_output': [],
               'app_output': [],
               'app_info': [],
               'app_input': [],
               'job_ids': []}
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
        rec = {
            'parent': {
                'ontology_id': data.get('ontology', None),
                'ontology_name': data.get('default_namespace', None)
             }
        }

        features_rec = []
        for name in data['term_hash'].keys():
            feature = data['term_hash'][name]
            frec = {'guid': f'{self._guid(upa)}:{feature["id"]}',
                    'id': feature['id'],
                    'name': feature['name'],
                    'namespace': feature['namespace'],
                    'definition': feature['def'],
                    'synonyms': feature.get('synonym')}
            features_rec.append(frec)
        rec['documents'] = features_rec
        rec['schema'] = self.mapping('ontologyterm_schema.json')
        return rec

    def pairedend_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = {'technology': data['sequencing_tech'],
               'files': [data['lib1']['file']['file_name']],
               'phred_type': data['phred_type'],
               'read_count': int(data['read_count']),
               'read_length': int(data.get('read_length_mean')),
               'quality': float(data.get('qual_mean')),
               'gc_content': float(data.get('gc_content'))}

        if 'lib2' in data:
            data['files'].append(data['lib2']['file']['file_name'])
        if data.get('insert_size_mean') is not None:
            rec['insert_size'] = int(data.get('insert_size_mean'))
        else:
            rec['insert_size'] = None
        schema = self.mapping('pairedendlibrary_schema.json')
        return {'data': rec, 'schema': schema}

    def singleend_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = {'technology': data['sequencing_tech'],
               'phred_type': data['phred_type'],
               'read_count': int(data['read_count']),
               'read_length': int(data.get('read_length_mean')),
               'quality': float(data.get('qual_mean')),
               'gc_content': float(data.get('gc_content'))}
        if 'lib' in data:
            rec['file'] = data['lib']['file']['file_name']
        elif 'lib1' in data:
            rec['file'] = data['lib1']['file']['file_name']
        schema = self.mapping('singleendlibrary_schema.json')
        return {'data': rec, 'schema': schema}

    def pangenome_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = {'name': data['name'],
               'type': data['type'],
               'genomes': len(data['genome_refs']),
               'orthologs': len(data['orthologs']),
               'genome_names': []}
        schema = self.mapping('pangenome_schema.json')
        return {'data': rec, 'schema': schema}

    def pangenomeorthologyfamily_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = {'parent': {}}
        features_rec = []
        for feature in data['orthologs']:
            frec = {'guid': f'{self._guid(upa)}:{feature["id"]}',
                    'function': feature['function'],
                    'id': feature['id']}
            genes = []
            for g in feature['orthologs']:
                genes.append(g[0])
            frec['ortholog_genes'] = genes
            features_rec.append(frec)
        rec['documents'] = features_rec
        rec['schema'] = self.mapping('pangenome_schema.json')
        return rec

    def rnaseqsampleset_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = {'sampleset_desc': data['sampleset_desc'],
               'num_replicates': int(data.get('num_replicates', 0)),
               'source': data['source'],
               'num_samples': int(data['num_samples'])}
        schema = self.mapping('rnaseqsampleset_schema.json')
        return {'data': rec, 'schema': schema}

    def taxon_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = {'scientific_name': data['scientific_name'],
               'scientific_lineage': data['scientific_lineage'],
               'domain': data['domain'],
               'genetic_code': int(data['genetic_code']),
               'aliases': data['aliases']}
        schema = self.mapping('taxon_schema.json')
        return {'data': rec, 'schema': schema}

    def tree_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = {'labels': data['default_node_labels'],
               'type': data['type']}
        schema = self.mapping('tree_schema.json')
        return {'data': rec, 'schema': schema}

    def mapping(self, filename):
        with open(os.path.join(self.schema_dir, filename)) as f:
            schema = json.loads(f.read())
        return schema['schema']
