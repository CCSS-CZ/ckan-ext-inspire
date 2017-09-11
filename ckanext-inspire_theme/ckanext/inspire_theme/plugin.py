# -*- coding: utf-8 -*-
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib
import re
import logging
import os
try:
	import json
except ImportError:
	import simplejson as json

log = logging.getLogger(__name__)


def toobj(term): 
	term = re.sub('\s\s+', ' ', term)
	#term = re.sub('^\[\s\{', '[{', term)
	#term = re.sub('}\s]$', '}]', term)
	try:
		termj = json.loads(term)
		#term = json.dumps(termj, indent=0, separators=(', ', ' : '))
		# p = re.compile(ur'\\u\d\d')
		# m = re.search(p, term)
		# if m:
			# term = term.decode('unicode_escape')
	except:
		log.debug('Nelze JSON %s', term)
	return termj


def list2dict(l):
	d = {}
	for i in range(len(l)):
		d[l[i]['key']] = l[i]['value']
	return d


def dict(lang):
	tdir = os.path.dirname(__file__)
	dictname = os.path.join(tdir, "dict/dict."+lang[:2]+".json")
	if not os.path.exists(dictname):
		dictname = os.path.join(tdir, "dict/dict.en.json")
	f = open(dictname, 'r')
	s = f.read()
	f.close()
	j = json.loads(s)
	return j


def humanreadable(key, term, dict):
	# dict je berlicka, jak tam propasirovat globalni adresar, lepe cist primo v objektu
	'''Return a readable string.'''
	log = logging.getLogger(__name__)
	if key == 'micka_harvester':
		log.debug('micka_harvester key')
	else:
		log.debug('Term = %s', term)
		log.debug('Key = %s', key)
		# replace multiple spaces with one
		term = re.sub('\s\s+', ' ', term)
		term = re.sub('^\[\s\{', '[{', term)
		term = re.sub('}\s]$', '}]', term)
		try:
			termj = json.loads(term)
			if (key == 'metadata-party') or (key == 'responsible-party1'):
				for i in range(len(termj)):
					if i>0: term += '<hr/>'
					term = '<b>' + termj[i]['organisationName'] + '</b><br />'
					if termj[i]['individualName']:
						term += termj[i]['individualName'] + '<br />'
					term += termj[i]['deliveryPoint'] + '<br />'
					term += termj[i]['city'] + '<br />'
					term += termj[i]['postalCode'] + '<br />'
					if termj[i]['url']: term += '<br /><span class="rlabel">url:</span>' + termj[i]['url']
					if termj[i]['email']: term += '<br /><span class="rlabel">e-mail:</span>' + termj[i]['email']
					if termj[i]['phone']: term += '<br /><span class="rlabel">phone:</span>' + termj[i]['phone']
					if termj[i]['positionName']: term += '<br /><span class="rlabel">positionName:</span>' + termj[i]['positionName']
					if termj[i]['role']: term += '<br /><span class="rlabel">role:</span>' + termj[i]['role']
			elif key == 'dataset-reference-date':
				term = ''
				for i in range(len(termj)):
					term += '<span class="rlabel">' + termj[i]['type'] + ':</span> ' + termj[i]['value'] + '<br/>'
			elif key == 'scales':
				term = ''
				for i in range(len(termj)):
					term += '1 : ' + str(termj[i]) + '<br/>'
			elif key == 'descriptive-keywords':
				term = ''
				for i in range(len(termj)):
					term += termj[i]['thesaurus']['title'] + '<ul>'
					for j in range(len(termj[i]['keywords'])):
						term += '<li>'
						if termj[i]['keywords'][j]['uri']:
							term += '<a href="' + termj[i]['keywords'][j]['uri'] + '" target="_blank">' + termj[i]['keywords'][j]['label'] + '</a>'
						else:
							term += termj[i]['keywords'][j]['label']
						term += '</li>'
					term += '</ul>'
			else:
				term = ''
				if type(termj).__name__ == 'list' :
					for i in range(len(termj)):
						if type(termj[i]).__name__ == 'dict':
							for key in termj[i]:
								term += '<span class="rlabel">' + key + ':</span>' + termj[i][key] + '<br/>'
						else:
							term = termj[i]
				elif type(termj).__name__ == 'dict' :
					for key in termj:
						term += '<span class="rlabel">' + key + ':</span>' + termj[key] + '<br/>'
				else:
					term = json.dumps(termj, indent=3, separators=('\s ', ' : '))
					term = "<br />".join(term.split("\n"))

		except:
			# log.debug('Nelze JSON %s', term)
			if key == 'graphic-preview-file':
				if term[:4] == 'http':
					term = '<a href="' + term + '" target="_blank"><img src="' + term + '" alt="' + term + '"></a>'
			#elif dict.codes[key] != '':
				#term = dict
		# replace u00 chars
		p = re.compile(ur'\\u\d\d')
		m = re.search(p, term)
		if m:
			term = term.decode('unicode_escape')
		term = term.replace('"', '')
		term = term.replace('[<br />', '')
		term = term.replace('{<br />', '')
		term = term.replace(']<br />', '')
		term = term.replace('}<br />', '')
		term = term.replace('<br />], ', ',')
		if term.endswith(']'):
			term = term[:-1]
		if term.endswith('}'):
			term = term[:-1]
		if term.startswith('['):
			term = term[1:]
		#log.debug('Vracim %s', term)
	return term


def bettercategories(catname):
	'''Capitalized first letter and undercores and dashes replaced with space'''
	catname = catname.replace('-', ' ')
	catname = catname.replace('_', ' ')
	catname = catname.capitalize()
	return catname


class InspireThemePlugin(plugins.SingletonPlugin):
	'''An Inspire metadata theme plugin.

	'''
	# Declare that this class implements IConfigurer.
	plugins.implements(plugins.IConfigurer)

	# Declare that this plugin will implement ITemplateHelpers.
	plugins.implements(plugins.ITemplateHelpers)
	
	# Declare that this plugin will implement IRoutes.
	plugins.implements(plugins.IRoutes, inherit=True)

	def update_config(self, config):

		# Add this plugin's templates dir to CKAN's extra_template_paths, so
		# that CKAN will use this plugin's custom templates.
		# 'templates' is the path to the templates dir, relative to this
		# plugin.py file.
		toolkit.add_template_directory(config, 'templates')

	def get_helpers(self):
		'''Register the functions above as a template
		helper functions.

		'''
		# Template helper function names should begin with the name of the
		# extension they belong to, to avoid clashing with functions from
		# other extensions.
		return {'inspire_theme_humanreadable': humanreadable, 'inspire_theme_bettercategories': bettercategories, 'inspire_theme_list2dict': list2dict, 'inspire_theme_getdict': dict, 'inspire_theme_toobj': toobj}

	def before_map(self, route_map):
		controller = "ckanext.inspire_theme.controller:InspireThemeController"
		route_map.connect("/dataset/{id}.rdfi", controller=controller, action="show")
		return route_map