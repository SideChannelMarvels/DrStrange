#!/usr/bin/python3

# sample code to read a TRS file and show its contents.
# By default it reads the trace

# The trsfile package can be either found at its github page:
#   https://github.com/Riscure/python-trsfile
# and in the pip3 installer:
#   pip3 install trsfile
#
# This script can be run either invoking python
#   python3 -f read_trs
# or, if python3 is in the path described in line 1, directly:
#   ./read_trs.py

#########################################
# Libraries
#########################################
import trsfile

# debugging doc: 
#https://docs.python.org/3/library/pdb.html
import pdb                      # for python debugging.

#########################################
# folder and file definitions
#########################################

# The file which contains the TRS files
OUTCOMING_FOLDER='DEMA_GALS2_noRC_noPipe_100000PTI_1av'
#OUTCOMING_FOLDER='.'

#TRS_FILENAME='trace-set.trs'
TRS_FILENAME='DEMA_GALS2_noRC_noPipe_100000PTI.trs'
input_filename=OUTCOMING_FOLDER+'/'+TRS_FILENAME

#########################################
# main code
#########################################

with trsfile.open(input_filename, 'r') as traces:
	# Show all headers
	for header, value in traces.get_headers().items():
		print(header, '=', value)
	print()
        
	# Iterate over the first 25 traces
	for i, trace in enumerate(traces[0:25]):
                # for debug - stops at each trace processed
		# pdb.set_trace() # for debug. continue with 'c'
		print('################################################################################')
		print('Trace {0:d}: {1:d} samples, name {2}'.format(i, len(trace), trace.title))
		print('            initial 10 samples: {0}'.format(trace[0:10]))
		print('            minimum value in trace: {0}'.format(min(trace)))
		print('            maximum value in trace: {0}'.format(max(trace)))

