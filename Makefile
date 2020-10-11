.PHONY: deps build clean test lint install ci

# echo is slienced with @
# https://www.gnu.org/software/make/manual/make.html#Echoing

deps:
	opam exec -- opam install --yes bisect_ppx bisect-summary General yojson

build:
	# https://github.com/aantron/bisect_ppx/blob/master/doc/advanced.md#Dune suggests
	# modifying the dune file for release. Let's modify it for tests instead.
	sed -i "s/^;\(.*bisect_ppx.*\)$$/\1/" ocaml_autodoc/dune
	dune build ocaml_autodoc/ocaml_autodoc.exe
	sed -i "s/^\(.*bisect_ppx.*\)$$/;\1/" ocaml_autodoc/dune

clean:
	rm -f bisect????.out
	rm -rf test/output build/test_doctrees
	rm -rf docs build/sphinx
	coverage3 erase

test: clean
	coverage3 run --branch --include "sphinxcontrib/*" $$(which sphinx-build) test/input test/output -d build/test_doctrees
	@echo
	@echo "See test documentation in $$(pwd)/test/output/index.html"
	@echo

	bisect-summary bisect????.out
	@echo
	coverage3 report
	@echo
	bisect-ppx-report -I ocaml_autodoc -html ocaml_autodoc/_build/bisect bisect????.out
	coverage3 html --directory build/coverage
	@echo "See coverage reports in $$(pwd)/ocaml_autodoc/_build/bisect/index.html"
	@echo "and $$(pwd)/build/coverage/index.html"
	@echo

lint:
	pycodestyle --max-line-length=120 sphinxcontrib *.py doc/conf.py

install:
	./setup.py install --user
	opam pin --yes --no-action add --kind=path .
	opam reinstall --yes sphinxcontrib-ocaml

	./setup.py build_sphinx
	cp -r build/sphinx/html docs
	@echo
	@echo "See documentation in $$(pwd)/docs/index.html"

ci: clean deps lint build test install
