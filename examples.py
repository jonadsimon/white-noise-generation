'''
Demonstration of generate_white_noise.py
In all cases we assume a sampling rate of 16kHz and a duration of 10sec (default)
'''

from generate_white_noise import generate_white_noise

# Flat frequency response across entire 0Hz-8000Hz sprectrum
generate_white_noise('Examples/uniform_0Hz-8000Hz.wav', [4000], [1], nyquist=8000, lb_type='flat', ub_type='flat')

# Flat frequency response from 2000Hz-6000Hz, 0 elsewhere
generate_white_noise('Examples/uniform_2000Hz-6000Hz_zero_boundary.wav', [2000,6000], [1,1], nyquist=8000, lb_type='zero', ub_type='zero')

# Flat frequency response from 2000Hz-6000Hz, linearly decreasing outside this range
generate_white_noise('Examples/uniform_2000Hz-6000Hz_linear_boundary.wav', [2000,6000], [1,1], nyquist=8000, lb_type='linear', ub_type='linear')

# Triangular frequency response across entire 0Hz-8000Hz spectrum (peak at 4000Hz)
generate_white_noise('Examples/triangular_0Hz-8000Hz.wav', [4000], [1], nyquist=8000, lb_type='linear', ub_type='linear')

# Triangular frequency response from 2000Hz-6000Hz (peak at 4000Hz), 0 elsewhere
generate_white_noise('Examples/triangular_2000Hz-6000Hz_zero_boundary.wav.wav', [2000,4000,6000], [0,1,0], nyquist=8000)

# Linearly decreasing frequency response across entire 0Hz-8000Hz spectrum
generate_white_noise('Examples/decreasing_0Hz-8000Hz.wav', [0], [1], nyquist=8000, ub_type='linear')

# Linearly decreasing frequency response from 2000Hz-8000Hz, 0 elsewhere
generate_white_noise('Examples/decreasing_2000Hz-8000Hz_zero_boundary.wav', [2000], [1], nyquist=8000, lb_type='zero', ub_type='linear')

# Impulse response at 4000Hz
generate_white_noise('Examples/impulse_4000Hz.wav', [4000], [1], nyquist=8000, lb_type='zero', ub_type='zero')