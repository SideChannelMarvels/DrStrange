#!/usr/bin/python3

# This script reads Matlab MAT files, each one containing a power trace,
# and shows it on the screen
#
# This script can be run either invoking python
#   python3 -f read_mat
# or, if python3 is in the path described in line 1, directly:
#   ./read_mat.py

#########################################
# Libraries
#########################################
import os

#https://docs.python.org/3/library/binascii.html
import binascii

# Include library to manipulate Matlab MAT files.
# Documentation can be found at:
# https://scipy-cookbook.readthedocs.io/items/Reading_mat_files.html
from scipy.io import loadmat

# Include library to debug python scripts.
# Documentation can be found at:
# https://docs.python.org/3/library/pdb.html
import pdb                      # for python debugging. Continue with 'c'

#########################################
# folder and file definitions
#########################################

# This code expects that the incoming folder contains one file per trace, saved as MAT file, and that
# its name contains the key, plaintext and ciphertext used, in this format:
# trace_DES__k=f49d7b07c3ee29ef_m=004c5517a01903c7_c=c2eb8188c1e11cd6.mat
INCOMING_FOLDER='2019-03-1ktraces_mat'

#just a counter
ntraces=0
#########################################
# main code
#########################################

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

    # this data will be needed to recover the original data, in read functions
    # more information on data types can be seen in:
    # https://docs.python.org/2/library/struct.html
    # This is EXACTLY the parameter we need to pass to unpack() function in order to read
    # back the data
    data_format = matfile['trace'][0].dtype.byteorder + matfile['trace'][0].dtype.char
    # this code returns a NUMPY ndarray:
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html
    trace = matfile['trace']

    # parses filename separating ciphertext (c), plaintext (m) and key (k)
    init_pos=filename.find('k=')
    key=filename[init_pos+2:init_pos+18]

    init_pos=filename.find('m=')
    message=filename[init_pos+2:init_pos+18]

    init_pos=filename.find('c=')
    ciphertext=filename[init_pos+2:init_pos+18]

    # shows the trace content

    print('################################################################################')
    print('Trace {0:d}: {1:d} samples, format {2}'.format(ntraces, len(trace), data_format ))
    print('            initial 10 samples: {0}'.format(trace[0:10]))
    print('            minimum value in trace: {0}'.format(min(trace)))
    print('            maximum value in trace: {0}'.format(max(trace)))

    # Uncomment the following line for debug - stops at each trace processed
    #pdb.set_trace() # for debug. continue with 'c'

    ntraces=ntraces+1
    # display a message each 100 traces processed
    if ntraces % 100 == 0 :# or ntraces < 10:
        print(' '+str(ntraces)+' traces processed !')
        break;

