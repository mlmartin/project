#!/usr/local/bin/python

import cgi

import classes

form=cgi.FieldStorage()

form['topgenes']

time=classes.Expressed(form['topgenes'])

print'Content-Type: text/html'
print
print '<link rel="stylesheet" type="text7css" href="styles.css">'
print '<body style='background-color:black'>'
print '<div id='wrapper'>'
print '<div id='header'><a href='main_page.html'><h1>Mario Bioinformatics Project</h1></a></div>'
print '<div id='content'><form id=geneform name=geneform method=POST action=cgi-bin/query.py>'
print 'Introduce GeneID: <input type=text size=20 name='geneid'/><input type=submit name=submit value='Submit!'/></form></div>'
print '<div id='footer'>Mario's Practical Project. Powered by lots of Monster and Redbull cans and a few hours of despair</div>'
print '</body></html>'

