# coding: utf8

# Copyright 2017 Vincent Jacques <vincent@vincent-jacques.net>

"""
A `Sphinx <http://www.sphinx-doc.org>`_ extension providing an `OCaml`
`domain <http://www.sphinx-doc.org/en/stable/domains.html>`_
and `autodocumenters <>`_ for `OCaml` elements.
"""

from . import domain
from . import autodocumenters


def setup(app):
    app.add_domain(domain.OCamlDomain)
    app.add_autodocumenter(autodocumenters.ModuleDocumenter)
