from . import domain

def setup(app):
    app.add_domain(domain.OCamlDomain)
