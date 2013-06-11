GNRGX
=====

GAMESS Energy value Extractor

For extracting surface mapping geometry line-pairs of the form

     COORD 1=  .000 COORD 2=  .000
     HAS ENERGY VALUE    -847.041249

from GAMESS (version 1 may 2012 (r1)) log files

Default output is as a CSV file, but may also output a COORD1, COORD2, VALUE list using the -l flag

Usage
=====

	usage: extract.py [-h] [-l] [-o OUT] IN

	Process log file to CSV table

	positional arguments:
	  IN                    log file to process

	optional arguments:
	  -h, --help            show this help message and exit
	  -l, --list            dump output as a list rather than a table
	  -o OUT, --outfile OUT dump output to specified

Examples:

*  `./extract.py product_scan_dual.log -o table.csv` (write csv data to `table.csv`)
* `python extract.py product_scan_cont.log -l` (output a list of data triples to the screen)

