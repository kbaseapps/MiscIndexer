# -*- coding: utf-8 -*-
import json
import os
import unittest
from configparser import ConfigParser
from unittest.mock import Mock

from MiscIndexer.MiscIndexerImpl import MiscIndexer
from MiscIndexer.MiscIndexerServer import MethodContext
from installed_clients.WorkspaceClient import Workspace


class MiscIndexerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('MiscIndexer'):
            cls.cfg[nameval[0]] = nameval[1]
        cls.cfg['workspace-admin-token'] = token

        user_id = 'bogus'
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'MiscIndexer',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.impl = MiscIndexer(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.test_dir = os.path.dirname(os.path.abspath(__file__))
        cls.mock_dir = os.path.join(cls.test_dir, 'mock_data')
        cls.schema_dir = cls.cfg['schema-dir']

        cls.wsinfo = cls.read_mock('get_workspace_info.json')
        cls.assemblyobj = cls.read_mock('assembly_object.json')
        cls.narobj = cls.read_mock('narrative_object.json')
        cls.pairedend = cls.read_mock('pairedend_object.json')
        cls.singleend = cls.read_mock('singleend_object.json')
        cls.ontology = cls.read_mock('ontology_object.json')
        cls.pangenome = cls.read_mock('pangenome_object.json')
        cls.rnaseqsampleset = cls.read_mock('rnaseqsampleset_object.json')
        cls.taxon = cls.read_mock('taxon_object.json')
        cls.tree = cls.read_mock('tree_object.json')
        
        cls.params = {'upa': '1/2/3'}
        cls.impl.indexer.ws.get_objects2 = Mock()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    @classmethod
    def read_mock(cls, filename):
        with open(os.path.join(cls.mock_dir, filename)) as f:
            obj = json.loads(f.read())
        return obj

    def _validate(self, sfile, data):
        schema = json.load(open(os.path.join(self.schema_dir, sfile)))
        for key in schema['schema'].keys():
            self.assertIn(key, data)

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_indexers(self):
        self.impl.indexer.ws.get_objects2.return_value = self.assemblyobj
        ret = self.impl.assembly_index(self.ctx, self.params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self.assertIn('schema', ret[0])
        self._validate('assembly_schema.json', ret[0]['data'])

        ret = self.impl.assemblycontig_index(self.ctx, self.params)
        self.assertIsNotNone(ret[0])
        self.assertIn('documents', ret[0])
        self.assertIn('schema', ret[0])
        self._validate('assemblycontig_schema.json', ret[0]['documents'][0])

    def test_narrative_indexes(self):
        self.impl.indexer.ws.get_objects2.return_value = self.narobj
        ret = self.impl.narrative_index(self.ctx, self.params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self.assertIn('schema', ret[0])
        self._validate('narrative_schema.json', ret[0]['data'])

        nar2 = self.read_mock('narrative2_object.json')
        self.impl.indexer.ws.get_objects2.return_value = nar2
        ret = self.impl.narrative_index(self.ctx, self.params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self.assertIn('schema', ret[0])
        self._validate('narrative_schema.json', ret[0]['data'])

    def test_ontologyterm_index(self):
        self.impl.indexer.ws.get_objects2.return_value = self.ontology
        ret = self.impl.ontologyterm_index(self.ctx, self.params)
        self.assertIsNotNone(ret[0])
        self.assertIn('documents', ret[0])
        self.assertIn('schema', ret[0])
        self.assertIn('definition', ret[0]['documents'][0])
        self.assertIn('id', ret[0]['documents'][0])
        self.assertIn('name', ret[0]['documents'][0])
        self.assertIn('namespace', ret[0]['documents'][0])
        self.assertIn('ontology_id', ret[0]['parent'])
        self.assertIn('ontology_name', ret[0]['parent'])

    def test_pairedendlibrary_index(self):
        self.impl.indexer.ws.get_objects2.return_value = self.pairedend
        ret = self.impl.pairedendlibrary_index(self.ctx, self.params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self.assertIn('schema', ret[0])
        self._validate('pairedendlibrary_schema.json', ret[0]['data'])

    def test_pangenome_indexes(self):
        self.impl.indexer.ws.get_objects2.return_value = self.pangenome
        ret = self.impl.pangenome_index(self.ctx, self.params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self.assertIn('schema', ret[0])
        self._validate('pangenome_schema.json', ret[0]['data'])

        ret = self.impl.pangenomeorthology_index(self.ctx, self.params)
        self.assertIsNotNone(ret[0])
        self.assertIn('documents', ret[0])
        self.assertIn('schema', ret[0])
        self._validate('pangenomeorthologyfamily_schema.json', ret[0]['documents'][0])

    def test_rnaseqsampleset_index(self):
        self.impl.indexer.ws.get_objects2.return_value = self.rnaseqsampleset
        ret = self.impl.rnaseqsampleset_index(self.ctx, self.params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self.assertIn('schema', ret[0])
        self._validate('rnaseqsampleset_schema.json', ret[0]['data'])

    def test_singleendlibrary_index(self):
        self.impl.indexer.ws.get_objects2.return_value = self.singleend
        ret = self.impl.singleendlibrary_index(self.ctx, self.params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self.assertIn('schema', ret[0])
        self._validate('singleendlibrary_schema.json', ret[0]['data'])

    def test_taxon_index(self):
        self.impl.indexer.ws.get_objects2.return_value = self.taxon
        ret = self.impl.taxon_index(self.ctx, self.params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self.assertIn('schema', ret[0])
        self._validate('taxon_schema.json', ret[0]['data'])

    def test_tree_index(self):
        self.impl.indexer.ws.get_objects2.return_value = self.tree
        ret = self.impl.tree_index(self.ctx, self.params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self.assertIn('schema', ret[0])
        self._validate('tree_schema.json', ret[0]['data'])
