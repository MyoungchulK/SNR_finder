import ROOT
from ROOT import TGraph
from ROOT import gInterpreter, gSystem
import numpy as np
import os, sys
from matplotlib import pyplot as plt

# custom lib
import SNR_def as snr_def

ROOT.gSystem.Load(os.environ.get('ARA_UTIL_INSTALL_DIR')+"/lib/libAraEvent.so")
gInterpreter.ProcessLine('#include "'+os.environ.get('ARA_UTIL_INSTALL_DIR')+'/../misc_build/include/FFTtools.h"')

#load data
wf = np.loadtxt('example_interpolated_wf_A2_R1449_E452_Ch7.txt')

# shape info
# wf[:,0] -> time(ns)
# wf[:,1] -> volt(mV)



# 1 SNR from FFTtools
# make Tgraph for uising ROOT.FFTtools.getWaveformSNR()
ex_gr = TGraph(len(wf[:,0]), np.array(wf[:,0]), np.array(wf[:,1]))

# test ROOT.FFTtools.getWaveformSNR()
snr_ffttools = ROOT.FFTtools.getWaveformSNR(ex_gr)
print('SNR from FFTtools:',snr_ffttools)

# 2 SNR from python version of FFTtools(double check)
snr_fft, p2p_fft, rms_fft = snr_def.FFTtools_p2p_SNR(wf[:,1])
print('SNR from FFTtools(python version):',snr_fft)
print('Maximum p2p:',p2p_fft)
print('RMS:',rms_fft)

# 3 SNR from scipy extrema method
snr_py, p2p_py, rms_py = snr_def.py_p2p_SNR(wf[:,1])
print('SNR from Extrema:',snr_py)
print('Maximum p2p:',p2p_py)
print('RMS:',rms_py)


# plot in slack
# locate extrema
max_peak1, max_peak_index1 = snr_def.extrema_locator(wf[:,1], np.greater_equal)
min_peak1, min_peak_index1 = snr_def.extrema_locator(wf[:,1], np.less_equal)

# 1st plot
fig, ax = plt.subplots(figsize=(12, 6))
plt.ylabel(r'Amplitude [ $mV$ ]', fontsize=25)
plt.xlabel(r'Bin #', fontsize=25)
plt.grid(linestyle=':')
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.title(r'A2, R1449, E452, D4BV', y=1.02,fontsize=25)
plt.ylim(-1000,1000)
plt.xlim(-50,800)

plt.plot(wf[:,1],'o-',color='blue',alpha=0.7,label='WF')
plt.plot(max_peak_index1, max_peak1,'o',color='green',label='Max extrema')
plt.plot(min_peak_index1, min_peak1, 's',color='red',label='Min extrema')

plt.annotate('SNR(FFTtools, original code):'+str(snr_ffttools), (0, 850), fontsize=15)
plt.annotate('SNR(FFTtools):'+str(snr_fft), (0, 700), fontsize=15)
plt.annotate('SNR(Extrema):'+str(snr_py), (0, 550), fontsize=15)

plt.annotate('RMS(FFTtools):'+str(rms_fft), (0, -550), fontsize=15)
plt.annotate('RMS(Extrema):'+str(rms_py), (0, -700), fontsize=15)

plt.legend(loc='best',numpoints = 1 ,fontsize=18)
fig.savefig('plot1.png',bbox_inches='tight')#,dpi=100)
plt.close()
print('1st plot is done!')

# 2nd plot
fig, ax = plt.subplots(figsize=(12, 6))
plt.ylabel(r'Amplitude [ $mV$ ]', fontsize=25)
plt.xlabel(r'Bin #', fontsize=25)
plt.grid(linestyle=':')
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.title(r'A2, R1449, E452, D4BV', y=1.02,fontsize=25)
plt.ylim(-1000,1000)
plt.xlim(450,550)

plt.plot(wf[:,1],'o-',color='blue',alpha=0.7,label='WF')
plt.plot(max_peak_index1, max_peak1,'o',markersize=8, color='green',label='Max extrema')
plt.plot(min_peak_index1, min_peak1, 's',markersize=8, color='red',label='min extrema')

plt.annotate(str(wf[493,1])+'(FFTtools, Extrema)', (493, wf[493,1]-110), fontsize=15, color='red')
plt.annotate(str(wf[491,1])+'(Extrema)', (491-35, wf[491,1]+100), fontsize=15, color='green')
plt.annotate(str(wf[498,1])+'(FFTtools)', (498-2, wf[498,1]+100), fontsize=15, color='green')

plt.annotate('p2p(FFTtools):'+str(p2p_fft), (452, -500), fontsize=12)
plt.annotate('p2p(Extrema):'+str(p2p_py), (452, -650), fontsize=12)

plt.legend(loc='best',numpoints = 1 ,fontsize=12)
fig.savefig('plot2.png',bbox_inches='tight')#,dpi=100)
plt.close()
print('2nd plot is done!')


















