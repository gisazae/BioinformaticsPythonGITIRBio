#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get the number of contigs that matched a hit.')
    parser.add_argument('input', help='file containing the list of contigs ')
    args = parser.parse_args()
    contigs=[]
    with open(args.input, 'r') as contigFile:
	contigFile.readline()
	contigFile.readline()
	contigFile.readline()
        for line in contigFile:
            if line in ['\n', '\r\n']:
    		break
            contigs.append((line[:11]).strip())
    print len(set(contigs))
