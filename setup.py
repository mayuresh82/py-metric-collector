#!/usr/bin/env python3

from setuptools import setup

version = '0.1.26'

setup(
    name= 'py-metric-collector',
    version= version,
    package_dir= {'': 'lib'},
    packages= ["metric_collector"],
    scripts= [
        'bin/metric-collector'
    ],
    license= 'Apache License, Version 2.0',
    description= 'Collect timeseries information from network devices',
    install_requires= [
        'cffi',
        'ncclient',
        'jxmlease',
        'pytest>=3.6',
        'pytest-cov',
        'jinja2',
        'pyyaml>=5.1',
        'junos-eznc',
        'ipaddress',
        'textfsm',
        'jmespath',
        'requests-mock',
        'requests',
    ],
    classifiers= [
       'Topic :: Utilities',
       'Environment :: Console',
       'Intended Audience :: Developers',
       'Intended Audience :: Information Technology',
       'Intended Audience :: System Administrators',
       'License :: OSI Approved :: Apache Software License',
       'Operating System :: OS Independent',
       'Programming Language :: Python',
    ],
    keywords= 'netconf junos juniper timeserie tsdb f5 bigip'
)