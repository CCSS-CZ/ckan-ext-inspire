from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-inspire_theme',
    version=version,
    description="Inspire metadata theme",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Marek Splichal',
    author_email='marek.splichal@gmail.com',
    url='www.ccss.cz',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.inspire_theme'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        inspire_theme=ckanext.inspire_theme.plugin:InspireThemePlugin
    ''',
)
