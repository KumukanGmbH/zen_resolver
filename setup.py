# -*- coding: utf-8 -*-
import os
from setuptools import setup

setup(
    name = "zen_resolver",
    version = "0.0.1",
    author = "Ross Crawford-d'Heureuse",
    author_email = "ross.crawford@kumukan.com",
    description = ("Script for closing zendesk tickets when we get pdfs"),
    license = "GPL",
    keywords = "",
    url = "https://github.com/KumukanGmbH/zen_resolver",
    install_requires = [
        'zdesk',  # must refer to package version explicitly **required**
        'requests',
        'pyOpenSSL',
    ]
)