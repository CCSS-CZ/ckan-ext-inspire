# INSPIRE CKAN extensions
These extensions are designed for work with [INSPIRE metadata](http://inspire.ec.europa.eu/index.cfm/pageid/101) in [CKAN](http://ckan.org/).

## inspire_harvester
This module extends csw_harvester and spatial_metadata extensions to support harvesting of all INSPIRE required metadata elements from [CSW 2.0.2 ISO AP 1.0](http://www.opengeospatial.org/standards/cat).

Depends on:
-  https://github.com/ckan/ckanext-harvest
-  https://github.com/ckan/ckanext-spatial
    - csw_harvester
    - spatial_metadata

## inspire_theme
This extension enables:
- Display INSPIRE metadata user friendly form at CKAN interface.
- Export INSPIRE metadata in extended [GeoDCAT-AP 1.0](https://joinup.ec.europa.eu/node/139283/) RDF format.

Depends on:
- inspire_harvester


## Installation
Copy plugins into ckan/src directory. In plugins folder run `python setup.py develop`.
In CKAN configuration file add plugins:
- for inspire_harvester - `inspire_harvester`
- for inspire_theme - `inspire_theme` - the endpoint is `rdfi` - to avoid conflicts with other extensions

## License
This material is open and licensed under the GNU Affero General Public License (AGPL) v3.0 whose full text may be found at:
http://www.fsf.org/licensing/licenses/agpl-3.0.html

###### These extensions are still under development. Any comments are welcome.



