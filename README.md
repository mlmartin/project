#Mario L. Martin README file for the Practical Project A in Bioinformatics

The present file contains a guide of the different files included in this Git repository
used in the Bioinformatics Project carried out by Mario L. Martin (Student ID: 130020616).



# Web files

4 files were used for the web design. 3 html for each web 'page',
and a css file for the web design and format.

main_page.html: includes the presentation of the webpage.

database.html: includes the forms to query the information about the data.

information.html: includes the information about the project and how query the information in the database page.	

styles.css: 	the style file, which defines the style and format of the html files.
		The characteristics of the elements of each webpage (header, main text, etc.), including position, color, structure are defined by this file.
 

#Data files

The GDS3420 file contains the raw dataset information, all the expression values, probenames, genes. 
The information is not properly organised and cannot be used to fill the MySQL tables.

The readdata.py file contains the python script needed for the data interpretation of the GDS3420 file. 
This script reads the file, takes the relevant data (geneid, gene symbol, gene title, probenames, sample names, expression values...) and writes the data in
separated .txt files in a organised structure (columns) suitable to fill the MySQL tables directly using these files.

The genes.txt, expression.txt and probes.txt are the files obtained with the readdata python script, containing the structured data.

The sample.txt file also contains organised data (the samplename, time corresponding to each sample and replica corresponding also to each sample. The only
difference between this file and the other is that the data in this file was written manually from the GEO website, as it could not be obtained from the raw 
data in the GDS3420 file.


#Python Scripts

Different python scripts were written to query the data to the MySQL database.

classes.py: 	This file includes the different classes and methods developed to query specific information to the MySQL database. The first class, DBHandler, creates
		a connection with the MySQL database, which is used to the rest of classes to acces the tables. The other classes uses python/sql languages to 
		request specific information (gene information, expression values, average expressions...) store that information in objects and lists to be
		then retrieved to the user.

query.py, query2.py, query3.py:	different python scripts used to link the classes.py with the html webpage. They take the input submited by the user
				and use the classes.py file to query the information to the MySQL databse, print the result back in a webpage.

 
