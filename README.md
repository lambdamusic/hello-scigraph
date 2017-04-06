# intro

An examples of how to load data from SciGraph and doing something useful with it.

- https://github.com/springernature/scigraph/wiki
- https://github.com/RDFLib/rdflib-jsonld
- https://rdflib.readthedocs.io/en/stable/intro_to_sparql.html
- https://tryolabs.com/blog/2015/02/17/python-elasticsearch-first-steps/
- https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html
- https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html

@todo: create a docType in a pythonic way
- https://elasticsearch-dsl.readthedocs.io/en/latest/persistence.html#doctype




# graph db setup

Create a repo called scigraph-2016
turn off inference for now

# notes

- check that we have subjects @done
- other fields to add: journal issn maybe? @done
- grid IDs for researchers @done
- grants and @done
- need to group org data otherwise they are separate! @done
- time the overall process @ could be done by launching with 'time', or just the log
- timeout GraphDB after 1minute, produce a log of these problems @done




# Errors

2017-03-24 http://www.springernature.com/scigraph/things/articles/9a134c934df47032b6550b9ac9ecea71

//www.springernature.com/scigraph/things/articles/5ccb1a7a4e1bca6c2a150f848c907e8e


> update 2017-03-23:  seems to be fixed after altering the construct graph (properties of GRID subject, instead of article) and also removing the 'publishedname' property)

The folowing query with article ID <http://www.springernature.com/scigraph/things/articles/06366821d60a729d83de02ce4c7c3c8d> returns many duplicates..
Seems related to the ?o foaf:homepage ?orgHomepage pattern.

WHY?

```
prefix sg: <http://www.springernature.com/scigraph/ontologies/core/>
prefix skos: <http://www.w3.org/2004/02/skos/core#>
prefix es: <http://elastic-index.scigraph.com/>
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix grid: <http://www.grid.ac/ontology/>
prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>

 construct {
    ?x es:scigraphId ?sgId .
    ?x es:title ?title .
    ?x es:doi ?doi .
    ?x es:doiLink ?link .
    ?x es:abstract ?ab .
    ?x es:fieldOfResearch ?forlabel .
    ?x es:subject ?subjectlabel .
    ?x es:journalIssn ?issn .
    ?x es:journalTitle ?jtitle .
    ?x es:journalUrl ?jurl .
    ?x es:journalOpenAccess ?joa .
    ?x es:pubDate ?pubdate .
    ?x es:pubYear ?pubyear .
    ?x es:language ?language .
    ?x es:orgName ?orgName .
    ?x es:orgGrid ?o .
    ?x es:orgHomepage ?orgHomepage .
    ?x es:orgWikipage ?orgWikipage .
    ?x es:orgCountry ?orgCountry .
    ?x es:orgLatitude ?orgLat .
    ?x es:orgLongitude ?orgLong .
    ?x es:fundingGrant ?grantPage .
    ?x es:fundingGrantTitle ?grantTitle .
}
where
{   BIND (<http://www.springernature.com/scigraph/things/articles/06366821d60a729d83de02ce4c7c3c8d> AS ?x) .
    ?x sg:scigraphId ?sgId .
    # === basic biblio metadata ===
    OPTIONAL  { ?x sg:title ?title }
    OPTIONAL { ?x sg:doi ?doi }
    OPTIONAL { ?x sg:doiLink ?link }
    OPTIONAL { ?x sg:abstract ?ab }
    OPTIONAL { ?x sg:publicationDate ?pubdate }
    OPTIONAL { ?x sg:publicationYear ?pubyear }
    OPTIONAL { ?x sg:language ?language }
    OPTIONAL { ?x sg:hasJournal ?j . ?j sg:issn ?issn }
    OPTIONAL { ?x sg:hasJournal ?j . ?j sg:hasJournalBrand ?jb . ?jb sg:title ?jtitle }
    OPTIONAL { ?x sg:hasJournal ?j . ?j sg:hasJournalBrand ?jb . ?jb sg:webpage ?jtitle }
    OPTIONAL { ?x sg:hasJournal ?j . ?j sg:hasJournalBrand ?jb . ?jb sg:openAccess ?joa }
    # === categories ===
    OPTIONAL { ?x sg:hasFieldOfResearchCode ?for . ?for skos:prefLabel ?forlabel }
    OPTIONAL { ?x sg:hasSubject ?subject . ?subject skos:prefLabel ?subjectlabel }
    # === organization info ===
    OPTIONAL { ?x sg:hasContribution ?c . ?c sg:hasAffiliation ?a .     ?a sg:publishedName ?orgName .  ?a sg:hasOrganization ?o }
    # the following causes duplicated data! see README
    OPTIONAL { ?x sg:hasContribution ?c . ?c sg:hasAffiliation ?a .     ?a sg:publishedName ?name .  ?a sg:hasOrganization ?o  . ?o foaf:homepage ?orgHomepage}
    OPTIONAL { ?x sg:hasContribution ?c . ?c sg:hasAffiliation ?a .     ?a sg:publishedName ?name .  ?a sg:hasOrganization ?o . ?o grid:wikipediaPage ?orgWikipage .}
    OPTIONAL { ?x sg:hasContribution ?c . ?c sg:hasAffiliation ?a .     ?a sg:publishedName ?name .  ?a sg:hasOrganization ?o .  ?o grid:hasAddress ?address .  ?address grid:countryName ?orgCountry .  ?address geo:lat ?orgLat .  ?address geo:long ?orgLong . }
    # === grant info ===
    OPTIONAL { ?grant sg:hasFundedPublication ?x . ?grant sg:title ?grantTitle  }
    OPTIONAL { ?grant sg:hasFundedPublication ?x . ?grant sg:webpage ?grantPage }.
}
```


Another very long query with http://www.springernature.com/scigraph/things/articles/5ccb1a7a4e1bca6c2a150f848c907e8e
