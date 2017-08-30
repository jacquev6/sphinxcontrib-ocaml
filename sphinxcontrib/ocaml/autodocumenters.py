# coding: utf8

# Copyright 2017 Vincent Jacques <vincent@vincent-jacques.net>

import json
import subprocess

import sphinx.ext.autodoc

from . import autoocamldoc


class ModuleDocumenter(sphinx.ext.autodoc.Documenter):
    objtype = "ocamlmodule"

    def generate(self, more_content=None, real_modname=None, check_module=False, all_members=False):
        contents = json.loads(subprocess.run(
            # @todo Remove hard-coded paths
            ["autoocamldoc/_build/autoocamldoc.byte", "test/src/ocaml/{}.mli".format(self.directive.arguments[0])],
            stdout=subprocess.PIPE,
            check=True,
            universal_newlines=True,
        ).stdout)
        generator = autoocamldoc.Generator(contents)
        for line in generator():
            self.add_line(line, "a")  # @todo Set file and line number (for error messages)
