#!/usr/local/bin/python

import cgi
import classes

form=cgi.FieldStorage()

form['geneid']

gene=classes.Gene(form['geneid'])

print(gene)
