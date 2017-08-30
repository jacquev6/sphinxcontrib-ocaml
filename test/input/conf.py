# coding: utf8

# Copyright 2017 Vincent Jacques <vincent@vincent-jacques.net>

import os.path
import sys
import subprocess


project = "Test project for sphinx-ocaml"
author = '<a href="http://vincent-jacques.net/">Vincent Jacques</a>'
copyright = '2017 {}'.format(author)

nitpicky = True
master_doc = "index"
extensions = []

# https://github.com/bitprophet/alabaster
html_sidebars = {
    "**": ["about.html", "navigation.html", "searchbox.html"],
}

# Development version
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "sphinxcontrib")))
extensions.append("ocaml")
ocaml_autoocamldoc_executable = "autoocamldoc/_build/autoocamldoc.byte"
ocaml_source_directories = ["test/src/ocaml"]
ocaml_findlib_packages = ["General"]
