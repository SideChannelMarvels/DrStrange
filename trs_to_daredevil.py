#!/usr/bin/python3

# This is a simple script to create Daredevil files from a
# Riscure TRS file containing power traces.
#
# The trsfile package can be either found at its github page:
#   https://github.com/Riscure/python-trsfile
# and in the pip3 installer:
#   pip3 install trsfile
#
# This script can be run either invoking python
#   python3 -f trs_to_daredevil
# or, if python3 is in the path described in line 1, directly:
#   ./trs_to_daredevil.py

#########################################
# Libraries
#########################################
import os
import sys
import glob
import struct
#https://docs.python.org/3/library/binascii.html
import binascii

import trsfile
from trsfile import trs_open, Trace, SampleCoding, TracePadding, Header

# debugging doc: 
#https://docs.python.org/3/library/pdb.html
import pdb                      # for python debugging.

#########################################
# folder and file definitions
#########################################

# The file which will be stored the daredevil files - Will be created, if not available
OUTCOMING_FOLDER='DEMA_GALS2_noRC_noPipe_100000PTI_1av'
#OUTCOMING_FOLDER='.'

#trs_filename=sys.argv[1]
trs_filename=OUTCOMING_FOLDER+'/'+'DEMA_GALS2_noRC_noPipe_100000PTI.trs'
traces_filename=trs_filename+'.traces'
input_filename=trs_filename+'.input'
config_filename=trs_filename+'.config'

traces_loop=0

#########################################
# main code
#########################################

traces_file = open(traces_filename, 'wb')
tracename_file=open(input_filename, 'wb')

with trsfile.open(trs_filename, 'r') as traces:
	# Show all headers
	for header, value in traces.get_headers().items():
		print(header, '=', value)
	print()
	ntraces     = traces.get_header(Header.NUMBER_TRACES)
	nsamples    = traces.get_header(Header.NUMBER_SAMPLES)
	#isfloat     = Header.SAMPLE_CODING.value == 63
	isfloat     = traces[0].sample_coding.is_float
	#samplesize
	#datasize
	#pdb.set_trace()
        
	# Iterate over all the traces
	for i, trace in enumerate(traces[:]):
	    pdb.set_trace() # for debug. continue with 'c'
	    # saves the trace content
            data_format = trace[:].dtype.byteorder + trace[:].dtype.char
	    traces_file.write(trace[:].tobytes())

            filename = trace.title
            # parses filename separating ciphertext (c), plaintext (m) and key (k)
            init_pos=filename.find('k=')
            key=filename[init_pos+2:init_pos+18]

            init_pos=filename.find('m=')
            message=filename[init_pos+2:init_pos+18]

            init_pos=filename.find('c=')
            ciphertext=filename[init_pos+2:init_pos+18]

            # Writes the plaintext as daredevil expects it
            tracename_file.write(binascii.a2b_hex(message))
            
            # ensures we write the data
            tracename_file.flush
            traces.flush()

            # display a message each 100 traces processed
	    if i % 100 == 0 or i < 10:
	        print(' '+str(i)+' traces processed !')


# creates the configuration file
with open(config_filename, 'w') as config:
        config.write(
"""
[Traces]
files=1
trace_type={format}
transpose=true
index=0
nsamples={nsamples}
trace={traces_filename} {ntraces} {nsamples}

[Guesses]
files=1
guess_type=u
transpose=true
guess={input_filename} {ntraces} 8

[General]
threads=8
order=1
return_type=double
algorithm=DES
position=LUT/DES_BEFORE_SBOX
round=0
bitnum=none
bytenum=all
#correct_key={key}
memory=4G
top=20
""".format(format=data_format, ntraces=ntraces, nsamples=nsamples, traces_filename=traces_filename, input_filename=input_filename, key=key))

