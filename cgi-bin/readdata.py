#!/usr/bin/python

infile='GDS3420'
#Creates an object with the name of the file to be opened and read

fh = open(infile)
#Creates an object which is the opened file with all its content

line= fh.readline()
'''The readline method reads a single line of the file, which will useful to be used to obtain the data from the table line by line.'''

while line[:20] != '!dataset_table_begin':
    line=fh.readline()

'''This is the loop which will allow us to read the data in raw table included in the file.
The statement is that "while" the first 20 characters of the line read (remember we are reading each line of the 
file individually with readline()), are different to '!dataset_table_begin' (which is stated with the exclamation 
simbol '!' before the equal symbol), then read that line. This loop allow the script not to start reading the file until the 
dataset table begins, which is just in the line after the '!dataset_table_begin' line.'''
 

header= fh.readline().strip()
'''Creates an object which is each line read (readline()) and whitespaces are removed from the beginning and the end of the line (=string).
This will be used to read the first line of the table, which contains the titles for our columns (gene title, gene symbol...).'''

colnames={}
#Creates an empty dictionary.

index=0
for title in header.split('\t'):
    colnames[title]=index
    print '%s\t%s'%(title,index)
    index=index+1
#Each element (title) in the header line is linked with an 'indez number', appended with it to the colname dictionary created, and printed in the screen. 


#open our output files, one per table.
genefile=open('genes.txt', 'w')
expressionfile=open('expression.txt','w')
probefile=open('probes.txt', 'w')



genefields=['Gene ID', 'Gene title', 'Gene symbol']
samples=header.split('\t')[2:int(colnames['Gene title'])]
probefields=['ID_REF','Gene ID']
'''A list for column headers for Gene and Probe files. As they are common for all the GEO files, they can be introduced manually.
A list of the samples is also created, splitting the header as we did before, and using the 'splitted' outputs obtained from 'index=2' 
until colname='Gene title', excluding this last one. We can know this thanks to the dictionary created and printed before!.'''


def buildrow(row, fields):
    newrow=[]
    for f in fields:
        newrow.append(row[int(colnames[f])])
    return "\t".join(newrow)+"\n"


def build_expression(row, samples):
    exprrows=[]
    for s in samples:
        newrow=[s,]
	newrow.append(row[int(colnames['ID_REF'])])
	newrow.append(row[int(colnames[s])])
	exprrows.append("\t".join(newrow))
    return "\n".join(exprrows)+"\n"

'''This two methods define how each part of the line should be read and written in each file. The first one takes the 'name' in each line corresponding
to each column name (colname) previously defined and puts those in a list, which will be printed in order in the files. The second defines how to take the 
expression value in a similar way than the other method, takes the expression value for each column, but, in this case, the values are taken according to their
corresponding sample name. In both methods, the names/values are appended separated in columns and rows (table structure, and it is in this way how
they will we written in the files. '''

rows=0    
for line in fh.readlines():
    try:
        if line[0]=='!':
            continue
        row=line.strip().split('\t')
        genefile.write(buildrow(row, genefields))
        probefile.write(buildrow(row,probefields))
        expressionfile.write(build_expression(row, samples))	
	rows=rows+1
    except:
	pass

'''This loop defines that if the line does not start with !, then should be stripped and splitted and written in the way defined by the 
previous defined methods. Note that gene and probe files, the method will only take the 'names' for the corresponding columns, as they are
defined in 'genefields' and 'probefields' lists.'''

genefile.close()
probefile.close()
expressionfile.close()

#Closes the files with all the information written in them.

print '%s rows processed'%rows

#Prints the number of rows processed.

