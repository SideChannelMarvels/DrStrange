#!/usr/bin/python3

# This is a sample script to create Riscure TRS files from a
# set of traces in Matlab MAT format.
# It can be adapted to CSV-style easily
#
# It uses the python library provided by Riscure and scipy to
# manipulate MATLAB-dependent format.
#
# The trsfile package can be either found at its github page:
#   https://github.com/Riscure/python-trsfile
# and in the pip3 installer:
#   pip3 install trsfile
#
# This script can be run either invoking python
#   python3 -f matlab_to_trs
# or, if python3 is in the path described in line 1, directly:
#   ./matlab_to_trs.py


#########################################
# Libraries
#########################################

import os

#https://docs.python.org/3/library/binascii.html
import binascii

# libraries needed to read MAT files
# https://scipy-cookbook.readthedocs.io/items/Reading_mat_files.html
from scipy.io import loadmat

# To manipulate Riscure TRS files, may be useful.
import trsfile
from trsfile import trs_open, Trace, SampleCoding, TracePadding, Header

# debugging doc: 
#https://docs.python.org/3/library/pdb.html
import pdb                      # for python debugging. Continue with 'c'

#########################################
# folder and file definitions
#########################################
INCOMING_FOLDER='/home/luciano/Documentos/mestrado/pesquisa/traces/DEMA_GALS2_noRC_noPipe_100000PTI_1av_mat'
OUTCOMING_FOLDER='DEMA_GALS2_noRC_noPipe_100000PTI_1av'
TRS_FILENAME='DEMA_GALS2_noRC_noPipe_100000PTI.trs'

# daredevil file
traces_filename=OUTCOMING_FOLDER+'/'+TRS_FILENAME+'.traces'

# simple counter
ntraces=0

#########################################
# main code
#########################################
os.system('mkdir '+OUTCOMING_FOLDER)

# opens TRS files for editing
traces = open(traces_filename, 'ab')

trs_file = trs_open(
    OUTCOMING_FOLDER+'/'+TRS_FILENAME,                 # File name of the trace set
    'w',                             # Mode: r, w, x, a (default to x)
    # Zero or more options can be passed (supported options depend on the storage engine)
    #engine = 'TrsEngine',            # Optional: how the trace set is stored (defaults to TrsEngine)
    #headers = {                      # Optional: headers (see Header class)
    #	Header.LABEL_X: 'Testing X',
    #	Header.LABEL_Y: 'Testing Y',
    #	Header.DESCRIPTION: 'Testing trace creation',
    #},
    padding_mode = TracePadding.AUTO,# Optional: padding mode (defaults to TracePadding.AUTO)
    live_update = True               # Optional: updates the TRS file for live preview (small performance hit)
                                 #   0 (False): Disabled (default)
                                 #   1 (True) : TRS file updated after every trace
                                 #   N        : TRS file is updated after N traces
    )

# loop over all files from incoming folder
for filename in os.listdir(INCOMING_FOLDER):

    if not filename.endswith(".mat"):
        print('  skipping '+filename)
        # print(os.path.join(directory, filename))
        continue

    #print('processing '+filename)

    # reading matlab files in python, using scipy:
    # https://docs.scipy.org/doc/scipy/reference/tutorial/io.html
    matfile = loadmat(INCOMING_FOLDER+'/'+filename)

    # this code returns a NUMPY ndarray:
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html
    trace = matfile['trace']

    # for debug
    #print('Trace: {0:d} samples, type {1}, name {2}'.format(matfile['trace'].size, filename, matfile['trace'].dtype))
    #print('            initial 10 samples: {0}'.format(trace[0:10]))
#    pdb.set_trace() # for debug. continue with 'c'

    # saves data as TRS file
    trs_file.append(
            Trace(
       	        SampleCoding.FLOAT,
                trace[0].tolist(), #trsfile expects a list object, matfile returns a numpy ndArray
                title = filename
            )
    )

    # display a message each 100 traces processed
    ntraces +=1
    if ntraces % 100 == 0 or ntraces < 10:
        print(' '+str(ntraces)+' traces processed !')

print('done!')
