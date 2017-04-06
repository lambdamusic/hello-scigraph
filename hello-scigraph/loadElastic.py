#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Creates an elasticsearch index with denormalized article data coming from GraphDB

Usage:

> python -m hello-scigraph.loadElastic

"""


from __future__ import print_function
import json, sys, time
from rdflib.plugins.stores.sparqlstore import SPARQLStore
from rdflib import Graph, ConjunctiveGraph
from elasticsearch import Elasticsearch

import logging
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("elasticsearch").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG, filename='loadElastic.log',)



try:
    from .queries import *
    from .timeout import *
except:
    print("TIP: run the script `python -m hello-scigraph.loadElasticSearch` from outside package folder")
    sys.exit(0)


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
store = SPARQLStore("http://localhost:7200/repositories/scigraph-2016")
g = ConjunctiveGraph(store=store)

ES_INDEX_NAME = "sg-2017-03-24"
MAX_TIMEOUT = 60 # seconds



def extract_article_info(row, i):
    # extract more article info
    articleUri = str(row[0])
    raw = g.query(ARTICLE_INFO_QUERY % articleUri)

    g1 =  ConjunctiveGraph()
    g1.parse(data=raw.serialize())

    context = {"@vocab": "http://elastic-index.scigraph.com/", "@language": "en"}
    json_str = g1.serialize(format='json-ld', context=context, indent=4)
    print("Adding article [%d] to index: %s ... " % (i, ES_INDEX_NAME))
    # note: if not including a context, you must use
    # json.loads(json_str)[0] extracts the dict (from a top level list)
    es.index(index=ES_INDEX_NAME, doc_type='articles', id=articleUri, body=json.loads(json_str))
    print("======")




offset = 0
offset_size = 200
index = offset  # used for monitoring progress

logging.info("\n========\nScript Started Running \n=========\n")

while True:

    print("============ Batch %d - %d ============"  % (offset, offset+offset_size))
    q1 = g.query(ALL_ARTICLES_IDS_OFFSET % (offset_size, offset))
    if q1:
        for row in q1:
            print("Article URI:", str(row[0]))
            index += 1
            # force a timeout
            try:
                with time_limit(MAX_TIMEOUT):
                    extract_article_info(row, index)
            except TimeoutException, msg:
                error = "Timed out!"
                print(error)
                logging.error("[ERROR] TIMED OUT: %s" % str(row[0]))
            except Exception, e:
                error = "Exception: %s" % e
                print(error)
                logging.error("[ERROR] EXCEPTION WITH: %s" % str(row[0]))

        offset += 200
        print("+++Waiting 10 seconds to let GraphDB catch breath..")
        time.sleep(10) # wait 10 seconds
    else:
        print("finished")
        logging.info("Completed with index: %d" % index)
        sys.exit(0)
