from setuptools import setup, find_packages
import sys, os

version = '0.4'

setup(
    name='ckanext-inspire_harvester',
    version=version,
    description="CKAN harvester INSPIRE metadata.",
    long_description="""\
    """,
    classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Marek Splichal, Stepan Kafka',
    author_email='marek.splichal@gmail.com, kafka@email.cz',
    url='www.ccss.cz',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.inspireh'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[  # -*- Extra requirements: -*-
    ],
    entry_points= \
        """
        [ckan.plugins]
        inspire_harvester=ckanext.inspireh.harvesters:InspireHarvester
    """,
)
