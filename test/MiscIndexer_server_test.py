# -*- coding: utf-8 -*-
import os
import time
import unittest
from configparser import ConfigParser

from MiscIndexer.MiscIndexerImpl import MiscIndexer
from MiscIndexer.MiscIndexerServer import MethodContext
from MiscIndexer.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace
from unittest.mock import Mock
import json


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

        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        # user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
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
        cls.serviceImpl = MiscIndexer(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.test_dir = os.path.dirname(os.path.abspath(__file__))
        cls.mock_dir = os.path.join(cls.test_dir, 'mock_data')

        cls.wsinfo = cls.read_mock('get_workspace_info.json')
        cls.assemblyobj = cls.read_mock('assembly_object.json')
        cls.pairedend = cls.read_mock('pairedend_object.json')
        cls.singleend = cls.read_mock('singleend_object.json')
        cls.ontology = cls.read_mock('ontology_object.json')
        cls.pangenome = cls.read_mock('pangenome_object.json')
        cls.rnaseqsampleset = cls.read_mock('rnaseqsampleset_object.json')
        cls.taxon = cls.read_mock('taxon_object.json')
        cls.tree = cls.read_mock('tree_object.json')

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

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_MiscIndexer_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def _validate(self, sfile, data):
        with open(self.test_dir + '/../' + sfile) as f:
            d = f.read()

        schema = json.loads(d)
        for key in schema['schema'].keys():
            self.assertIn(key, data)

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_mappings(self):
        ret = self.getImpl().assembly_mapping(self.getContext(), {})
        self.assertIsNotNone(ret[0])

        ret = self.getImpl().assemblycontig_mapping(self.getContext(), {})
        self.assertIsNotNone(ret[0])

        ret = self.getImpl().ontologyterm_mapping(self.getContext(), {})
        self.assertIsNotNone(ret[0])

        ret = self.getImpl().pairedendlibrary_mapping(self.getContext(), {})
        self.assertIsNotNone(ret[0])

        ret = self.getImpl().pangenome_mapping(self.getContext(), {})
        self.assertIsNotNone(ret[0])

        ret = self.getImpl().pangenomeorthology_mapping(self.getContext(), {})
        self.assertIsNotNone(ret[0])

        ret = self.getImpl().rnaseqsampleset_mapping(self.getContext(), {})
        self.assertIsNotNone(ret[0])

        ret = self.getImpl().singleendlibrary_mapping(self.getContext(), {})
        self.assertIsNotNone(ret[0])

        ret = self.getImpl().taxon_mapping(self.getContext(), {})
        self.assertIsNotNone(ret[0])

        ret = self.getImpl().tree_mapping(self.getContext(), {})
        self.assertIsNotNone(ret[0])



    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_indexers(self):
        impl = self.getImpl()
        params = {'upa': '1/2/3'}
        impl.indexer.ws.get_objects2 = Mock()

        impl.indexer.ws.get_objects2.return_value = self.assemblyobj
        ret = impl.assembly_index(self.getContext(), params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self._validate('assembly_schema.json', ret[0]['data'])

        ret = impl.assemblycontig_index(self.getContext(), params)
        self.assertIsNotNone(ret[0])
        self.assertIn('features', ret[0])
        self._validate('assemblycontig_schema.json', ret[0]['features'][0])

        impl.indexer.ws.get_objects2.return_value = self.ontology
        ret = impl.ontologyterm_index(self.getContext(), params)
        self.assertIsNotNone(ret[0])
        self.assertIn('features', ret[0])
        self.assertIn('definition', ret[0]['features'][0])
        self.assertIn('id', ret[0]['features'][0])
        self.assertIn('name', ret[0]['features'][0])
        self.assertIn('namespace', ret[0]['features'][0])
        self.assertIn('ontology_id', ret[0]['parent'])
        self.assertIn('ontology_name', ret[0]['parent'])

        impl.indexer.ws.get_objects2.return_value = self.pairedend
        ret = impl.pairedendlibrary_index(self.getContext(), params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self._validate('pairedendlibrary_schema.json', ret[0]['data'])

        impl.indexer.ws.get_objects2.return_value = self.pangenome
        ret = impl.pangenome_index(self.getContext(), params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self._validate('pangenome_schema.json', ret[0]['data'])

        ret = impl.pangenomeorthology_index(self.getContext(), params)
        self.assertIsNotNone(ret[0])
        self.assertIn('features', ret[0])
        self._validate('pangenomeorthologyfamily_schema.json', ret[0]['features'][0])

        impl.indexer.ws.get_objects2.return_value = self.rnaseqsampleset
        ret = impl.rnaseqsampleset_index(self.getContext(), params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self._validate('rnaseqsampleset_schema.json', ret[0]['data'])

        impl.indexer.ws.get_objects2.return_value = self.singleend
        ret = impl.singleendlibrary_index(self.getContext(), params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self._validate('singleendlibrary_schema.json', ret[0]['data'])

        impl.indexer.ws.get_objects2.return_value = self.taxon
        ret = impl.taxon_index(self.getContext(), params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self._validate('taxon_schema.json', ret[0]['data'])

        impl.indexer.ws.get_objects2.return_value = self.tree
        ret = impl.tree_index(self.getContext(), params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self._validate('tree_schema.json', ret[0]['data'])
