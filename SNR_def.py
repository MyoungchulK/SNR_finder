import numpy as np
import os, sys
from scipy.signal import argrelextrema

# copy of ROOT.FFTtools.getWaveformSNR() from FFTtools.cxx
# original code is in /cvmfs/ara.opensciencegrid.org/trunk/centos7/source/libRootFftwWrapper/src/FFTtools.cxx
def FFTtools_p2p_SNR(v):

    # sampling rms
    nRMS = 25
    rms = np.nanstd(v[:nRMS])
    del nRMS

    #p2p
    trending = 3
    p2p = 0
    firstBin = 0
   
    for i in range(len(v)):
        # set standard bin for compare with bafore and after bin
        y = v[i]
       
        # analyzing from second bin
        if i > 0:
            if y < v[i-1] and trending == 0:
                #if np.abs(y - v[firstBin] > p2p):
                if np.abs(y - v[firstBin]) > p2p:
                    p2p = np.abs(y - v[firstBin])
            elif y < v[i-1] and (trending == 1 or trending == 2):
                trending = 0
                firstBin = i-1
                #if np.abs(y - v[firstBin] > p2p):
                if np.abs(y - v[firstBin]) > p2p:
                    p2p = np.abs(y - v[firstBin])
            elif y > v[i-1] and (trending == 0 or trending == 2):
                trending = 1
                firstBin = i-1
                #if np.abs(y - v[firstBin] > p2p):
                if np.abs(y - v[firstBin]) > p2p:
                    p2p = np.abs(y - v[firstBin])
            elif y > v[i-1] and trending == 1:
                #if np.abs(y - v[firstBin] > p2p):
                if np.abs(y - v[firstBin]) > p2p:
                    p2p = np.abs(y - v[firstBin])
            elif y == v[i-1]:
                trending = 2
            elif trending == 3:
                if y < v[i-1]:
                    trending = 0
                    firstBin = 0
                if y > v[i-1]:
                    trending = 1
                    firstBin = 0
            else:
                print("trending cock up!")
                print('y',y,' v[i]',v[i],' v[i-1]',v[i-1])                
                return -1

            #print(p2p)
    
    del trending, firstBin, y
    
    # original
    #p2p /= 2.
    #return p2p / rms
   
    # for debug
    p2p_max = p2p / 2.
    return p2p_max/rms, p2p, rms


# python version of p2p snr calculator
# it is using scipy.signal.argrelextrema library
def extrema_locator(v, comparator):
    
    # locate index of the extrema
    i_ex = argrelextrema(v, comparator, order=1)[0]

    # check neighboring extrema(equal value)
    i_nei_ex = (i_ex[1:] - i_ex[:-1]).astype(int)

    # locate neighboring extrema(equal value)
    i_nei_ex_loc = np.where(i_nei_ex == 1)[0] # remove first neighboring extrema
    del i_nei_ex 

    # delete one of the neighboring extrema(equal value)
    i_ex = np.delete(i_ex, i_nei_ex_loc)
    del i_nei_ex_loc

    # fine index value
    ex_peak = v[i_ex]

    return ex_peak, i_ex

def py_p2p_SNR(v):

    # fine index value
    max_peak, max_peak_index = extrema_locator(v, np.greater_equal)
    min_peak, min_peak_index = extrema_locator(v, np.less_equal)

    #match the length by cutting last value
    max_len = len(max_peak)
    min_len = len(min_peak)
    if max_len > min_len:
        max_peak = max_peak[:min_len]
    elif max_len < min_len:
        min_peak = min_peak[:max_len]
    else:
        pass
    del max_len, min_len

    #calculate p2p value
    if max_peak_index[0] > min_peak_index[0]:
        p2p_1 = np.abs(max_peak - min_peak)
        p2p_2 = np.abs(max_peak[:-1] - min_peak[1:])
    else:
        p2p_1 = np.abs(max_peak - min_peak)
        p2p_2 = np.abs(max_peak[1:] - min_peak[:-1])
    del max_peak_index, min_peak_index, max_peak, min_peak
    
    #maximum p2p
    p2p = np.concatenate((p2p_1, p2p_2), axis=None)
    #print(p2p)

    del p2p_1, p2p_2
    p2p_max = np.nanmax(p2p) / 2

    # sampling rms
    nRMS = 25
    rms = np.nanstd(v[:nRMS])
    del nRMS

    return  p2p_max / rms, np.nanmax(p2p), rms























































