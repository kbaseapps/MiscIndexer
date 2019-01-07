# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
from unittest.mock import patch

from os import environ
from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from Workspace.WorkspaceClient import Workspace as workspaceService
# from MiscIndexer.authclient import KBaseAuth as _KBaseAuth
from Utils.MiscIndexer import MiscIndexer


class MiscIndexerTester(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('MiscIndexer'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        # authServiceUrl = cls.cfg['auth-service-url']
        # auth_client = _KBaseAuth(authServiceUrl)
        # user_id = auth_client.get_user(cls.token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.scratch = cls.cfg['scratch']
        cls.cfg['token'] = cls.token
        cls.upa = '1/2/3'
        cls.test_dir = os.path.dirname(os.path.abspath(__file__))
        cls.mock_dir = os.path.join(cls.test_dir, 'mock_data')

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

    @patch('Utils.MiscIndexer.WorkspaceAdminUtils', autospec=True)
    def index_assembly_test(self, mock_wsa):
        iu = MiscIndexer(self.cfg)
        iu.ws.get_objects2.return_value = self.assemblyobj
        res = iu.assembly_index(self.upa)
        self.assertIsNotNone(res)
        self.assertIn('data', res)
        res = iu.assemblycontig_index(self.upa)
        self.assertIsNotNone(res)
        self.assertIn('features', res)

    @patch('Utils.MiscIndexer.WorkspaceAdminUtils', autospec=True)
    def index_ontologyterm_test(self, mock_wsa):
        iu = MiscIndexer(self.cfg)
        iu.ws.get_objects2.return_value = self.ontology
        res = iu.ontologyterm_index(self.upa)
        self.assertIsNotNone(res)
        self.assertIn('features', res)

    @patch('Utils.MiscIndexer.WorkspaceAdminUtils', autospec=True)
    def index_pairedend_test(self, mock_wsa):
        iu = MiscIndexer(self.cfg)
        iu.ws.get_objects2.return_value = self.pairedend
        res = iu.pairedend_index(self.upa)
        self.assertIsNotNone(res)
        self.assertIn('data', res)

    @patch('Utils.MiscIndexer.WorkspaceAdminUtils', autospec=True)
    def index_pangenome_test(self, mock_wsa):
        iu = MiscIndexer(self.cfg)
        iu.ws.get_objects2.return_value = self.pangenome
        res = iu.pangenome_index(self.upa)
        self.assertIsNotNone(res)
        self.assertIn('data', res)
        res = iu.pangenomeorthologyfamily_index(self.upa)
        self.assertIsNotNone(res)
        self.assertIn('features', res)

    @patch('Utils.MiscIndexer.WorkspaceAdminUtils', autospec=True)
    def index_rnaseq_test(self, mock_wsa):
        iu = MiscIndexer(self.cfg)
        iu.ws.get_objects2.return_value = self.rnaseqsampleset
        res = iu.rnaseqsampleset_index(self.upa)
        self.assertIsNotNone(res)
        self.assertIn('data', res)

    @patch('Utils.MiscIndexer.WorkspaceAdminUtils', autospec=True)
    def index_singleend_test(self, mock_wsa):
        iu = MiscIndexer(self.cfg)
        iu.ws.get_objects2.return_value = self.singleend
        res = iu.singleend_index(self.upa)
        self.assertIsNotNone(res)
        self.assertIn('data', res)

    @patch('Utils.MiscIndexer.WorkspaceAdminUtils', autospec=True)
    def index_taxon_test(self, mock_wsa):
        iu = MiscIndexer(self.cfg)
        iu.ws.get_objects2.return_value = self.taxon
        res = iu.taxon_index(self.upa)
        self.assertIsNotNone(res)
        self.assertIn('data', res)

    @patch('Utils.MiscIndexer.WorkspaceAdminUtils', autospec=True)
    def index_tree_test(self, mock_wsa):
        iu = MiscIndexer(self.cfg)
        iu.ws.get_objects2.return_value = self.tree
        res = iu.tree_index(self.upa)
        self.assertIsNotNone(res)
        self.assertIn('data', res)
