# !/usr/bin/env python
#  -*- coding: UTF-8 -*-


#
#
# TEST ====
#
# query a GraphDB database and output results as json-ld
#
#

# legacy docs maybe
# https://github.com/RDFLib/rdflib-sparqlstore
# https://lawlesst.github.io/notebook/rdflib-stardog.html
# https://github.com/RDFLib/rdflib

from __future__ import print_function
from rdflib.plugins.stores.sparqlstore import SPARQLStore
from rdflib import Graph, ConjunctiveGraph

import sys
import time

try:
    from .queries import *
    from .timeout import *
except:
    print("TIP: run the script `python -m src.testGraphDB` from outside package folder")
    sys.exit(0)



MAX_TIMEOUT = 10 # seconds

SPARQL_ENDPOINT = "http://localhost:7200/repositories/scigraph-2016"


def main():

    store = SPARQLStore(SPARQL_ENDPOINT)
    g = ConjunctiveGraph(store=store)
    # g.bind("sg", "http://www.springernature.com/scigraph/ontologies/core/")

    # get a few articles
    q1 = g.query(ALL_ARTICLES_IDS_SAMPLE)
    for row in q1:
        print("Article URI:", str(row[0]))

    # extract more article info
    for row in q1:
        try:
            with time_limit(MAX_TIMEOUT):
                raw = g.query(ARTICLE_INFO_QUERY % str(row[0]))
                g1 =  ConjunctiveGraph()
                g1.parse(data=raw.serialize())

                # create JSON-LD
                context = {"@vocab": "http://elastic-index.scigraph.com/", "@language": "en"}
                print(g1.serialize(format='json-ld', context=context, indent=4))
                print("======")
        except TimeoutException, msg:
            error = "Timed out!"
            print(error)
        except Exception, e:
            error = "Exception: %s" % e
            print(error)









if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt, e:  # Ctrl-C
        raise e
