import re
import time
import sys


DATE_TIME_FORMAT = '%d %b %Y'
FIELD_TAG_PATTERN = 'PO %s    %s\n'
FIELD_ERROR = 'XXXXX'
PATTERN_ERROR = '== Error in line %d (%s,%s) =='

STORE_PI_ENABLE = 1
STORE_PI_DISABLE = 0


count_wo = 0


def makePPList(lstPP, count):
	'''
		 Funtio to organize the array according to the priority date

			   +-------------------> group(1): priority number  
			   |			+------> group(2): priority date 
			___|____	____|______
		 PI US152531	03 Jun 2011
			US222247	31 Aug 2011
	'''
	lstFormattedPP = []
	pattern = re.compile("([A-Za-z0-9]*)[ ]*(.*)")
	
	for pp in lstPP:
		ret = pattern.match(pp)
		
		datestring = ret.group(2)
		
		try:		
			dt = time.strptime(datestring,DATE_TIME_FORMAT)
			npp = ret.group(1)
			
			if (dt.tm_year > 1000):
				lstFormattedPP.append({dt: npp})
			else:
				print PATTERN_ERROR % (count, pp, datestring)
		except:
			print PATTERN_ERROR % (count, pp, datestring)

	lstFormattedPP.sort()
	
	return lstFormattedPP

	
	
	
def generateNewField(lstPP):
	'''
	Lista de entrada tem uma lista com dicionario interno separado por data=>texto
	'''
	global count_wo
	pattern = re.compile("^WO[A-Za-z0-9]*")
	
	pp = lstPP.pop(0)
	
	for dt,npp in pp.items():
		dtSel = dt
		ppSel = npp
		
	for pp in lstPP:
		for dt,npp in pp.items():
			if (dt != dtSel) :
				return FIELD_TAG_PATTERN % (ppSel,time.strftime(DATE_TIME_FORMAT,dtSel))
			else :
				ret = pattern.match(npp)
				if (ret != None) :
					count_wo = count_wo + 1
					#print 'count-wo: '+npp+' => '+str(count_wo)
					dtSel = dt
					ppSel = npp
					
	return FIELD_TAG_PATTERN % (ppSel,time.strftime(DATE_TIME_FORMAT,dtSel))

	
	
	

def __main__():
	
	
	
	count = 0
	count_pattern = 0
		
	print '\t\t#### EARLIEST PRIORITY SELECTOR ####\n'
	print '# Please, write the input file name, as in following the example.'
	print '# DO NOT forget to add the extension .txt'
	print '\n# EXAMPLE: file_name.txt\n'
	entrada = raw_input(">>> Input file name: ") 
	arquivo_de_entrada = entrada
	print '\n\n# Now, write a name to the output file (different from the input file).'
	print '# DO NOT forget to add the extension .txt\n'
	saida = raw_input(">>> Output file name: ")
	arquivo_de_saida = saida

	try:
		fileIn = open(arquivo_de_entrada, 'r')
		fileOut = open(arquivo_de_saida, 'w')
	except:
		raw_input('# File not found. Please, try again!')
		sys.exit()

	print ''
	print '-----------------------------------------------------------------------------'
	print '\n# Treating the file: '+arquivo_de_entrada+''
	print '#Please, wait...'
	arr = []
	patternPI = re.compile("^PI (.*)")
	patternNext = re.compile("^ [ ]*(.*)")
	pi_active = STORE_PI_DISABLE

	print ''
	print '# Output file: '+arquivo_de_saida+'\n'


	try:
		for line in fileIn:
			count = count + 1
			
			if pi_active == STORE_PI_ENABLE:
				ret2 = patternNext.match(line)
				if (ret2 != None) :
					arr.append(ret2.group(1))
				else: 
					fileOut.write(generateNewField(makePPList(arr, count)))
					arr = []
					count_pattern = count_pattern + 1;
					pi_active = STORE_PI_DISABLE

			if (pi_active == STORE_PI_DISABLE):
				ret = patternPI.match(line)
				if (ret != None) :
					arr.append(ret.group(1))
					pi_active = STORE_PI_ENABLE
			fileOut.write(line);
	finally:
		print 'Number of records with two or more earliest date: '+str(count_wo)
		print '\n-----------------------------------------------------------------------------'
		fileIn.close()
		fileOut.close()

	raw_input('\n# Press ENTER to finish')
__main__();	

