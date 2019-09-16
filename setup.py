# -- coding: utf-8 --
#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pathlib

from setuptools import setup


basedir = pathlib.Path(__file__).parent


setup(
    name="mox_stsorgsync",
    version=(basedir / "VERSION").read_text().strip(),
    author="Magenta ApS",
    author_email="info@magenta.dk",
    description=("mox agent for synchronizing stsorgsync from os2mo"),
    license="MPL",
    keywords="sts stsorgsync os2mo lora",
    url="",
    packages=["mox_stsorgsync", "os2sync_log_printer"],
    long_description=(basedir / "README.md").read_text().strip(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MPL License",
    ],
    install_requires=[
        # see requirements.txt
        # https://caremad.io/posts/2013/07/setup-vs-requirement/
    ],
)
