#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
Load a folder containin RDF files into GraphDB from the command line

python -m hello-scigraph.loadGraphDB ~/path/to/scigraph-downloads/

"""



import os, sys


# PARAMETERS

GRAPH_DB = "scigraph-2016"



# METHODS


def clean_repo(db):
    """
    Removes all content from DB

    http://rdf4j.org/doc/the-rdf4j-server-rest-api/#Repository_statements

    """
    print >> sys.stderr, "Erasing DB:", db, "\n-----------------"
    os.system("curl -X DELETE http://localhost:7200/repositories/%s/statements" % db)


def add_triples_from_file(filename, db):
    """
    Add content to DB

    Essentially a wrapper around curl:

    ```
    curl -X POST -H "Content-Type:application/n-triples" -T springernature-scigraph-subjects.2017-02-15.nt http://localhost:7200/repositories/scigraph-2016/statements
    ```

    See also:
    > http://graphdb.ontotext.com/documentation/free/quick-start-guide.html
    > http://www.iana.org/assignments/media-types/media-types.xhtml
    """
    print >> sys.stderr, "...",  filename

    if filename.endswith(".rdf"):
        _cmd = """curl -X POST -H "Content-Type:application/x-turtle" -T %s http://localhost:7200/repositories/%s/statements""" % (filename, db)
        os.system(_cmd)
    elif filename.endswith(".nt"):
        _cmd = """curl -X POST -H "Content-Type:application/n-triples" -T %s http://localhost:7200/repositories/%s/statements""" % (filename, db)
        os.system(_cmd)
    else:
        _cmd = """curl -X POST -H "Content-Type:application/rdf+xml" -T %s http://localhost:7200/repositories/%s/statements""" % (filename, db)
        os.system(_cmd)



def getRDFFiles(folder):
    """walk dir and return RDF files as a list
        note: this is recursive
    """
    out = []
    rdf_extensions = ['.ttl', '.rdf', '.nt']
    if os.path.exists(folder):
        for root, dirs, files in os.walk(folder):
            for file in files:
                for e in rdf_extensions:
                    if file.endswith(e):
                        out += [os.path.join(root, file)]

    else:
        print >> sys.stderr, "WARNING: the folder <%s> doesn't exist!" % folder
    return out




def main():
    """
    Pass a folder name, loads all RDF files into graphdb (note: recursive
    directory browser)

    """

    try:
        folder = sys.argv[1]
    except:
        print >> sys.stderr, "Please specify a folder containing RDF"
        sys.exit(0)

    files_list = getRDFFiles(folder)
    print >> sys.stderr, "==Found %s files==" % len(files_list)

    # # if needed:
    if False:
        cleanRepo()


    for f in files_list:
        add_triples_from_file(f, GRAPH_DB)




if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt, e:  # Ctrl-C
        raise e
