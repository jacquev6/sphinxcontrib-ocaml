# coding: utf8

# Copyright 2017 Vincent Jacques <vincent@vincent-jacques.net>

import json
import os.path
import subprocess

import sphinx.ext.autodoc

from . import autoocamldoc


class ModuleDocumenter(sphinx.ext.autodoc.Documenter):
    objtype = "ocamlmodule"

    def generate(self, more_content=None, real_modname=None, check_module=False, all_members=False):
        if self.env.config.ocaml_source_directories is None:
            # @todo Use Sphinx's warnings and errors infrastructure
            print("ERROR: please set ocaml_source_directories in conf.py")
            exit(1)

        module_name = self.directive.arguments[0]
        for d in self.env.config.ocaml_source_directories:
            interface_file_name = "{}/{}.mli".format(d, module_name)
            if os.path.isfile(interface_file_name):
                break
        else:
            # @todo Use Sphinx's warnings and errors infrastructure
            print("ERROR: {}.mli not found in any ocaml_source_directories".format(module_name))
            exit(1)

        contents = json.loads(subprocess.run(
            [self.env.config.ocaml_autoocamldoc_executable, interface_file_name],
            stdout=subprocess.PIPE,
            check=True,
            universal_newlines=True,
        ).stdout)

        generator = autoocamldoc.Generator(contents)
        for line in generator():
            self.add_line(line, "a")  # @todo Set file and line number (for error messages)
