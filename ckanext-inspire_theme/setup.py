from setuptools import setup, find_packages
import sys, os

version = '0.2'

setup(
    name='ckanext-inspire_theme',
    version=version,
    description="Inspire metadata theme and export",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Stepan Kafka, Marek Splichal',
    author_email='kafka@email.cz, marek.splichal@gmail.com',
    url='http://www.ccss.cz',
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
