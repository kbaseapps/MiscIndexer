# -*- coding: utf-8 -*-
#BEGIN_HEADER
from Utils.MiscIndexer import MiscIndexer as UtilMiscIndexer
#END_HEADER


class MiscIndexer:
    '''
    Module Name:
    MiscIndexer

    Module Description:
    A KBase module: MiscIndexer
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "git@github.com:kbaseapps/MiscIndexer.git"
    GIT_COMMIT_HASH = "0ccac363fa473b23027c0bd28fefaa25debb4f35"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.shared_folder = config['scratch']
        self.wsa_token = None
        self.wsa_token = config.get('workspace-admin-token', None)
        self.indexer = UtilMiscIndexer(config)
        #END_CONSTRUCTOR
        pass


    def assembly_index(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN assembly_index
        output = self.indexer.assembly_index(params['upa'])
        #END assembly_index

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method assembly_index return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def assemblycontig_index(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN assemblycontig_index
        output = self.indexer.assemblycontig_index(params['upa'])
        #END assemblycontig_index

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method assemblycontig_index return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def narrative_index(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN narrative_index
        output = self.indexer.narrative_index(params['upa'])
        #END narrative_index

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method narrative_index return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def ontologyterm_index(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN ontologyterm_index
        output = self.indexer.ontologyterm_index(params['upa'])
        #END ontologyterm_index

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method ontologyterm_index return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def pairedendlibrary_index(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN pairedendlibrary_index
        output = self.indexer.pairedend_index(params['upa'])
        #END pairedendlibrary_index

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method pairedendlibrary_index return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def pangenome_index(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN pangenome_index
        output = self.indexer.pangenome_index(params['upa'])
        #END pangenome_index

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method pangenome_index return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def pangenomeorthology_index(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN pangenomeorthology_index
        output = self.indexer.pangenomeorthologyfamily_index(params['upa'])
        #END pangenomeorthology_index

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method pangenomeorthology_index return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def rnaseqsampleset_index(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN rnaseqsampleset_index
        output = self.indexer.rnaseqsampleset_index(params['upa'])
        #END rnaseqsampleset_index

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method rnaseqsampleset_index return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def singleendlibrary_index(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN singleendlibrary_index
        output = self.indexer.singleend_index(params['upa'])
        #END singleendlibrary_index

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method singleendlibrary_index return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def taxon_index(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN taxon_index
        output = self.indexer.taxon_index(params['upa'])
        #END taxon_index

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method taxon_index return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def tree_index(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN tree_index
        output = self.indexer.tree_index(params['upa'])
        #END tree_index

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method tree_index return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
