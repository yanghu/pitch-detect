from scipy.signal import fftconvolve
import matplotlib.mlab as mlab
from numpy import linspace,sin,pi,diff,argmax
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
fs = int(4.41e5)
window_len = fs/10
x=linspace(0,0.1,fs/10)
f=f_A4  #frequency of A4 note

f=27.5  #frequency of A4 note
y=sin(2*pi*f*x)+0.5 #manually add an offset

tic=time.perf_counter()
window = y[0:0+window_len]
res,d,corr=freq_from_autocorr(window,fs)
toc=time.perf_counter()
timediff=toc-tic
print("Detected frequency is:", res, "and the true frequency is :", f)
print("Time elapsed:", timediff)
