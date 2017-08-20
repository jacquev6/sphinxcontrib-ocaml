#!/bin/bash

set -o errexit

cd autoocamldoc
ocamlbuild -use-ocamlfind -no-links -package bisect_ppx autoocamldoc.byte
cd ..

rm -f bisect????.out
coverage3 erase
for f in tests/*.mli
do
    autoocamldoc/_build/autoocamldoc.byte $f >${f%.mli}.json
    coverage3 run --branch --append sphinxcontrib/ocaml/autoocamldoc.py <${f%.mli}.json >${f%.mli}.rst
done
bisect-summary bisect????.out
echo
bisect-ppx-report -I autoocamldoc -html autoocamldoc/_build/bisect bisect????.out
echo "See coverage report (for autoocamldoc.ml) in $(pwd)/autoocamldoc/_build/bisect/index.html"
echo
coverage3 report
echo
coverage3 html --directory build/coverage
echo "See coverage report (for autoocamldoc.py) in $(pwd)/build/coverage/index.html"
echo
rm -f bisect????.out
coverage3 erase

pep8 --max-line-length=120 sphinxcontrib *.py doc/conf.py

# Install and use to build doc

./setup.py --quiet install --user
opam pin --yes --no-action add .
opam reinstall --yes sphinx-ocaml

rm -rf docs build/sphinx
./setup.py build_sphinx
cp -r build/sphinx/html docs
touch docs/.nojekyll
rm -f docs/.buildinfo
echo
echo "See documentation in $(pwd)/docs/index.html"
echo

echo
echo "Development cycle OK"
