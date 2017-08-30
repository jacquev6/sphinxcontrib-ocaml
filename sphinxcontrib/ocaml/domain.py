# coding: utf8

# Copyright 2017 Vincent Jacques <vincent@vincent-jacques.net>

import itertools
import json

import docutils
import sphinx

from sphinx.addnodes import desc, desc_content


def desc_annotation(s):
    return sphinx.addnodes.desc_annotation(s, s)


def desc_name(s):
    return sphinx.addnodes.desc_name(s, s)


def desc_signature():
    return sphinx.addnodes.desc_signature("", "")


def identity(x):
    return x


class Directive(docutils.parsers.rst.Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    doc_field_types = []

    def current_module_prefix(self):
        return self.env.domaindata[OCamlDomain.name]["module_stack"][-1]

    def get_index_entry(self):
        container_name = self.current_module_prefix()[:-1]
        if container_name == "":
            container = ""
        else:
            container_kind = {
                ".": "",
                ":": "module type ",
                "$": "functor parameter ",
            }[self.current_module_prefix()[-1]]
            container = " in {}{}".format(container_kind, container_name)
        return "{} ({}{})".format(self.get_header_name(), self.object_type.replace("_", " "), container)

    def append_if_not_none(self, parent, make, child):
        if child is not None:
            parent.append(make(child))

    def run(self):
        self.env = self.state.document.settings.env

        should_index = "noindex" not in self.options

        header_node = self.make_header_node()

        index_node = sphinx.addnodes.index(entries=[])
        ident = self.get_id()
        if ident is not None:
            if ident in self.state.document.ids:
                # @todo Use Sphinx's warnings and errors infrastructure
                print("WARNING: Duplicate:", ident)
            header_node["first"] = False
            header_node["ids"].append(ident)
            self.state.document.note_explicit_target(header_node)

            if should_index:
                index_entry = self.get_index_entry()
                if index_entry is not None:
                    self.env.domaindata[OCamlDomain.name][self.role][ident.split()[-1]] = self.env.docname
                    index_node["entries"].append(("single", index_entry, ident, "", None))

        contents_node = desc_content()
        if self.contents_separator is not None:
            self.env.domaindata[OCamlDomain.name]["module_stack"].append(
                self.current_module_prefix() + self.arguments[0] + self.contents_separator
            )
        self.state.nested_parse(self.content, self.content_offset, contents_node)
        if self.contents_separator is not None:
            self.env.domaindata[OCamlDomain.name]["module_stack"].pop()
        # @todo Maybe labels and constructors should be directives instead of docfields?
        sphinx.util.docfields.DocFieldTransformer(self).transform_all(contents_node)

        footer_node = self.make_footer_node()

        main_node = desc()
        main_node["objtype"] = self.object_type
        self.append_if_not_none(main_node, identity, header_node)
        self.append_if_not_none(main_node, identity, contents_node)
        self.append_if_not_none(main_node, identity, footer_node)
        return [index_node, main_node]

    def make_header_node(self):
        header_node = desc_signature()
        self.append_if_not_none(header_node, desc_annotation, self.get_header_prefix())
        self.append_if_not_none(header_node, desc_name, self.get_header_name())
        self.append_if_not_none(header_node, desc_annotation, self.get_header_suffix())
        return header_node

    def make_footer_node(self):
        footer_node = desc_signature()
        self.append_if_not_none(footer_node, desc_annotation, self.get_footer())
        return footer_node


class Module(Directive):
    option_spec = {
        "noindex": docutils.parsers.rst.directives.flag,

        "contents_from": docutils.parsers.rst.directives.unchanged,
        "alias_of": docutils.parsers.rst.directives.unchanged,
    }

    object_type = "module"
    role = "mod"
    contents_separator = "."

    def get_id(self):
        return "mod {}{}".format(self.current_module_prefix(), self.arguments[0])

    def get_header_prefix(self):
        return "module "

    def get_header_name(self):
        return self.arguments[0]

    def get_header_suffix(self):
        alias_of = self.options.get("alias_of")
        if alias_of is None:
            contents_from = self.options.get("contents_from")
            if contents_from is None:
                contents_from = ""
            else:
                contents_from = "{} = ".format(contents_from)
            # @todo " : functor(A: ...)(B: ...) -> sig" when there are functor parameters in the content
            return " : {}sig".format(contents_from)
        else:
            return " = {}".format(alias_of)

    def get_footer(self):
        if self.options.get("alias_of") is None:
            return "end"
        else:
            return None


class ModuleType(Directive):
    option_spec = {
        "noindex": docutils.parsers.rst.directives.flag,

        "contents_from": docutils.parsers.rst.directives.unchanged,
    }

    object_type = "module_type"
    role = "modtyp"
    contents_separator = ":"

    def get_id(self):
        return "modtyp {}{}".format(self.current_module_prefix(), self.arguments[0])

    def get_header_prefix(self):
        return "module type "

    def get_header_name(self):
        return self.arguments[0]

    def get_header_suffix(self):
        contents_from = self.options.get("contents_from")
        if contents_from is None:
            contents_from = ""
        else:
            contents_from = "{} = ".format(contents_from)
        # @todo " = functor(A: ...)(B: ...) -> sig" when there are functor parameters in the content
        return " = {}sig".format(contents_from)

    def get_footer(self):
        return "end"


class FunctorParameter(Directive):
    option_spec = {
        "contents_from": docutils.parsers.rst.directives.unchanged,
    }

    object_type = "functor_parameter"
    contents_separator = "$"

    def get_id(self):
        return None

    def get_header_prefix(self):
        return "functor parameter "

    def get_header_name(self):
        return self.arguments[0]

    def get_header_suffix(self):
        contents_from = self.options.get("contents_from")
        if contents_from is None:
            contents_from = ""
        else:
            contents_from = "{} = ".format(contents_from)
        return " : {}sig".format(contents_from)

    def get_footer(self):
        return "end"


class Include(Directive):
    required_arguments = 0

    option_spec = {
        "contents_from": docutils.parsers.rst.directives.unchanged,
    }

    object_type = "incl"
    contents_separator = None

    def get_id(self):
        return "incl {}{}".format(
            self.current_module_prefix(),
            self.env.new_serialno("include {}".format(self.current_module_prefix())),
        )

    def get_index_entry(self):
        return None

    def get_header_prefix(self):
        return "include "

    def get_header_name(self):
        return self.options.get("contents_from")

    def get_header_suffix(self):
        if self.options.get("contents_from") is None:
            return "sig"
        else:
            return " = sig"

    def get_footer(self):
        return "end"


class Atom(Directive):
    contents_separator = None

    def handle_signature(self, sig, signode):
        self.__full_name = self.env.domaindata[OCamlDomain.name]["module_stack"][-1] + sig
        self.add_signature(sig, signode)
        return "{} {}".format(self.object_type, self.__full_name)

    def get_id(self):
        return "{} {}{}".format(self.role, self.current_module_prefix(), self.get_header_name())

    def get_header_prefix(self):
        return "{} ".format(self.object_type)

    def get_header_name(self):
        return self.arguments[0]

    def get_header_suffix(self):
        return None

    def make_footer_node(self):
        return None


class Value(Atom):
    role = "val"
    object_type = "val"

    option_spec = {
        "noindex": docutils.parsers.rst.directives.flag,

        "type": docutils.parsers.rst.directives.unchanged,
    }

    def get_header_suffix(self):
        type_ = self.options.get("type")
        if type_:
            return ": {}".format(type_)


class Type(Atom):
    role = "typ"
    object_type = "type"
    # @todo Add constructors and labels in indexes
    # @todo Parse type and display it as a multiline desc_signature if needed
    # (variant with several constructors or record with several labels)

    option_spec = {
        "noindex": docutils.parsers.rst.directives.flag,

        "parameters": docutils.parsers.rst.directives.unchanged,
        "private": docutils.parsers.rst.directives.flag,
        "manifest": docutils.parsers.rst.directives.unchanged,
        "kind": docutils.parsers.rst.directives.unchanged,
    }

    def get_header_prefix(self):
        parameters = self.options.get("parameters")
        if parameters:
            return "type {} ".format(parameters)
        else:
            return "type "

    def get_header_suffix(self):
        private = ""
        if "private" in self.options:
            private = "private "

        def suffix(key):
            value = self.options.get(key)
            if value:
                return " = {}{}".format(private, value)
            else:
                return ""

        suffix = "".join(suffix(key) for key in ["manifest", "kind"])

        if suffix == "":
            return None
        else:
            return suffix


class Exception(Atom):
    role = "exn"
    object_type = "exception"
    # @todo Add labels in indexes
    # @todo Parse payload and display it as a multiline desc_signature if needed (record with several labels)

    option_spec = {
        "noindex": docutils.parsers.rst.directives.flag,

        "payload": docutils.parsers.rst.directives.unchanged,
    }

    def get_header_suffix(self):
        payload = self.options.get("payload")
        if payload is not None:
            return " of {}".format(payload)


class XRefRole(sphinx.roles.XRefRole):
    def process_link(self, env, refnode, has_explicit_title, title, target):
        if not has_explicit_title:
            title = title.replace(":", ".").replace("$", ".").lstrip("~").lstrip(".")
            if target[0] == "~":
                target = target[1:]
                title = title.split(".")[-1]
        return (title, target)


class OCamlDomain(sphinx.domains.Domain):
    name = "ocaml"
    label = "OCaml"
    object_types = {
        Module.object_type: sphinx.domains.ObjType(Module.object_type, Module.role),
        ModuleType.object_type: sphinx.domains.ObjType(ModuleType.object_type, ModuleType.role),
        Value.object_type: sphinx.domains.ObjType(Value.object_type, Value.role),
        Type.object_type: sphinx.domains.ObjType(Type.object_type, Type.role),
        Exception.object_type: sphinx.domains.ObjType(Exception.object_type, Exception.role),
        # @todo Add an object type for functor parameters
    }
    directives = {
        Module.object_type: Module,
        ModuleType.object_type: ModuleType,
        Value.object_type: Value,
        Type.object_type: Type,
        Exception.object_type: Exception,

        Include.object_type: Include,
        FunctorParameter.object_type: FunctorParameter,
    }
    roles = {
        Module.role: XRefRole(),
        ModuleType.role: XRefRole(),
        # @todo Add a role for functor parameters
        Value.role: XRefRole(),
        Type.role: XRefRole(),
        Exception.role: XRefRole(),
    }
    initial_data = {
        "module_stack": [""],
        Module.role: {},
        ModuleType.role: {},
        Value.role: {},
        Type.role: {},
        Exception.role: {},
    }
    # @todo Add indexes for:
    # - modules (maybe specific indexes for structures and functors?)
    # - module types (maybe for signatures and functors?)
    # - values
    # - types
    # - exceptions
    # - constructors
    # - labels
    # - functor parameters

    def resolve_xref(self, env, fromdocname, builder, role, target, node, child):
        data = self.data[role]
        if any(target.startswith(prefix) for prefix in ".:$"):
            # If we ever have a performance issue here, we can build a index instead of enumerating
            matches = [(k, v) for (k, v) in data.items() if k.endswith(target)]
            best_matches = [(k, v) for (k, v) in matches if v == fromdocname]
            if len(best_matches) == 1:
                (target, todocname) = best_matches[0]
            elif len(matches) == 1:
                (target, todocname) = matches[0]
            else:
                todocname = None
                if matches:
                    # @todo Use Sphinx's warnings and errors infrastructure
                    print("ERROR: multiple matches for target '{}'".format(target))
        else:
            todocname = data.get(target)
        if todocname:
            targetid = "{} {}".format(role, target)
            return sphinx.util.nodes.make_refnode(builder, fromdocname, todocname, targetid, child)
        else:
            return None
