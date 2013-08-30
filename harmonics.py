import numpy
from matplotlib import pyplot as plt
from numpy import sin,pi

def harmonic_series(fbase,len=None):
	if len == None:
		len=0.03
	x=numpy.arange(0,len,1/44000)
	harmo_f = [fbase*n for n in range(1,10)]
	t=[]
	for freq in harmo_f:
		t.append(sin(2*pi*freq*x))
	return t

def stack(orders,t):
	combined = None
	for order in orders:
		combined += t[order]
	return combined


def just_into_tune():
	notes = list('CcDdEFfGgAaB')

	def getnext(key):
		ind = (notes.index(key)+7)%12
		return notes[ind]

	tune={}
	key='C'
	tune['C']=100
	newkey = getnext(key)
	while newkey!='C':
		tmp_freq = (tune[key]*1.5)
		while tmp_freq >= 200:
			tmp_freq/=2
		tune[newkey] = tmp_freq
		key = newkey
		newkey = getnext(key)
	C4 = 261.63
	freqs = [tune[key]*C4/100 for key in notes]
	
def well_tempered():
	notes = list('CcDdEFfGgAaB')
	keys = [1*2**(n/12) for n in range(13)]
	C4 = 261.63
	freqs = [key*C4 for key in keys]
	tune = dict(zip(notes,freqs))
	return tune


tunes = well_tempered()

Gs_series = harmonic_series(tunes['g'],0.5)
A_series = harmonic_series(tunes['A'],5)
E_series = harmonic_series(tunes['E'],5)
Gs4=Gs_series[0]
A4=A_series[0]
A5=A_series[1]
E5=E_series[1]
fifth = A4+E5
#semi = Gs3+A3

x=numpy.arange(0,0.1,1/44000)

plot(fifth)
plot(A4)
plot(E5)
plot(x,semi)