==============
All references
==============

This demonstrates all kinds of references to OCaml elements.

.. default-domain:: ocaml

Top-level elements
------------------

.. type:: top_level_type

.. val:: top_level_value

.. exception:: TopLevelException

.. module_type:: TopLevelModuleType

.. module:: TopLevelModule

Type: :typ:`top_level_type`, value: :val:`top_level_value`, exception: :exn:`TopLevelException`, module type: :modtyp:`TopLevelModuleType` and module: :mod:`TopLevelModule`.

Elements within module, module type and functor parameter
---------------------------------------------------------

.. module:: Container

    .. type:: t

    .. val:: v

    .. exception:: e

    .. module_type:: MT

    .. module:: M

Type: :typ:`Container.t`, value: :val:`Container.v`, exception: :exn:`Container.e`, module type: :modtyp:`Container.MT` and module: :mod:`Container.M`.

.. module_type:: Container

    .. type:: t

    .. val:: v

    .. exception:: e

    .. module_type:: MT

    .. module:: M

Type: :typ:`Container:t`, value: :val:`Container:v`, exception: :exn:`Container:e`, module type: :modtyp:`Container:MT` and module: :mod:`Container:M`.

.. module:: Functor

    .. functor_parameter:: Container

        .. type:: t

        .. val:: v

        .. exception:: e

        .. module_type:: MT

        .. module:: M

Type: :typ:`Functor.Container!t`, value: :val:`Functor.Container!v`, exception: :exn:`Functor.Container!e`, module type: :modtyp:`Functor.Container!MT` and module: :mod:`Functor.Container!M`.

Elements with same name
-----------------------

.. module:: SameName

    .. type:: x

    .. val:: x

    .. exception:: x

    .. module_type:: x

    .. module:: x

Type: :typ:`SameName.x`, value: :val:`SameName.x`, exception: :exn:`SameName.x`, module type: :modtyp:`SameName.x` and module: :mod:`SameName.x`.
