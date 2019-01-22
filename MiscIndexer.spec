/*
A KBase module: MiscIndexer
*/

module MiscIndexer {
    typedef structure {
        string file_name;
        UnspecifiedObject index;
    } Results;

    funcdef assembly_index(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

    funcdef assemblycontig_index(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

    funcdef narrative_index(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

    funcdef ontologyterm_index(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

    funcdef pairedendlibrary_index(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

    funcdef pangenome_index(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

    funcdef pangenomeorthology_index(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

    funcdef rnaseqsampleset_index(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

    funcdef singleendlibrary_index(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

    funcdef taxon_index(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

    funcdef tree_index(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

};


