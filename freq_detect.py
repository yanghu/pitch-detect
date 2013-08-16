from scipy.signal import fftconvolve,hann, blackmanharris
from scipy import fftpack
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
from numpy import linspace,sin,pi,diff,argmax,log,copy
from Parabolic import parabolic
import time
f_A4=440

def freq_from_autocorr(sig, fs):
    """Estimate frequency using autocorrelation
    """
    # Calculate autocorrelation (same thing as convolution, but with
    # one input reversed in time), and throw away the negative lags
    corr = fftconvolve(sig, sig[::-1], mode='full')
    corr = corr[len(corr)/2:]
    # Find the first low point
    d = diff(corr)
    try:
        start = mlab.find(d > 0)[0]
    except IndexError as error:
        DetectionFailed(error)
        return -1
    # Find the next peak after the low point (other than 0 lag). This bit is
    # not reliable for long signals, due to the desired peak occurring between
    # samples, and other peaks appearing higher.
    # Should use a weighting function to de-emphasize the peaks at longer lags.
    corr = corr[start:]
    peak = argmax(corr) + start

    xp, yp = parabolic(corr, peak)
    #return fs/((peak-start)*2),d,corr
    return fs/((xp-start)*2),d,corr

def DetectionFailed(error):
    if isinstance(error,IndexError):
        print('Sample window too small,autocorollation failed!')


###to test the function
fs = 44100
window_len = fs/10
x=linspace(0,0.1,fs/10)
f=f_A4  #frequency of A4 note

#f=27.5  #frequency of A4 note
y=sin(2*pi*f*x)+0.5 #manually add an offset

tic=time.perf_counter()
window = blackmanharris(window_len,False)*y
flat = y[0:window_len]

res_wind,d,corr=freq_from_autocorr(window,fs)
res_flat,d,corr=freq_from_autocorr(flat,fs)
toc=time.perf_counter()
timediff=toc-tic
print("Detected frequency is:", res_wind, "and the true frequency is :", f)
print("Detected frequency (flat)is:", res_flat, "and the true frequency is :", f)
print("Time elapsed:", timediff)
windowed = np.array(window)
windowed-=windowed.mean()
c = abs(fftpack.rfft(windowed))
maxharms = 8
plt.subplot(maxharms,1,1)
plt.plot(log(c))
for x in range(2,maxharms):
    a = copy(c[::x]) #Should average or maximum instead of decimating
    # max(c[::x],c[1::x],c[2::x],...)
    c = c[:len(a)]
    i = argmax(abs(c))
    try:
        true_i = parabolic(abs(c), i)[0]
    except IndexError:
        true_i = i
    print ('Pass %d: %f Hz' % (x, fs * true_i / len(windowed)))
    c *= a
    plt.subplot(maxharms,1,x)
    plt.plot(log(c))
plt.show()
