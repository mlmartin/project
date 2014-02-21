'''Clases for gene representation from the MySQL database'''

import MySQLdb

class DBHandler():
	'''This class will allow us to connect to our database without having to request accession every single time'''
	
	connection=None
	dbname='mlmartin'
	dbuser='mlmartin'
	dbpassword='eWC3c8tn'
	
	def __init__(self):
		'''This method defines how we will connect to our database with the username and password provided in the DBHandler class'''

		if DBHandler.connection == None:
			DBHandler.connection = MySQLdb.connect(db=DBHandler.dbname, user=DBHandler.dbuser, passwd=DBHandler.dbpassword)

	def cursor (self):
		'''This method makes the connection'''

		return DBHandler.connection.cursor()

class Gene():
	'''Includes all the methods to get expression values from a given genid from the Gene table'''
	geneid=''
	genetitle=''
	genesymbol=''
	probelist=[]
	samplelist=[]
	expressionlist=[]
	probeaverage=''

	def __init__(self,geneid):
		'''Returns the gene symbol, gene title and a list of the probes related to a slected gene ID.
		Example: gene=classes.Gene('geneid')'''

		self.geneid=geneid
		db=DBHandler()
		cursor=db.cursor()
		'''Defines cursor as the execution of commands in our database'''

		sql='select genetitle, genesymbol from Gene where geneid=%s'
		cursor.execute(sql,(geneid,))
		result=cursor.fetchone()
		
		self.genetitle=result[0]
		self.genesymbol=result[1]

		probesql='select probename from Probe where geneid=%s'
		cursor.execute(probesql, (geneid,))

		probes=cursor.fetchall()
		
		for probe in probes:
			self.probelist.append(probe[0])
		'''Append adds a new item at the end of the probelist'''
		
		print(self.geneid)		
		print(self.genetitle)
		print(self.genesymbol)
		print(self.probelist)
		
	
	
	def probesexp (self,probename):
		'''Returns a list of the samples and their related expressions for the selected probe from the list of probes from the geneid selected.
		Example: gene.probesexp('probename')'''	
		
		db=DBHandler()
		cursor=db.cursor()
		
		sql='select samplename from Expression where probename=%s'
		cursor.execute(sql, (probename,))

		samples=cursor.fetchall()

		for sample in samples:
			self.samplelist.append(sample[0])
				

		expressionsql='select expressionvalue from Expression where probename=%s'
		cursor.execute(expressionsql, (probename,))
		expressions=cursor.fetchall()
		
		
		for expression in expressions:
			self.expressionlist.append(expression[0])
		
		
		averagesql='select sum(expressionvalue)/count(expressionvalue) as average from Expression where probename=%s'
		cursor.execute(averagesql, (probename,))
		average=cursor.fetchone()
		
		self.probeaverage=average[0]
		 		

		print('Sample list:') 
		print(self.samplelist)
		print('Expressions list:')
		print(self.expressionlist)
		print('Average expression of the selected probe')
		print(self.probeaverage)
		


	def averageexpression(self):
		'''Returns the average expression values of the given gene grouped in both conditions: 4 h and 24h.
		Example: gene.averageexpression()'''
		
		db=DBHandler()
		cursor=db.cursor()
		averagelist=[]
		geneid=self.geneid
		
		sql='select sum(expressionvalue)/count(expressionvalue) as Average from Expression e inner join Probe p on e.probename=p.probename inner join Gene g on g.geneid=p.geneid inner join Sample s on s.samplename=e.samplename where g.geneid=%s group by time'
		
		cursor.execute(sql, (geneid,))
		averageexpressions=cursor.fetchall()

		for averageexpression in averageexpressions:
			averagelist.append(averageexpression[0])

		print('4 hours average expression for' + self.geneid + ':')
		print(averagelist[0])
		print('24 hours average expression for' + self.geneid + ':')
		print(averagelist[1])



class Expressed():
	'''Includes all the methods to get the top 10 genes most expressed at a given time
	Example: time=classes.Expressed('time','n_req')
	Example with numbers: time=classes.Expressed('4','10')'''

	time=''
	probelist=[]
	genelist=[]
	expressionlist=[]
	

	geneid=''
	genesymbol=''
	genetitle=''

	def __init__(self,time):
		self.time=time
		db=DBHandler()
		cursor=db.cursor()
		

		sql='select sum(expressionvalue)/count(expressionvalue) as average, probename from Expression p inner join Sample s on p.samplename=s.samplename where time=%s group by probename order by average desc'
		cursor.execute(sql, (time,))
		probes=cursor.fetchmany(10)
		
		for probe in probes:
			self.probelist.append(probe[1])
			self.expressionlist.append(probe[0])
		
		print(self.probelist)
		print(self.expressionlist)
	
	def getgenes(self):
		db=DBHandler()
                cursor=db.cursor()
		genesql='select g.geneid from Gene g inner join Probe p on p.geneid=g.geneid where probename=%s'

		for p in self.probelist:
			cursor.execute(genesql, (p,))
			gene=cursor.fetchone()
			print(gene, p)
						
		
		
						
		print('Top genes being expressed:')
		print(self.genelist)
	
	def genedetails(self, geneid):
		self.geneid=geneid
		
		db=DBHandler()
		cursor=db.cursor()

		sql='select genesymbol, genetitle from Gene where geneid=%s'
		cursor.execute(sql, (geneid,))
		results=cursor.fetchone()
		
		self.genesymbol=results[0]
		self.genetitle=results[1]
		
		print('GeneID:' + self.geneid)
		print('Gene Symbol:' + self.genesymbol)
		print('Gene Title:' + self.genetitle)
			
			


class Average():
	'''Includes all the methods necessaries to get the average expression of all the expressed genes at a given time
	Example: time=classes.Time('time')'''

	time=''
	averageexpression=''

	def __init__(self,time):
		self.time=time
		db=DBHandler()
		cursor=db.cursor()

		sql='select sum(expressionvalue)/count(expressionvalue) from Expression e inner join Sample s on s.samplename=e.samplename where time=%s'
		cursor.execute(sql,(time,))
		results=cursor.fetchone()


		self.averageexpression=results[0]


		print('Time selected:')
		print(self.time)
		print('Average Expression:')
		print(self.averageexpression)	
	
	
	def onlyexpressed(self):
		'''Returns the average expression ONLY of the expressed genes (expression value > 0) for the given time
		Example: time.onlyexpressed()'''
		
		
		db=DBHandler()
		cursor=db.cursor()
		
		expressedaverage=''
		
		sql='select sum(expressionvalue)/count(expressionvalue) from Expression e inner join Sample s on e.samplename=s.samplename where time=%s and expressionvalue>0'
		cursor.execute(sql,(self.time,))
		result=cursor.fetchone()
		
		expressedaverage=result[0]
		
		print('Time selected:')
		print(self.time)
		print('Average expression of expressed genes:')
		print(expressedaverage)

