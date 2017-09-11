import logging
from pylons import response
from ckan import model
from ckan.model import Package

from ckan.controllers.api import ApiController
from ckan.lib.base import abort

from ckanext.inspire_theme.produce import rdf_produce

log = logging.getLogger(__name__)

class InspireThemeController(ApiController):

    def show(self,id):
        package = Package.get(id)
        if package:
            doc = rdf_produce(package)
			
            response.content_type = 'application/rdf+xml'
            response.headers['Content-Length'] = len(doc)

            return doc
        else:
            abort(404)