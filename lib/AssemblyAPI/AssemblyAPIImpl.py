# -*- coding: utf-8 -*-
#BEGIN_HEADER
import doekbase.data_api.sequence.assembly.api
from doekbase.data_api import cache
import logging

from AssemblyAPI.AssemblyIndexer import AssemblyIndexer
#END_HEADER


class AssemblyAPI:
    '''
    Module Name:
    AssemblyAPI

    Module Description:
    A KBase module: AssemblyAPI
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.1.0"
    GIT_URL = ""
    GIT_COMMIT_HASH = "82897279c6b03e15a6574bffb5cf9d990e404381"

    #BEGIN_CLASS_HEADER
    workspaceURL = None
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspaceURL = config['workspace-url']
        self.shockURL = config['shock-url']
        self.handleURL = config['handle-service-url']
        self.logger = logging.getLogger()
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        self.logger.addHandler(log_handler)


        self.services = {
                "workspace_service_url": self.workspaceURL,
                "shock_service_url": self.shockURL,
                "handle_service_url": self.handleURL,
            }
        try:
            cache_dir = config['cache_dir']
        except:
            cache_dir = None
        try:
            redis_host = config['redis_host']
            redis_port = config['redis_port']
        except:
            redis_host = None
            redis_port = None
        if redis_host is not None and redis_port is not None:
            self.logger.info("Activating REDIS at host:{} port:{}".format(redis_host, redis_port))
            cache.ObjectCache.cache_class = cache.RedisCache
            cache.ObjectCache.cache_params = {'redis_host': redis_host, 'redis_port': redis_port}
        elif cache_dir is not None:
            self.logger.info("Activating File")
            cache.ObjectCache.cache_class = cache.DBMCache
            cache.ObjectCache.cache_params = {'path':cache_dir,'name':'data_api'}
        else:
            self.logger.info("Not activating REDIS")



        self.indexer = AssemblyIndexer(config)

        #END_CONSTRUCTOR
        pass


    def search_contigs(self, ctx, params):
        """
        :param params: instance of type "SearchAssemblyOptions" (num_found -
           optional field which when set informs that there is no need to
           perform full scan in order to count this value because it was
           already done before; please don't set this value with 0 or any
           guessed number if you didn't get right value previously.) ->
           structure: parameter "ref" of String, parameter "query" of String,
           parameter "sort_by" of list of type "column_sorting" -> tuple of
           size 2: parameter "column" of String, parameter "ascending" of
           type "boolean" (Indicates true or false values, false = 0, true =
           1 @range [0,1]), parameter "start" of Long, parameter "limit" of
           Long, parameter "num_found" of Long
        :returns: instance of type "SearchAssemblyResult" (num_found - number
           of all items found in query search (with only part of it returned
           in "bins" list).) -> structure: parameter "query" of String,
           parameter "start" of Long, parameter "contigs" of list of type
           "AssemblyData" (contig_id - id of the contig description -
           description of the contig (description on fasta header rows)
           length - (bp) length of the contig gc - gc_content of the contig
           is_circ - 0 or 1 value indicating if the contig is circular.  May
           be null if unknown N_count - number of 'N' bases in the contig md5
           - md5 checksum of the sequence) -> structure: parameter
           "contig_id" of String, parameter "description" of String,
           parameter "length" of Long, parameter "gc" of Long, parameter
           "is_circ" of Long, parameter "N_count" of Long, parameter "md5" of
           String, parameter "num_found" of Long
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN search_contigs
        result = self.indexer.search_contigs(ctx["token"],
                                             params.get("ref", None),
                                             params.get("query", None),
                                             params.get("sort_by", None),
                                             params.get("start", None),
                                             params.get("limit", None),
                                             params.get("num_found", None))
        #END search_contigs

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method search_contigs return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]

    def get_assembly_id(self, ctx, ref):
        """
        Retrieve Assembly ID.
        :param ref: instance of type "ObjectReference" (Insert your typespec
           information here.)
        :returns: instance of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_assembly_id
        assembly_api = doekbase.data_api.sequence.assembly.api.AssemblyAPI(self.services, ctx['token'], ref)
        returnVal=assembly_api.get_assembly_id()
        #END get_assembly_id

        # At some point might do deeper type checking...
        if not isinstance(returnVal, basestring):
            raise ValueError('Method get_assembly_id return value ' +
                             'returnVal is not type basestring as required.')
        # return the results
        return [returnVal]

    def get_genome_annotations(self, ctx, ref):
        """
        Retrieve associated GenomeAnnotation objects.
        @return List of GenomeAnnotation object references
        :param ref: instance of type "ObjectReference" (Insert your typespec
           information here.)
        :returns: instance of list of type "ObjectReference" (Insert your
           typespec information here.)
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_genome_annotations
        assembly_api = doekbase.data_api.sequence.assembly.api.AssemblyAPI(self.services, ctx['token'], ref)
        returnVal=assembly_api.get_genome_annotations(ref_only=True)
        #END get_genome_annotations

        # At some point might do deeper type checking...
        if not isinstance(returnVal, list):
            raise ValueError('Method get_genome_annotations return value ' +
                             'returnVal is not type list as required.')
        # return the results
        return [returnVal]

    def get_external_source_info(self, ctx, ref):
        """
        Retrieve the external source information for this Assembly.
        @return Metadata about the external source
        :param ref: instance of type "ObjectReference" (Insert your typespec
           information here.)
        :returns: instance of type "AssemblyExternalSourceInfo" (* * Metadata
           about the external source of this Assembly.) -> structure:
           parameter "external_source" of String, parameter
           "external_source_id" of String, parameter
           "external_source_origination_date" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_external_source_info
        assembly_api = doekbase.data_api.sequence.assembly.api.AssemblyAPI(self.services, ctx['token'], ref)
        returnVal=assembly_api.get_external_source_info()
        #END get_external_source_info

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_external_source_info return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_stats(self, ctx, ref):
        """
        Retrieve the derived statistical information about this Assembly.
        :param ref: instance of type "ObjectReference" (Insert your typespec
           information here.)
        :returns: instance of type "AssemblyStats" (* * Derived statistical
           information about an assembly.) -> structure: parameter
           "num_contigs" of type "i64", parameter "dna_size" of type "i64",
           parameter "gc_content" of type "double"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_stats
        assembly_api = doekbase.data_api.sequence.assembly.api.AssemblyAPI(self.services, ctx['token'], ref)
        returnVal=assembly_api.get_stats()
        #END get_stats

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_stats return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_number_contigs(self, ctx, ref):
        """
        Retrieve the number of contigs for this Assembly.
        @return Total number of contiguous sequences.
        :param ref: instance of type "ObjectReference" (Insert your typespec
           information here.)
        :returns: instance of Long
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_number_contigs
        assembly_api = doekbase.data_api.sequence.assembly.api.AssemblyAPI(self.services, ctx['token'], ref)
        returnVal=assembly_api.get_number_contigs()
        #END get_number_contigs

        # At some point might do deeper type checking...
        if not isinstance(returnVal, int):
            raise ValueError('Method get_number_contigs return value ' +
                             'returnVal is not type int as required.')
        # return the results
        return [returnVal]

    def get_gc_content(self, ctx, ref):
        """
        Retrieve the total GC content for this Assembly.
        @return Proportion of GC content, between 0 and 1.
        :param ref: instance of type "ObjectReference" (Insert your typespec
           information here.)
        :returns: instance of type "double"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_gc_content
        assembly_api = doekbase.data_api.sequence.assembly.api.AssemblyAPI(self.services, ctx['token'], ref)
        returnVal=assembly_api.get_gc_content()
        #END get_gc_content

        # At some point might do deeper type checking...
        if not isinstance(returnVal, float):
            raise ValueError('Method get_gc_content return value ' +
                             'returnVal is not type float as required.')
        # return the results
        return [returnVal]

    def get_dna_size(self, ctx, ref):
        """
        Retrieve the total DNA size for this Assembly.
        @return Total DNA size
        :param ref: instance of type "ObjectReference" (Insert your typespec
           information here.)
        :returns: instance of Long
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_dna_size
        assembly_api = doekbase.data_api.sequence.assembly.api.AssemblyAPI(self.services, ctx['token'], ref)
        returnVal=assembly_api.get_dna_size()
        #END get_dna_size

        # At some point might do deeper type checking...
        if not isinstance(returnVal, int):
            raise ValueError('Method get_dna_size return value ' +
                             'returnVal is not type int as required.')
        # return the results
        return [returnVal]

    def get_contig_ids(self, ctx, ref):
        """
        Retrieve the contig identifiers for this Assembly.
        @return List of contig IDs.
        :param ref: instance of type "ObjectReference" (Insert your typespec
           information here.)
        :returns: instance of list of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_contig_ids
        assembly_api = doekbase.data_api.sequence.assembly.api.AssemblyAPI(self.services, ctx['token'], ref)
        returnVal=assembly_api.get_contig_ids()
        #END get_contig_ids

        # At some point might do deeper type checking...
        if not isinstance(returnVal, list):
            raise ValueError('Method get_contig_ids return value ' +
                             'returnVal is not type list as required.')
        # return the results
        return [returnVal]

    def get_contig_lengths(self, ctx, ref, contig_id_list):
        """
        Retrieve the lengths of the contigs in this Assembly.
        @return Mapping of contig ID to contig length.
        :param ref: instance of type "ObjectReference" (Insert your typespec
           information here.)
        :param contig_id_list: instance of list of String
        :returns: instance of mapping from String to Long
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_contig_lengths
        assembly_api = doekbase.data_api.sequence.assembly.api.AssemblyAPI(self.services, ctx['token'], ref)
        returnVal=assembly_api.get_contig_lengths(contig_id_list)
        #END get_contig_lengths

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_contig_lengths return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_contig_gc_content(self, ctx, ref, contig_id_list):
        """
        Retrieve the gc content for contigs in this Assembly.
        @return Mapping of contig IDs to GC content proportion.
        :param ref: instance of type "ObjectReference" (Insert your typespec
           information here.)
        :param contig_id_list: instance of list of String
        :returns: instance of mapping from String to type "double"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_contig_gc_content
        assembly_api = doekbase.data_api.sequence.assembly.api.AssemblyAPI(self.services, ctx['token'], ref)
        returnVal=assembly_api.get_contig_gc_content(contig_id_list)
        #END get_contig_gc_content

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_contig_gc_content return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_contigs(self, ctx, ref, contig_id_list):
        """
        Retrieve all the data for the contigs in this Assembly.
        @return Mapping of contig ID to details for that contig.
        :param ref: instance of type "ObjectReference" (Insert your typespec
           information here.)
        :param contig_id_list: instance of list of String
        :returns: instance of mapping from String to type "AssemblyContig" ->
           structure: parameter "contig_id" of String, parameter "sequence"
           of String, parameter "length" of type "i64", parameter
           "gc_content" of type "double", parameter "md5" of String,
           parameter "name" of String, parameter "description" of String,
           parameter "is_complete" of type "bool", parameter "is_circular" of
           type "bool"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_contigs
        assembly_api = doekbase.data_api.sequence.assembly.api.AssemblyAPI(self.services, ctx['token'], ref)
        returnVal=assembly_api.get_contigs(contig_id_list)
        #END get_contigs

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_contigs return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK", 'message': "", 'version': self.VERSION, 
                     'git_url': self.GIT_URL, 'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
