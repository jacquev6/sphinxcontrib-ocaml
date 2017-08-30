# coding: utf8

# Copyright 2017 Vincent Jacques <vincent@vincent-jacques.net>

import sphinx.ext.autodoc


class ModuleDocumenter(sphinx.ext.autodoc.Documenter):
    objtype = "ocamlmodule"

    def generate(self, more_content=None, real_modname=None, check_module=False, all_members=False):
        self.add_line("Yup", "a")
