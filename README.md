# white-noise-generation

##### Inputs/parameters:

* infile_name: comma-separated frequency/amplitude values (DECIBELS?)
* outfile_name: name of output WAV file
* ~~interpolation_type: linear or cubic spline~~
* nyquist_frequency: either maximum input frequency, or provided frequency
* sampling_rate: 2x nyquist frequency; either of the two parameters can be given, but not both
* duration: duration of white noise
* lower_bound_interpolation: zero, flat, or linear ~~, or spline (?)~~
* upper_bound_interpolation: zero, flat, or linear ~~, or spline (?)~~

##### Outputs:

* WAV file containing desired white noise
