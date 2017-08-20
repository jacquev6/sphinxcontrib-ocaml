# coding: utf8

# Copyright 2017 Vincent Jacques <vincent@vincent-jacques.net>


master_doc = "index"
project = "sphinx-ocaml"
author = '<a href="http://vincent-jacques.net/">Vincent Jacques</a>'
copyright = ('2013-2017 {} <script>var jacquev6_ribbon_github="{}"</script>'.format(author, project) +
             '<script src="https://jacquev6.github.io/ribbon.js"></script>')
extensions = []


nitpicky = True
# See https://github.com/simpeg/discretize/commit/e1a9cf2352edef9ebf0fdde8a6886db58bf4e90f
nitpick_ignore = [
    ('py:obj', 'list'),
]

# https://github.com/bitprophet/alabaster
# html_theme_path
extensions.append("alabaster")
html_theme = "alabaster"
html_sidebars = {
    "**": ["about.html", "navigation.html", "searchbox.html"],
}
html_theme_options = {
    "github_user": "jacquev6",
    "github_repo": project,
    "travis_button": True,
}
# html_logo = "logo.png"

# https://github.com/jacquev6/sphinx-ocaml
extensions.append("sphinxcontrib.ocaml")
