#!/usr/bin/python
# -*- coding: utf-8 -*-



# ==================
# March 24, 2017
# ==================

ALL_ARTICLES_IDS_SAMPLE = """
        prefix sg: <http://www.springernature.com/scigraph/ontologies/core/>
        select ?a where {?a a sg:Article . ?a sg:scigraphId ?id}  order by ?id limit 10
"""

ALL_ARTICLES_IDS_OFFSET = """
        prefix sg: <http://www.springernature.com/scigraph/ontologies/core/>
        select ?a where {?a a sg:Article . ?a sg:scigraphId ?id} order by ?id limit %d offset %d
"""



# ==================
# March 24, 2017 : ARTICLE_INFO_QUERY
# ==================

# note: types are added to query for better readability
# also, the graph has multiple subjects to make sure it's alwasy serialized in JSON-LD using the structures
# "@context": {
#         "@language": "en",
#         "@vocab": "http://elastic-index.scigraph.com/"
#     },
#     "@graph": [ .....

ARTICLE_INFO_QUERY = """
    prefix sg: <http://www.springernature.com/scigraph/ontologies/core/>
    prefix skos: <http://www.w3.org/2004/02/skos/core#>
    prefix es: <http://elastic-index.scigraph.com/>
    prefix foaf: <http://xmlns.com/foaf/0.1/>
    prefix grid: <http://www.grid.ac/ontology/>
    prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>

    construct {
        ?x es:scigraphId ?sgId .
        ?x a es:Article .
        ?x es:title ?title .
        ?x es:doi ?doi .
        ?x es:doiLink ?link .
        ?x es:abstract ?ab .
        ?x es:fieldOfResearch ?forlabel .
        ?x es:subject ?subjectlabel .
        # ?x es:journalIssn ?issn .
        # ?x es:journalTitle ?jtitle .
        # ?x es:journalUrl ?jurl .
        # ?x es:journalOpenAccess ?joa .
        ?x es:journal ?j .
        ?j a es:Journal .
        ?j es:journalIssn ?issn .
        ?j es:journalTitle ?jtitle .
        ?j es:journalUrl ?jurl .
        ?j es:journalOpenAccess ?joa .
        ?x es:pubDate ?pubdate .
        ?x es:pubYear ?pubyear .
        ?x es:language ?language .
        ?x es:orgGrid ?o .
        ?o a es:Organization .
        ?o es:orgName ?orgName .
        ?o es:orgHomepage ?orgHomepage .
        ?o es:orgWikipage ?orgWikipage .
        ?o es:orgCountry ?orgCountry .
        ?o es:orgLatitude ?orgLat .
        ?o es:orgLongitude ?orgLong .
        ?x es:fundingGrant ?grant .
        ?grant a es:Grant .
        ?grant es:fundingGrantTitle ?grantTitle .
        ?grant es:fundingGrantPage ?grantPage .
    }
    where
    {   BIND (<%s> AS ?x) .
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
        OPTIONAL { ?x sg:hasContribution ?c . ?c sg:hasAffiliation ?a .  ?a sg:hasOrganization ?o }
        # the following caused duplicated data! now fixed
        OPTIONAL { ?x sg:hasContribution ?c . ?c sg:hasAffiliation ?a . ?a sg:hasOrganization ?o  . ?o foaf:homepage ?orgHomepage}
        OPTIONAL { ?x sg:hasContribution ?c . ?c sg:hasAffiliation ?a . ?a sg:hasOrganization ?o . ?o skos:prefLabel ?orgName .}
        OPTIONAL { ?x sg:hasContribution ?c . ?c sg:hasAffiliation ?a . ?a sg:hasOrganization ?o . ?o grid:wikipediaPage ?orgWikipage .}
        OPTIONAL { ?x sg:hasContribution ?c . ?c sg:hasAffiliation ?a .  ?a sg:hasOrganization ?o .  ?o grid:hasAddress ?address .  ?address grid:countryName ?orgCountry .  ?address geo:lat ?orgLat .  ?address geo:long ?orgLong . }
        # === grant info ===
        OPTIONAL { ?grant sg:hasFundedPublication ?x . ?grant sg:title ?grantTitle  }
        OPTIONAL { ?grant sg:hasFundedPublication ?x . ?grant sg:webpage ?grantPage }.

    }
"""
