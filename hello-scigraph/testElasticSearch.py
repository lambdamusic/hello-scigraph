#!/usr/bin/python
# -*- coding: utf-8 -*-


# tip: access from browser via http://localhost:9200/sg/articles/1

from elasticsearch import Elasticsearch
import json
import os

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# list all indices
_cmd = """curl http://localhost:9200/_aliases?pretty=1"""
os.system(_cmd)


if False:
    # retrieve one article
    print(es.get(index='sg', doc_type='articles', id=5))

if False:
    # inner structures are accessible via the '.' dot notation!
    print(es.search(index="sg", body={"query": {"match": {'http://my-output/title.@value': 'energy'}}}))


# deleting an index
if False:
    print("deleting index...")
    _cmd = """curl -XDELETE localhost:9200/sg"""
    os.system(_cmd)


# see also: http://stackoverflow.com/questions/22924300/removing-data-from-elasticsearch

#
# Using cURL
#
# curl -XDELETE localhost:9200/index/type/documentID
# e.g.
#
# curl -XDELETE localhost:9200/shop/product/1
# You will then receive a reply as to whether this was successful or not. You can delete an entire index or types with an index also, you can delete a type by leaving out the document ID like so -
#
# curl -XDELETE localhost:9200/shop/product
# If you wish to delete an index -
#
# curl -XDELETE localhost:9200/shop
