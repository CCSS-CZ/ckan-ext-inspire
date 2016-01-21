import re
import urllib
import urlparse

import logging

from ckan import model

from ckan.plugins.core import SingletonPlugin, implements

from ckanext.harvest.interfaces import IHarvester
from ckanext.harvest.model import HarvestObject
from ckanext.harvest.model import HarvestObjectExtra as HOExtra

from ckanext.spatial.lib.csw_client import CswService
from ckanext.spatial.harvesters.base import SpatialHarvester, text_traceback
from ckanext.spatial.harvesters.csw import CSWHarvester

from  ckan.lib.helpers import json
import math

from lxml import etree
import os

log = logging.getLogger(__name__)

xsl_path = os.path.abspath(os.path.dirname(__file__))
xsl_temp = xsl_path + "/" + "iso2json.xsl"


class InspireHarvester(CSWHarvester, SingletonPlugin):
    def info(self):
        return {
            'name': 'Inspire Harverster',
            'title': 'CSW server (Inspire)',
            'description': 'Harvests Inspire metadata from server instances via CSW',
            'form_config_interface': 'Text'
        }

    def get_package_dict(self, iso_values, harvest_object):

        package_dict = super(InspireHarvester, self).get_package_dict(iso_values, harvest_object)

        # Add default_tags from config
        default_tags = self.source_config.get('default_tags', [])
        if default_tags:
            for tag in default_tags:
                package_dict['tags'].append({'name': tag})

        # Add default_extras from config
        default_extras = self.source_config.get('default_extras', {})
        if default_extras:
            override_extras = self.source_config.get('override_extras', False)

            existing_keys = [entry.get('key') for entry in package_dict['extras']]

            for key, value in default_extras.iteritems():
                # log.debug('Processing extra %s', key)
                if not key in existing_keys or override_extras:
                    # Look for replacement strings
                    if isinstance(value, basestring):
                        value = value.format(
                            harvest_source_id=str(harvest_object.job.source.id),
                            harvest_source_url=str(harvest_object.job.source.url).strip('/'),
                            harvest_source_title=str(harvest_object.job.source.title),
                            harvest_job_id=str(harvest_object.job.id),
                            harvest_object_id=str(harvest_object.id),
                            guid=str(harvest_object.guid))
                    package_dict['extras'].append({'key': key, 'value': value})
                else:
                    log.debug('Skipping existing extra %s', key)

        # parse and work with XML
        inspire_xml = '<?xml version="1.0" encoding="UTF-8"?>' + harvest_object.content.encode('utf-8')
        inspire_dom = etree.fromstring(inspire_xml)
        inspire_template = etree.parse(xsl_temp)
        inspire_transform = etree.XSLT(inspire_template)
        inspire_ndom = inspire_transform(inspire_dom)

        rec = {}
        inspire_string = str(inspire_ndom)
        inspire_string = inspire_string.replace("\t", "")
        inspire_string = inspire_string.replace("\r", "")
        inspire_string = inspire_string.replace("\n", "")
        inspire_string = inspire_string.lstrip()
        inspire_string = inspire_string.rstrip()

        exec(inspire_string)

        for key, value in rec.iteritems():
            value = value.lstrip()
            value = value.rstrip()
            package_dict['extras'].append({'key': key, 'value': value.decode('utf-8')})

        # Add harvester info
        package_dict['extras'].append({'key': 'inspire_harvester', 'value': 'true'})

        # End of processing, return the modified package
        return package_dict

