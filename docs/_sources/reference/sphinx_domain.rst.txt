===================
OCaml Sphinx domain
===================

.. default-domain:: ocaml

.. highlight:: rst

Remember that these directives and roles are in a Sphinx `domain <http://www.sphinx-doc.org/en/stable/domains.html>`_,
so you can either prefix them with ``ocaml:`` or set the default domain to ``"ocaml"``, either with the ``default-domain`` directive::

    .. default-domain:: ocaml

or in the ``conf.py`` file:

.. code-block:: python

    default_domain = "ocaml"

Examples below assume the default domain is set.

Directives
==========

Values and types
----------------

.. rst:directive:: .. val:: name

    Document a value::

        .. val:: v

            Some doc for *v*.

    is rendered as:

        .. val:: v
            :noindex:

            Some doc for *v*.

    The value's type can be documented using the ``:type:`` option::

        .. val:: coords
            :type: (int * int) list

            The coordinates.

    ..

        .. val:: coords
            :noindex:
            :type: (int * int) list

            The coordinates.

.. rst:directive:: .. type:: name

    Document a type::

        .. type:: t

            Some doc for *t*.

    ..

        .. type:: t
            :noindex:

            Some doc for *t*.

    The type's parameters can be documented using the ``:parameters:`` option::

        .. type:: t3
            :parameters: ('a, 'b, 'c)

            *t3* has three parameters.

    ..

        .. type:: t3
            :noindex:
            :parameters: ('a, 'b, 'c)

            *t3* has three parameters.

    The type's manifest (*i.e.* if it is an alias for some other type) can be documented using the ``:manifest:`` option::

        .. type:: int_list
            :manifest: int list

            A list of integers.

    ..

        .. type:: int_list
            :noindex:
            :manifest: int list

            A list of integers.

    The type's kind (*i.e.* its constructors and record labels) can be documented using the ``:kind:`` option
    and the ``:constructor:`` and ``:label:`` doc fields::

        .. type:: variant
            :kind: A | B of int

            A variant type.

            :constructor A: a

            :constructor B: b

    ..

        .. type:: variant
            :kind: A | B of int

            A variant type.

            :constructor A: a

            :constructor B: b

    ::

        .. type:: record
            :kind: {a: int; b: float}

            A record type.

            :label a: a

            :label b: b

    ..

        .. type:: record
            :noindex:
            :kind: {a: int; b: float}

            A record type.

            :label a: a

            :label b: b

    The type can be marked as `private <https://caml.inria.fr/pub/docs/manual-ocaml-4.05/extn.html#sec220>`_ using the ``:private:`` flag::

        .. type:: int_list_p
            :private:
            :manifest: int list

            A list of integers.

    ..

        .. type:: int_list_p
            :noindex:
            :private:
            :manifest: int list

            A list of integers.

.. rst:directive:: .. exception:: name

    Document an exception::

        .. exception:: MyException

            Some doc for *MyException*.

    ..

        .. exception:: MyException
            :noindex:

            Some doc for *MyException*.

    The exception's payload can be documented using the ``:payload:`` option.
    The ``:label:`` doc field is used like for a type::

        .. exception:: TupleException
            :payload: int * float

            With a tuple payload.

    ..

        .. exception:: TupleException
            :noindex:
            :payload: int * float

            With a tuple payload.

    ::

        .. exception:: RecordException
            :payload: {a: int; b: float}

            With a record payload.

            :label a: a

            :label b: b

    ..

        .. exception:: RecordException
            :noindex:
            :payload: {a: int; b: float}

            With a record payload.

            :label a: a

            :label b: b

Modules and module types
------------------------

.. rst:directive:: .. module:: Name

    Document a module::

        .. module:: MyModule

            Some documentation for *MyModule*.

            .. type:: t

    ..

        .. module:: MyModule
            :noindex:

            Some documentation for *MyModule*.

            .. type:: t

    The module can be documented as an `alias <https://caml.inria.fr/pub/docs/manual-ocaml-4.05/extn.html#sec235>`_ using the ``:alias_of:`` option.
    There should be no contents in that case::

        .. module:: MyAlias
            :alias_of: Original

            Some documentation for *MyAlias*.

    ..

        .. module:: MyAlias
            :noindex:
            :alias_of: Original

            Some documentation for *MyAlias*.

    If the module get its contents from something else (*e.g* a module type, a functor application, *etc.*),
    this can be documented using the ``:contents_from:`` option::

        .. module:: Contents
            :contents_from: SomeModuleType

            .. type:: t

    ..

        .. module:: Contents
            :noindex:
            :contents_from: SomeModuleType

            .. type:: t

.. rst:directive:: .. module_type:: Name

    Document a module type::

        .. module_type:: MyModuleType

            Some documentation for *MyModuleType*.

            .. type:: t

    ..

        .. module_type:: MyModuleType
            :noindex:

            Some documentation for *MyModuleType*.

            .. type:: t

    @todo contents_from

Functors
--------

.. rst:directive:: .. functor_parameter:: Name

    Document a functor parameter::

        .. module:: Functor

            .. functor_parameter:: Parameter

                .. val:: n
                    :type: int

            .. val:: m
                :type: int

    ..

        .. module:: Functor
            :noindex:

            .. functor_parameter:: Parameter

                .. val:: n
                    :noindex:
                    :type: int

            .. val:: m
                :noindex:
                :type: int

    @todo contents_from

Roles
=====

.. rst:role:: val

    @todo

.. rst:role:: typ

    @todo

.. rst:role:: exn

    @todo

.. rst:role:: mod

    @todo

.. rst:role:: modtyp

    @todo
