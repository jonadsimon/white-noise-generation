##########################################################################################
# Read in the frequency response data, and generate synthetic data having that spectrum
##########################################################################################

import numpy as np
from scipy.interpolate import interp1d
from scipy.fftpack import ifft 
from scipy.io.wavfile import write
import os
import sys

def get_signal(freqs, responses, nyquist, sampling_rate, duration=10, lb_type='linear', ub_type='linear', eps=0.001):
	'''
	Generates noise with a desired frequency distribution. Can be used for testing audio equipment.
	The provided frequency response values are linearly interpolated between to obtain a continuous frequency response curve.
	
	The behavior of the response curve near freq=0 and freq=nyquist are determined by the 'lb_type' and 'ub_type' parameters.
	The options for these parameters are:
	1) 'zero'	- response equals zero outside of freqs
	2) 'flat'	- response value at the extremal end of freqs is repeated for all values outside of freqs
	3) 'linear'	- response is linearly interpolated outside of freqs, decreasing to zero at the boundary

	Inputs:
	'freqs' 		- array of frequencies, in Hz
	'responses' 	- array of responses corresponding to the frequency values in 'freqs'
	'nyquist'		- the nyquist limit of the generated signal, in Hz (if sampling_rate is also given, it must equal 2*nyquist)
	'sampling_rate'	- the sampling rate of the generated signal, in Hz (if nyquist is also given, it must equal sampling_rate/2)
	'duration'		= the duration of the generated signal, in seconds (10sec by default)
	'lb_type'		- how the frequency response should behave between 0 and min(freqs), one of 'zero', 'flat', or 'linear' (linear by default)
	'ub_type'		- how the frequency response should behave between max(freqs) and nyquist, one of 'zero', 'flat', or 'linear' (linear by default)
	'eps'			- the epsilon jump after which the response drops to zero in the 'zero' condition (defaults to 0.001Hz)

	Outputs:
	'times'			- array of times comprising the generated signal, in seconds
	'amplitudes'	- array of amplitudes corresponding to the time values in 'times'
	'''

	# Interpolate the values in freqs according to 'lb_type' and 'ub_type'
	# Add additional values at the boundaries for 0 and nyquist if not already included
	freqs_extended = list(freqs)
	responses_extended = list(responses)

	min_freq_idx = np.argmin(freqs_extended) # don't want to search the array multiple times
	min_freq = freqs_extended[min_freq_idx]  # don't want to search the array multiple times
	if min_freq < 0:
		raise Exception('\nfrequencies must be nonnegative\n')
	elif min_freq > 0:
		if lb_type == 'flat':
			freqs_extended.append(0)
			responses_extended.append(responses_extended[min_freq_idx])
		elif lb_type == 'linear':
			freqs_extended.append(0)
			responses_extended.append(0)
		elif lb_type == 'zero':
			freqs_extended.extend([min_freq-eps,0])
			responses_extended.extend([0,0])
		else:
			raise Exception("lb_type must be one of: 'zero', 'flat', 'linear'")

	max_freq_idx = np.argmax(freqs_extended) # don't want to search the array multiple times
	max_freq = freqs_extended[max_freq_idx]  # don't want to search the array multiple times
	if max_freq > nyquist:
		raise Exception('\nfrequencies cannot be greater than nyquist\n')
	elif max_freq < nyquist:
		if ub_type == 'flat':
			freqs_extended.append(nyquist)
			responses_extended.append(responses_extended[max_freq_idx])
		elif ub_type == 'linear':
			freqs_extended.append(nyquist)
			responses_extended.append(0)
		elif ub_type == 'zero':
			freqs_extended.extend([max_freq+eps,nyquist])
			responses_extended.extend([0,0])
		else:
			raise Exception("ub_type must be one of: 'zero', 'flat', 'linear'")

	# Compute the interpolation function
	freq_func = interp1d(freqs_extended, responses_extended, 'linear')

	# Generate the full set of sampling_rate*duration many interpolated values, and perform the ifft
	n_samples = duration * nyquist + 1 # because: duration * sampling_rate = n_samples + (n_samples - 2)
	x_f = np.linspace(0,nyquist,n_samples) # frequencies
	y = freq_func(x_f) # amplitudes
	phase = np.random.uniform(0, 2*np.pi, len(y)) # associated (random) phases
	signal_z = y*np.exp(1j*phase) # complex signal in z-space on positive frequencies
	signal_z = np.concatenate((signal_z,np.conjugate(signal_z[-2:0:-1]))) # remove extremal (0 and nyquist) amplitudes, then flip, conjugate, and concatenate
	signal_t = np.real(ifft(signal_z)) # real signal in t-space
	x_t = np.arange(0,duration,1.0/sampling_rate) # times

	return x_t, signal_t


def generate_white_noise(outfile_path, freqs, responses, nyquist=None, sampling_rate=None, duration=10, lb_type='linear', ub_type='linear', eps=0.001):
	'''
	Generates noise with a desired frequency distribution. Can be used for testing audio equipment.
	The provided frequency response values are linearly interpolated between to obtain a continuous frequency response curve.
	
	The behavior of the response curve near freq=0 and freq=nyquist are determined by the 'lb_type' and 'ub_type' parameters.
	The options for these parameters are:
	1) 'zero'	- response equals zero outside of freqs
	2) 'flat'	- response value at the extremal end of freqs is repeated for all values outside of freqs
	3) 'linear'	- response is linearly interpolated outside of freqs, decreasing to zero at the boundary

	Inputs:
	'outfile_path'  - path where generated wav file should be saved
	'freqs' 		- array of frequencies, in Hz
	'responses' 	- array of responses corresponding to the frequency values in 'freqs'
	'nyquist'		- the nyquist limit of the generated signal, in Hz (if sampling_rate is also given, it must equal 2*nyquist)
	'sampling_rate'	- the sampling rate of the generated signal, in Hz (if nyquist is also given, it must equal sampling_rate/2)
	'duration'		= the duration of the generated signal, in seconds (10sec by default)
	'lb_type'		- how the frequency response should behave between 0 and min(freqs), one of 'zero', 'flat', or 'linear' (linear by default)
	'ub_type'		- how the frequency response should behave between max(freqs) and nyquist, one of 'zero', 'flat', or 'linear' (linear by default)
	'eps'			- the epsilon jump after which the response drops to zero in the 'zero' condition (defaults to 0.001Hz)

	Outputs: None
	'''

	# Check that 'nyquist' and 'sampling_rate' agree
	if not nyquist and not sampling_rate:
		raise Exception('\nEither nyquist or sampling_rate must be provided\n')
	elif nyquist and sampling_rate:
		if nyquist != sampling_rate/2.0:
			raise Exception('\nnyquist must equal sampling_rate/2\n')
	elif nyquist:
		sampling_rate = 2*nyquist
		if nyquist < max(freqs):
			raise Exception('\nfreqs may not contain values greater than nyquist\n')
	elif sampling_rate:
		nyquist = sampling_rate/2.0
		if sampling_rate/2.0 < max(freqs):
			raise Exception('\nfreqs may not contain values greater than sampling_rate/2\n')

	t, signal = get_signal(freqs, responses, nyquist, sampling_rate, duration, lb_type, ub_type, eps)
	signal = np.array(0.8*signal/max(abs(signal)), dtype='float32') # rescale signal so that its max is 80% of wav file limit
	write(outfile_path, sampling_rate, signal)
