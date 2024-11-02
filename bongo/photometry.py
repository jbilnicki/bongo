from scipy.signal import find_peaks
from scipy.integrate import simpson
from scipy.stats import zscore
from scipy.stats import mannwhitneyu
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pydoc


def open_file(path, n_cs=10):
    
    ''' function opens .csv file with photometry data
    and extracts necessary collumns
    
    path - path to a csv file
    n_cs (int, default=10) number of CS witch correspond to number of collumns we need
    
    return pandas DataFrame with selected values'''
    
    file = pd.read_csv(path, header=0)
    
    # we need only collumns with data for conditioned signal
    file = file.iloc[:, 1:n_cs+1]
    
    return file
    


def set_baseline(array, base_length=5, row_duration=50):
    ''' function for dividing array into baseline and values after treatment/event
    
    array - array-like object with data from specigic event
    base_length - float number of seconds prioror to our event that will be counted as a baseline
    row_duration (int default=50) what is difference in time from one row to the other (in miliseconds)
    
    return base - array with values for baseline, base_end - index of the last baseline value
    '''
    
    try: 
        array = np.array(array)
    except:
        raise TypeError("Can't convert your data to numpy.array")
        
    try:
        float(row_duration)
    except:
        raise TypeError("Invalid input - row_duration should be int")
        
    # calculating how many rows contains data with baseline values
    # each row is row_duration miliseconds so * 1000
    # first row is collumn name
    base_end = base_length/row_duration*1000
    base_end = int(base_end)
    base = array[1:base_end]
    
    return base, base_end
    
    
def normalize_peak(array, base_length=5, row_duration=50, event_length=6):
    
    ''' function for assesing percentage of change in fluorescence during some event
    
    array - array-like object with data from specigic event
    base_length - float number of seconds prioror to our event that will be counted as a baseline
    row_duration (int default=50) what is difference in time from one row to the other (in miliseconds)
    event_length (float default=5) number of seconds after the baseline
    for which maximal peak will be found
    
    then function plots results
    
    return normalised_peak - value of fluorescence in a maximal peak normalised to the baseline
    '''
    
    base, base_end = set_baseline(array, base_length, row_duration)
    
    # event for area under curve starts after baseline and lasts for a givent period
    event_duration = event_length/row_duration*1000
    event_duration = int(event_duration)
    
    # index of the last value counted as event
    event_end = base_end + event_duration
    
    event = array[base_end:event_end]
    
    # find peaks during our event
    peaks,_ = find_peaks(event)
    
    # maximal peak
    #max_peak = max(event[peaks])
    max_peak = max(event)
    max_peak_index = np.where(event==max_peak)
    
    normalised_peak = max_peak/np.mean(base)
    
    # correction for negative baseline
    if np.mean(base) < 0:
        normalised_peak *= -1
    
    # plot results
    
    # event x axis should start after baseline 
    # so we need to add number to a axis
    event_x = range(len(event))
    event_x = np.array(event_x)
    event_x += base_end
    
    plt.plot(array, color='orange')
    plt.plot(base, color='blue')
    plt.plot(event_x, event, color='red')
    plt.scatter(max_peak_index[0][0]+base_end, max_peak, color='green')
    
    return normalised_peak
    

def normalize_auc(array, base_length=5, row_duration=50, event_length=5):
    
    ''' function calculates area under curve for peak in fluorescence and normalize it to the background
    
    array - array-like object with fluorescence data
    base_length - float number of seconds prioror to our event that will be counted as a baseline
    row_duration (int default=50) what is difference in time from one row to the other (in miliseconds)
    event_length (float default=5) number of seconds after the baseline
    for which area under the curve will be calculated
    
    then function plots results
    
    return event_auc - float value of area under curve for given by event_length period, 
    standarized_auc - float value of area under curve for given by event_length period 
    normalized with baseline mean value
    '''
    
    base, base_end = set_baseline(array, base_length, row_duration)
    
    # event for area under curve starts after baseline and lasts for a givent period
    event_duration = event_length/row_duration*1000
    event_duration = int(event_duration)
    
    # index of the last value counted as event
    event_end = base_end + event_duration
    
    event = array[base_end:event_end]
    
    # drop nan values for simpson algorithm to work properly
    event = event[~np.isnan(event)]
    
    
    x = range(0,len(event))
    x = np.array(x)
    x += base_end
    
    # area under the curve for event and for baseline
    event_auc = simpson(event)
    base_auc = simpson(base)
    
    # normalization
    normalized_auc = event_auc/base_auc
    
    
    # plot results
    plt.plot(array, color='orange', label='other data')
    plt.plot(base, color='blue', label='baseline')
    plt.plot(x, event, color='red', label='event')
    plt.legend()
    
    
    return event_auc, normalized_auc

def calculate_z_score(array):
    
    ''' function that uses scipy.stats zscore to calculte array of z-score for 
    our photometry data
    
    array - array-like with fluorescence data
    
    return z_array - array-like with standarized values'''


    try: 
        array = np.array(array)
    except:
        raise TypeError("Can't convert your data to numpy.array")
        
    
    # drop nan values for z score calculating algorithm to work properly
    array = array[~np.isnan(array)]
    z_array = zscore(array)
    
    return z_array

#pydoc.writedoc("photometry")