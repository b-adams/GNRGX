#!/usr/bin/python

# extract.py - Extract Coord/Energy information from GAMESS logfiles

# Copyright 2013 Bryant Adams

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import itertools
import argparse
import sys
import csv
from collections import defaultdict

__author__ = 'badams'

# from itertools recipe: http://docs.python.org/2/library/itertools.html
def pairwise(iterable):
    "s -> (s0, s1), (s1, s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)

def coord_finder(filename):
    with open(filename) as dataset:
        reCoordMatch = r'\s*COORD 1=\s*(-?\d*\.\d*)\s*COORD 2=\s*(-?\d*\.\d*)\s*'
        reValMatch = r'\s*HAS ENERGY VALUE\s*(-?\d*\.\d*)'
        for line, next_line in pairwise(dataset):
            if 'COORD 1=' in line:
                cMatchOb = re.match(reCoordMatch, line)
                vMatchOb = re.match(reValMatch, next_line)
                if cMatchOb and vMatchOb:
#                    print line, next_line
                    yield cMatchOb.group(1), cMatchOb.group(2), vMatchOb.group(1)


def process_file(filename, asList, whereToWrite):
    if asList:
        for coord1, coord2, energy in coord_finder(filename):
            whereToWrite.write(str(coord1)+" "+str(coord2)+" "+str(energy)+"\n")
    else:
        print "CSV output not yet supported"
        dataset = defaultdict(dict)
        rows = defaultdict(int)
        cols = defaultdict(int)

        for coord1, coord2, energy in coord_finder(filename):
            rowname = str(coord2)
            colname = str(coord1)
            cols[colname] +=1
            rows[rowname] +=1
            dataset[rowname][colname] = str(energy)
        colnames = sorted(cols)
        rownames = sorted(rows)

        print colnames
        print rownames
        
        cwriter = csv.DictWriter(whereToWrite, dialect='excel', fieldnames=colnames, 
                                 delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        cwriter.writeheader()
#        cwriter.writerow(dict((x, x) for x in colnames)) #Write headers
        for row in rownames:
            cwriter.writerow(dataset[row])
        
        print "CSV output attempted"

def main():
    parser = argparse.ArgumentParser(description='Process log file to CSV table')
    parser.add_argument('infile', metavar='IN', help='log file to process')
    parser.add_argument('-l', '--list', help='dump output as a list rather than a table', action='store_true')
    parser.add_argument('-o', '--outfile', metavar='OUT', help='dump output to this file')
    args = parser.parse_args()

    if args.outfile:
        with open(args.outfile, 'w') as outputFile:
            process_file(args.infile, args.list, outputFile)
    else:
        process_file(args.infile, args.list, sys.stdout)

if __name__ == "__main__":
    sys.exit(main())