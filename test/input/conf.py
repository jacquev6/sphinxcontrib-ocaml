# coding: utf8

# Copyright 2017 Vincent Jacques <vincent@vincent-jacques.net>

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

# https://github.com/jacquev6/sphinx-ocaml
extensions.append("sphinxcontrib.ocaml")
