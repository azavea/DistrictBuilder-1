#!/bin/bash

# Generate the HTML and class UML diagrams
epydoc --config=epydoc.config

# Generate the DOT code for graphviz. This will prompt for a password
postgresql_autodoc -d publicmapping -h localhost -p 5432 -u publicmapping --password -s publicmapping -m "publicmapping_" -t dot

# Generate a graphic from the dot file.
dot -Tpng publicmapping.dot -o schema.png

rm publicmapping.dot
cp schema.png html/schema.png
