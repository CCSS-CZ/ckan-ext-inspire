import logging
import json

log = logging.getLogger(__name__)

def rdf_produce(pkg):
    return dict_produce(pkg.as_dict())

def dict_produce(data):
    extra = data.get('extras')
    rec = '''<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF
    xmlns:foaf="http://xmlns.com/foaf/0.1/"
    xmlns:owl="http://www.w3.org/2002/07/owl#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:dcat="http://www.w3.org/ns/dcat#"
    xmlns:dct="http://purl.org/dc/terms/"
    xmlns:skos="http://www.w3.org/2004/02/skos/core#"
    xmlns:prov="http://www.w3.org/ns/prov#"  
    xmlns:vcard="http://www.w3.org/2006/vcard/ns#"
>
'''
    rec += '<dcat:Description rdf:about="' + data.get('ckan_url', '') + '">'
    #rec += json.dumps(data)
    rec += '''
    <!-- METADATA ON METADATA -->  
    <foaf:isPrimaryTopicOf>
        <rdf:Description>
            <rdf:type rdf:resource="http://www.w3.org/ns/dcat#CatalogRecord"/>
            <!-- Metadata language -->      
            <dct:language rdf:resource="http://publications.europa.eu/resource/authority/language/'''
    rec += extra.get('metadata-language', '').upper()
    rec += '''"/>
        <!-- Metadata date -->        
        <dct:modified rdf:datatype="http://www.w3.org/2001/XMLSchema-datatypes#date">'''
    rec += extra.get('metadata-date', '').strip()
    rec += '''</dct:modified>
        <!-- Metadata point of contact -->'''
    for key, party in extra.items():
        if "metadata-party" in key:
            party = party.strip()
            party = ' '.join(party.split())
            party = json.loads(party)
            for part in party:
                rec += '''
                <dcat:contactPoint>
                    <vcard:Kind>
                        <vcard:organization-name>'''
                rec += part.get('organisationName').strip()
                rec += '''</vcard:organization-name>
                        <vcard:hasEmail rdf:resource="mailto:'''
                rec += part.get('email', '').strip()
                rec += '"/>'
                if part.get('url', None):
                    rec += '<vcard:hasURL rdf:resource="' + part.get('url').strip() + '"/>'
                rec += '''
                </vcard:Kind>
                </dcat:contactPoint>'''
                rec += '''<prov:qualifiedAttribution>
                    <prov:Attribution>
                        <prov:agent>
                            <vcard:Kind>
                                <vcard:organization-name'''
                if extra.get('mdlang2', ''):
                    rec += ' xml:lang="' + extra.get('mdlang2') + '"'
                rec += '>' + part.get('organisationName').strip()
                rec += '''</vcard:organization-name>
                                <vcard:hasEmail rdf:resource="mailto:'''
                rec += part.get('email', '').strip() + '"/>'
                if part.get('url', None):
                    rec += '''
                        <vcard:hasURL rdf:resource="''' + part.get('url') + '''"/>'''
                rec += '''</vcard:Kind>
                        </prov:agent>
                        <dct:type rdf:resource="http://inspire.ec.europa.eu/metadata-codelist/ResponsiblePartyRole/'''
                rec += part.get('role')
                rec += '''"/>
                    </prov:Attribution>
                </prov:qualifiedAttribution>
                '''
    rec += '<dct:identifier rdf:datatype="http://www.w3.org/2001/XMLSchema#string">'
    rec += extra.get('guid','').strip()
    rec += '''</dct:identifier>
        </rdf:Description>
    </foaf:isPrimaryTopicOf>'''
    rec += '''
    <!-- Resource type -->
    '''
    if extra.get('resource-type', None):
        if (extra.get('resource-type').strip() == 'dataset') or (extra.get('resource-type').strip() == 'series'):
            rec += '<rdf:type rdf:resource="http://www.w3.org/ns/dcat#Dataset"/>'
        else:
            rec += '<rdf:type rdf:resource="http://www.w3.org/ns/dcat#Catalog"/>'
        rec += '''
    <dct:type rdf:resource="http://inspire.ec.europa.eu/codelist/ResourceType/''' + extra.get('resource-type', None) + '''"/>
    '''
    rec += '''<!-- title -->
    <dct:title xml:lang="''' + extra.get('mdlang2', '') + '''">''' + data.get('title') + '''</dct:title>
    <!-- description -->
    <dct:description xml:lang="''' + extra.get('mdlang2', '') + '''">''' + data.get('notes') + '''</dct:description>
    '''
    rec += '''<owl:sameAs rdf:resource="urn:uuid:''' + data.get('id') + '''"/>
        '''
    for tag in data.get('tags'):
        rec += '''<dcat:keyword>''' + tag + '''</dcat:keyword>
        '''
    rec += '''<foaf:homepage rdf:resource="''' + data.get('ckan_url') + '''"/>
    '''
    rec += '''<rdfs:label>''' + data.get('name') + '''</rdfs:label>
    '''
    rec += '''<dct:identifier>''' + data.get('name') + '''</dct:identifier>
    '''
    rec += '''<!-- locator -->
    '''
    for rsrc in data.get('resources'):
        rec += '''<dcat:landingPage rdf:resource="''' + rsrc.get('url') + '''"/>
    '''
    for rsrc in data.get('resources'):
        rec += '''<dcat:distribution>
        <dcat:Distribution>
            <dcat:accessURL rdf:resource="''' + rsrc.get('url') + '''"/>
            '''
        if rsrc.get('format'):
            rec += '''<dct:format>
                        <dct:IMT>
                            <rdf:value>''' + rsrc.get('format') + '''</rdf:value>
                            <rdfs:label>''' + rsrc.get('format') + '''</rdfs:label>
                        </dct:IMT>
                    </dct:format>
                    '''
        if rsrc.get('name'):
            rec += '''<dct:title>''' + rsrc.get('name') + '''</dct:title>
            '''
        rec += '''</dcat:Distribution>
        </dcat:distribution>
        '''
    if data.get('author'):
        rec += '''<dct:creator>
            <rdf:Description>
                <foaf:name>''' + data.get('author') + '''</foaf:name>
                '''
        if data.get('author_email'):
            rec += '''<foaf:mbox rdf:resource="mailto:''' + data.get('author_email') + '''"/>
            '''
        rec += '''</rdf:Description>
    </dct:creator>
    '''
    if data.get('maintainer'):
        rec += '''<dct:contributor>
        <rdf:Description>
        '''
        rec += '''<foaf:name>''' + data.get('maintainer') + '''</foaf:name>
        '''
        if data.get('maintainer_email'):
            rec += '''<foaf:mbox rdf:resource="mailto:''' + data.get('maintainer_email') + '''"/>
        '''
        rec += '''</rdf:Description>
    </dct:contributor>
    '''

    if data.get('license_url'):
        rec += '''<dct:rights rdf:resource="''' + data.get('license_url') + '''"/>
        '''

    if extra.get('spatial-data-service-type'):
        rec += '''<dct:type rdf:resource="http://inspire.ec.europa.eu/metadata-codelist/SpatialDataServiceType/''' + extra.get('spatial-data-service-type') + '''"/>
        '''
    rec += '''<!--! topic category  -->
    '''
    if extra.get('topic-category'):
        cat = extra.get('topic-category')
        cat = json.loads(cat)
        for value in cat:
            rec += '''<dct:subject rdf:resource="http://inspire.ec.europa.eu/metadata-codelist/TopicCategory/''' + value + '''"/>
        '''
    rec += '''<!--! spatial - TODO - je jen pro BBOX -->
    <dct:spatial xmlns:locn="http://w3.org/ns/locn#" xmlns:gml="http://www.opengis.net/gml">
        <dct:Location>
            <locn:geometry rdf:datatype="http://www.opengis.net/rdf#GMLLiteral"><![CDATA[
                <gml:Envelope srsName="http://www.opengis.net/def/crs/OGC/1.3/CRS84">
                    <gml:lowerCorner>''' + extra.get('bbox-west-long') + ''' ''' + extra.get('bbox-south-lat') + '''</gml:lowerCorner>
                    <gml:upperCorner>''' + extra.get('bbox-east-long') + ''' ''' + extra.get('bbox-north-lat') + '''</gml:upperCorner>
                </gml:Envelope>]]>
            </locn:geometry>
        </dct:Location>
    </dct:spatial>
    '''

    if extra.get('dataset-language'):
        rec += '''<!--! resource language -->
        '''
        dlang = extra.get('dataset-language')
        dlang = json.loads(dlang)
        for value in dlang:
            rec += '''<dct:language rdf:resource="http://publications.europa.eu/resource/authority/language/''' + value.upper() + '''"/>
            '''

    rec += '''<!--! contactPoint 1 -->
    '''
    for key, party in extra.items():
        if "responsible-party1" in key:
            party = party.strip()
            party = ' '.join(party.split())
            party = json.loads(party)
            for part in party:
                rec += '''<dcat:contactPoint>
                <vcard:Kind>
                    <vcard:organization-name>''' + part.get('organisationName',None).strip() + '''</vcard:organization-name>
                    <vcard:hasEmail rdf:resource="mailto:''' + part.get('email').strip() + '''"/>
                    '''
                if part.get('url'):
                    rec += '''<vcard:hasURL rdf:resource="''' + part.get('url').strip() + '''"/>
                    '''
                rec += '''</vcard:Kind>
            </dcat:contactPoint>
                <prov:qualifiedAttribution>
                    <prov:Attribution>
                        <prov:agent>
                            <vcard:Kind>
                                <vcard:organization-name xml:lang="''' + extra.get('mdlang2','') + '''">''' + part.get('organisationName',None).strip() + '''</vcard:organization-name>
                                <vcard:hasEmail rdf:resource="mailto:''' + part.get('email').strip() + '''"/>
                                '''
                if part.get('url'):
                    rec += '''<vcard:hasURL rdf:resource="''' + part.get('url') + '''"/>
                    '''
                rec += '''</vcard:Kind>
                        </prov:agent>
                        <dct:type rdf:resource="http://inspire.ec.europa.eu/metadata-codelist/ResponsiblePartyRole/''' + part.get('role') + '''"/>
                    </prov:Attribution>
                </prov:qualifiedAttribution>
                '''

    rec += '''<!--! keywords  -->
        '''
        
    for key, dkey in extra.items():
        if "descriptive-keywords" in key:
            dkey = dkey.strip()
            dkey = ' '.join(dkey.split())
            dkey = json.loads(dkey)
            for dekey in dkey:
                for k in dekey.get('keywords'):
                    if k.get('uri'):
                        rec += '''<dcat:theme rdf:resource="''' + k.get('uri') + '''"/>
                        '''
                    else:
                        rec += '''<dcat:theme>
                        <skos:Concept>
                        <skos:prefLabel xml:lang="''' + extra.get('mdlang2','') + '''">''' + k.get('label',None) + '''</skos:prefLabel>
                        '''
                        if dekey.get('thesaurus').get('title'):
                            rec += '''<skos:inScheme>
                                            <skos:ConceptScheme>
                                                <rdfs:label xml:lang="''' + extra.get('mdlang2','') +'''">''' + dekey.get('thesaurus',None).get('title','') + '''</rdfs:label>
                                                <dct:issued rdf:datatype="http://www.w3.org/2001/XMLSchema#date">''' + dekey.get('thesaurus',None).get('date','').strip() + '''</dct:issued>
                                            </skos:ConceptScheme>
                                        </skos:inScheme>
                                        ''' 
                        rec += '''</skos:Concept>
                        </dcat:theme>
                        '''
    rec += '''<!-- lineage -->
    <dct:provenance>
        <dct:ProvenanceStatement>
            <rdfs:label xml:lang="''' + extra.get('mdlang2','') + '''">''' + extra.get('lineage',None) + '''</rdfs:label>
        </dct:ProvenanceStatement>
    </dct:provenance>
    '''

    rec += '''<dcat:distribution>
      <dcat:Distribution>    
        <!--! Conditions for access and use -->
        '''
    for key, accc in extra.items():
        if "access_constraints" in key:
            accc = json.loads(accc)
            for acc in accc:
                rec += '''<dct:rights>
                    <dct:RightsStatement>
                        <dct:label>''' + acc.strip() + '''</dct:label>
                    </dct:RightsStatement>
                </dct:rights>
                '''
    rec += '''<!--! Limitations on public access -->
    '''
    for key, lice in extra.items():
        if "licence" in key:
            lice = json.loads(lice)
            for lic in lice:
                rec += '''<dct:accessRights>
                    <dct:RightsStatement>
                        <dct:label>''' + lic.strip() + '''</dct:label>
                    </dct:RightsStatement>
                </dct:accessRights>
                '''
    rec += '''</dcat:Distribution>
    </dcat:distribution>'''
    rec += '''
    </dcat:Description>
</rdf:RDF>'''
    return rec
