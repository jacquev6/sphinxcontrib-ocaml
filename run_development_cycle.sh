#!/bin/bash

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
bisect-ppx-report -I autoocamldoc -html _build/bisect bisect????.out
echo "See coverage report (for autoocamldoc.ml) in $(pwd)/_build/bisect/index.html"
echo
coverage3 report
echo
coverage3 html --directory _build/coverage
echo "See coverage report (for autoocamldoc.py) in $(pwd)/_build/coverage/index.html"
rm -f bisect????.out
coverage3 erase
