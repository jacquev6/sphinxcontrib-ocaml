#!/bin/bash

# Copyright 2017 Vincent Jacques <vincent@vincent-jacques.net>

set -o errexit

# Install dependencies

eval `opam config env`
opam install --yes bisect_ppx bisect-summary General yojson
clear

# Build

cd autoocamldoc
ocamlbuild -use-ocamlfind -no-links -package bisect_ppx autoocamldoc.byte
cd ..

# Test

rm -f bisect????.out
coverage3 erase

rm -rf test/output build/test_doctrees
coverage3 run --branch --include "sphinxcontrib/*" $(which sphinx-build) test/input test/output -d build/test_doctrees
echo
echo "See test documentation in $(pwd)/test/output/index.html"
echo

bisect-summary bisect????.out
echo
coverage3 report
echo
bisect-ppx-report -I autoocamldoc -html autoocamldoc/_build/bisect bisect????.out
coverage3 html --directory build/coverage
echo "See coverage reports in $(pwd)/autoocamldoc/_build/bisect/index.html"
echo "and $(pwd)/build/coverage/index.html"
echo

rm -f bisect????.out
coverage3 erase

# Check

pep8 --max-line-length=120 sphinxcontrib *.py doc/conf.py

# Install and use to build doc

./setup.py --quiet install --user
opam pin --yes --no-action add .
opam reinstall --yes sphinxcontrib-ocaml

rm -rf docs build/sphinx
./setup.py build_sphinx
cp -r build/sphinx/html docs
rm -f docs/.buildinfo
echo
echo "See documentation in $(pwd)/docs/index.html"
echo

echo
echo "Development cycle OK"
