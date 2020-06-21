#!/usr/bin/python3

# sample code to read a Daredevil file and show its contents.
#
# This script can be run either invoking python
#   python3 -f read_daredevil
# or, if python3 is in the path described in line 1, directly:
#   ./read_daredevil.py

#########################################
# Libraries
#########################################
import os
import sys
import glob
import struct
import binascii

# debugging doc: 
#https://docs.python.org/3/library/pdb.html
import pdb                      # for python debugging.

#########################################
# folder and file definitions
#########################################

# this is the folder which contains the data
#OUTCOMING_FOLDER='2019-03-1ktraces_mat_processed'
OUTCOMING_FOLDER='.'

# The base name for Daredevil files
TRS_FILENAME='trace-set.trs'
basic_filename=OUTCOMING_FOLDER+'/'+TRS_FILENAME

# name of the folder containing the configuration file
config_filename=basic_filename+'.config'

# name of the folder containing the traces - can be read from config file
#traces_filename=basic_filename+'.traces'
# name of the folder containing the plaintext - can be read from config file
#input_filename=basic_filename+'.input'

#########################################
# Configuration read
#########################################

# Read the configuration file to extract nsamples, ntraces, sample_size
# Reads it line by line and searches for the strings needed.
# Could be done more efficiently, but it works.
with open(config_filename, 'r') as config:
    for line in config:
        #line=config.readline()
        if line.find('trace=') >= 0 :
            traces_filename = line.split('=')[1].split(' ')[0]
            ntraces    = int(line.split('=')[1].split(' ')[1])

        if line.find('nsamples') >= 0 :
            nsamples = int(line.split('=')[1])

        if line.find('guess=') >=0:
            ntraces    = int(line.split(' ')[1])
            guess_size = int(line.split(' ')[2])

        if line.find('trace_type') >= 0:
            # the types of struct are found at:
            # https://docs.python.org/2/library/struct.html
            trace_type = line.split('=')[1].split('\n')[0]
            # detect if the format contains the endianess of the data
            if trace_type[0] in ['@', '=' , '<','>','!'] :
                endianess   = trace_type[0]
                data_format = trace_type[1]
            else:
                endianess   = ''
                data_format = trace_type[0]
            # identify the sample size, using a switch case-like structure:
            # https://jaxenter.com/implement-switch-case-statement-python-138315.html
            sample_size_switch_case = {
                'h'  : 2,
                'f'  : 4,
                }
            sample_size = sample_size_switch_case.get(data_format,3)

# This way is more cryptic, but searches the file, instead of testing each
#  line for the ocurrence of ntraces
#config_fid = open(config_filename, 'r')
#config_content = config_fid.read() # reads all the file
#init = config_content.find('nsamples') # searches for the first ocurrence of 'nsamples'
#nsamples = int(config_content[init:].split('\n')[0].split('=')[1]) # extracts nsamples, with a little magic

# show the information read from config file, for debug
#print('nsamples = {0}, ntraces {1} sample_size {2}, data_format {3}, endianess {4}'.format(nsamples, ntraces, sample_size, data_format, endianess))
#pdb.set_trace() # for debug. continue with 'c'


#########################################
# Trace and input data read
#########################################
inputs_fid = open(input_filename, 'rb')

with open(traces_filename, 'rb') as traces:
   for i in range(0,ntraces):
       trace_byte = traces.read(nsamples*sample_size)
       trace_float = struct.unpack(endianess+str(nsamples)+data_format,trace_byte)
       input_data  = binascii.b2a_hex(inputs_fid.read(guess_size))
       print('################################################################################')
       print('Trace {0:d}: {1:d} samples, name {2}'.format(i, len(trace_float), input_data ))
       print('            initial 10 samples: {0}'.format(trace_float[0:10]))
       print('            minimum value in trace: {0}'.format(min(trace_float)))
       print('            maximum value in trace: {0}'.format(max(trace_float)))

       # for debug - stops at each trace processed
       pdb.set_trace() # for debug. continue with 'c'

       if i % 100 == 0 or i < 10:
          print(' '+str(i)+' traces processed !')



