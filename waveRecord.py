"""
PyAudio example:Record every second, and detect pitch
"""

import pyaudio
import wave
import sys
import array
import numpy as np
import scipy.signal as signal
import scipy.fftpack as fp
from struct import pack
from Parabolic import parabolic

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = 'test.wav'

THRESHOLD = 2000

def record(rate=RATE,channels=CHANNELS,filename = None):
	"""
	Record a period of sound from the microphone and 
	return the data as an array of signed shorts.

	Normalizes the audio, trims silence from the 
	start and end.
	"""
	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
	                channels=channels,
	                rate=rate,
	                input=True,
	                frames_per_buffer=CHUNK)

	num_silent = 0	#number of silent buffers read. 
	snd_started = False	#determine is sound have started.

	r = array.array('h')	#to store raw recorded data

	print("* recording")

	while 1:
		snd_data = array.array('h', stream.read(CHUNK))	#read CHUCK frames
		r.extend(snd_data)

		silent = is_silent(snd_data)

		if silent and snd_started:
			num_silent += 1
		elif not silent and not snd_started:
			snd_started = True
		#if we got sound, and silence after that. stop recording
		if snd_started and num_silent >30:
			break
	print("* done recording")

	sample_width = p.get_sample_size(FORMAT)
	stream.stop_stream()
	stream.close()
	p.terminate()

#	r = normalize(r)
	r = trim(r)
	return sample_width, r
	# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	#     data = stream.read(CHUNK)
	#     frames+=data

#	data = array.array('h',frames)
		# fs = RATE
		# detectedf,d,corr = freq_from_autocorr(data, fs)

		# print("Frequency detected:",detectedf)

		# if (detectedf >350 and detectedf < 550):
		# 	break;


def record_to_file(filename):
	sample_width, snd_data = record()
	data = pack('<'+('h'*len(snd_data)), *snd_data)

	wf = wave.open(filename, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(sample_width)
	wf.setframerate(RATE)
	wf.writeframes(data)
	wf.close()


def pitch_detect(sample):
	if  type(sample) is array.array:
		pass
	else:
		sample = array.array('h',sample)
	window = signal.blackmanharris(len(sample),False)
	window = np.array(window)
	window -=window.mean()
	freq= abs(fp.rfft(window))

	i = np.argmax(abs(freq)) # Just use this for less-accurate, naive version
	true_i = parabolic(np.log(abs(freq)), i)[0]
    
    # Convert to equivalent frequency
	return RATE * true_i / len(window)

def waveopen(filename):
	wf = wave.open(filename,'rb')
	nframes= wf.getnframes()
	frames=wf.readframes(nframes)
	data = array.array('h',frames)
	return data

def is_silent(snd_data):
	return max(snd_data) < THRESHOLD

def trim(snd_data):
	"Trim the blank spots at the start and end"
	def _trim(snd_data):
		snd_started = False
		r = array.array('h')

		for i in snd_data:
			if not snd_started and abs(i)>THRESHOLD:
				snd_started = True
				r.append(i)
			elif snd_started:
				r.append(i)
		return r

	#trim to the left
	snd_data = _trim(snd_data)
	#trim to the right
	snd_data.reverse()
	snd_data = _trim(snd_data)
	snd_data.reverse()
	return snd_data


if __name__ == "__main__":
	data = waveopen('test.wav')