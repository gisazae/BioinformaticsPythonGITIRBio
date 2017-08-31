#! /usr/bin/env python

import csv
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Generate a list the number of hits for each evalue.')
	parser.add_argument('input', help='file containing the anotation result ')
	parser.add_argument('output', help = 'Name and path of result.')
	args = parser.parse_args()
	ofile=open(args.output,"w")
	evalues=[]
	hitCount=[]
	temp=[]
	with open(args.input, 'r') as csvfile:
		anotation = csv.reader(csvfile, delimiter='\t')
		next(anotation, None)
		for row in anotation:
			if(row[8]!="No_evalue"):
				evalues.append(row[8])
	evalues.sort()
	for evalue in evalues:
		if evalue not in temp:
			temp.append(evalue)
			hitCount.append(evalues.count(evalue))
	writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)
	writer.writerow(("evalue","number_of_hits"))
	for index in range(len(temp)):
		writer.writerow((temp[index],hitCount[index]))
	ofile.close()
