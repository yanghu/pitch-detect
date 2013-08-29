import numpy
from matplotlib import pyplot as plt
from numpy import sin,pi

def harmonic_series(fbase):
	x=numpy.arange(0,0.02,1/44000)
	harmo_f = [fbase*n for n in range(10)]
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

	freqs = [tune[key] for key in notes]

A_series = harmonic_series(220)

E_series = harmonic_series(220*(2**(7/12)))
A3=A_series[1]
A4=A_series[2]
E5=E_series[2]
fifth = A4+E5


plot(fifth)
plot(A3)