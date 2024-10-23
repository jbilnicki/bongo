from scipy.signal import find_peaks
from scipy.integrate import simpson
from scipy.stats import mannwhitneyu
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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
    



def normalize_peak(array, base_length=5, row_duration=50):
    
    ''' function for assesing percentage of change in fluorescence during some event
    
    array - array-like object with data from specigic event
    base_length - float number of seconds prioror to our event that will be counted as a baseline
    row_duration (int default=50) what is difference in time from one row to the other (in miliseconds)
    
    then function plots results
    
    return normalised_peak - value of fluorescence in a maximal peak normalised to the baseline
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
    
    event = array[base_end:]
    
    # find peaks during our event
    peaks,_ = find_peaks(event)
    
    # maximal peak
    #max_peak = max(event[peaks])
    max_peak = max(event)
    max_peak_index = np.where(event==max_peak)
    
    normalised_peak = max_peak/np.mean(base)*100
    
    # correction for negative baseline
    if np.mean(base) < 0:
        normalised_peak *= -1
    
    # plot results
    
    # event x axis should start after baseline 
    # so we need to add number to a axis
    event_x = range(len(event))
    event_x = np.array(event_x)
    event_x += base_end
    
    plt.plot(base, color='blue')
    plt.plot(event_x, event, color='orange')
    plt.scatter(max_peak_index[0][0]+base_end, max_peak, color='red')
    
    return normalised_peak
    

def normalize_auc(array):
    
    ''' function calculates area under curve for peak in fluorescence and normalize it to the background
    array - array-like object with fluorescence data'''
    
    try: 
        array = np.array(array)
    except:
        raise TypeError("Can't convert your data to numpy.array")
    
    # drop nan values for simpson algorithm to work properly
    array = array[~np.isnan(array)]
    
    
    auc = simpson(array)
    
    return auc


file = open_file("~/Desktop/example.csv")

cs_1 = file["DeltaF/F-1"]

peak = normalize_peak(cs_1)

print(f'Normalized value of your peak is: {peak}')

auc = normalize_auc(cs_1)
print(auc)
