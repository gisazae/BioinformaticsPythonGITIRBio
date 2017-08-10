#!/usr/bin/python
# GITIRBio -> GITIR
""" Genera una lista de la cantidad de contigs agrupados por el tamaño de los contig ,
la salida de este archivo es utilizado por assembly1_2.R"""
from Bio import SeqIO
import argparse
import csv

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='length list of contig fasta file.')
	parser.add_argument('input', help='fasta file containing the contigs ')
	parser.add_argument('output', help = 'Name and path of result.')
	args = parser.parse_args()
	with open(args.input, 'r') as seq:
		sizes = [len(record) for record in SeqIO.parse(seq, 'fasta')]
	sizeCount=[]
	sizes.sort()
	temp=[]
	for size in sizes:
		if size not in temp:
			temp.append(size)
			sizeCount.append(sizes.count(size))
	rows=zip(temp,sizeCount)
	ofile  = open(args.output, "wb")
	writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)
	writer.writerow(("size","sizeCount"))
	for row in rows:
    		writer.writerow(row)
	ofile.close()	
