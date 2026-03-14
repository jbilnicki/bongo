import pytest
import numpy as np
import re
import sys
# in order to access files in parent directory
sys.path.append('../')
from voltammetry import analyze_transients

def test_valid_input(): 
    large_array = np.random.normal(0,1,1000) 
    large_array[51] = 200 
    large_array[280] = 200 
    large_array[780] = 200
   	# indices in array that have peak values 
    expected_result = [51,280,780] 
    transients, smoothed_array = analyze_transients(large_array)
    # sometimes due to smoothing peaks are shifted by 1 in relation to original array
    check = np.isclose(transients, expected_result, atol=1) 
    # check if all elements in check are True
    assert  np.all(check), 'Expected transients do not match.'

def test_invalid_input():
	invalid_input = ["some", 23, "wrong", None, "data"]
	with pytest.raises(TypeError, match=re.escape("Can't convert your data to numpy.array")):
		analyze_transients(invalid_input)


def test_invalid_diff_from_noise():
	with pytest.raises(TypeError, match=re.escape("Invalid input - diff_from_noise should be float (or int)")):
		analyze_transients([1,2,3], diff_from_noise="2a")

def test_large_input():
	large_array = np.random.normal(0,1,10000)
	transients, smoothed_array = analyze_transients(large_array, diff_from_noise=5, window=11, order=3)

	assert isinstance(transients, list)
	assert len(transients) == 0, "No transients should be found in normally distributed noise."

def test_smoothing_effect():
    array = np.random.normal(0,1,100)
    transients, smoothed_array = analyze_transients(array) 
    assert not np.array_equal(smoothed_array, array), "Smoothing did not change the array."

