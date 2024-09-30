# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt
import numpy as np 
import seaborn as sns
import pandas as pd
from scipy.signal import savgol_filter
#from scipy.signal import argrelextrema
from scipy.signal import find_peaks
import pydoc


def open_data(path):
    ''' function reads data from excel or csv file and creates pd.DataFrame.
    path (string)'''
    
    if path.endswith(".xlsx"):
        file = pd.read_excel(path, header=None, engine='openpyxl')
        
    elif path.endswith(".csv") or path.endswith(".txt"):
        file = pd.read_csv(path, sep="\t", header=None)
        file = file.T
        
    return file
        
    
def calculate_background_subtraction(file, bg=0):
    ''' Subtracts background (default: first row) from all rows in DataFrame'''
    
    bs = file.apply(lambda row: row-file.iloc[bg], axis=1)
    return bs

def sdbr(current, voltage):
    ''' function reduces noise 
    and calculates second derivative using savitzky-golay filter
    takes two arguments: current i voltage'''
    
    window_length = 50
    polyorder = 3
    deriv = 2
    
    sd = savgol_filter(x=current, window_length=window_length, polyorder=polyorder, deriv=deriv)
    
    # multiply every value by -1 to change direction of change in dataset
    
    sd *= -1
    
    return sd


def calculate_moving_average(array,window_size=5):
    '''Calculates rolling moving average for reducing noise'''
    
    array = pd.Series(array)
     
    # Get the window of series
    # of observations of specified window size
    windows = array.rolling(window_size)
     
    # Create a series of moving
    # averages of each window
    moving_averages = windows.mean()
    
    # Convert pandas series back to list
    #moving_averages_list = moving_averages.tolist()
    return moving_averages.tolist()
    
def calculate_sdbr(file, bg=0):
    ''' Combines background subtraction second derivative calculation
    and moving average to perform SDBR on voltamperometric data.
    file - pd.DataFrame with voltammetric data
    bg (int) number of column in file which will be used to background subtraction
    default = 0
    '''
    
    voltage = pd.read_csv("voltage.csv")
    voltage = voltage.iloc[:,0]
    file = file.astype(float)
    
    # background subtraction
    
    file = calculate_background_subtraction(file,bg)
    file = file.interpolate()
    
    window = 50
    #polyorder = 4 
    #deriv = 0
    
    # calculate second derivative for each row of the file
    derivatives = file.apply(lambda row: sdbr(row.values, voltage), axis=1)
    
    derivatives_df = pd.DataFrame(derivatives.tolist(), index=file.index)
    
    #for better signal to noise ratio we will apply moving average
    moving_averages = derivatives_df.apply(lambda row: calculate_moving_average(row.values,window), axis=1)
    derivatives_df = pd.DataFrame(moving_averages.tolist(), index=derivatives_df.index)
    return derivatives_df
    
def draw_heatmap(transposed_file):
    ''' Creates colorplot - heatmap for whole voltamperometric dataset,
    using seaborn and matplotlib.pyplot
    
    Takes transposed file so that time is on x axis and voltage on y axis'''
    
    # checking if DataFrame is transposed in a proper manner
    if transposed_file.shape[1] == 850:
        transposed_file = transposed_file.T
    
    color = sns.color_palette("viridis", as_cmap=True)
    ax = sns.heatmap(transposed_file, yticklabels=50, cmap=color)
    ax.set_title('colorplot')
    y = ["0","50","100","150","200","250","300","350","400","450","500","550","600", "650","700","750","800"]
    ax.set_yticklabels(y, rotation=0)
    ax.set_ylabel(ylabel='')
    
    if transposed_file.shape[1] > 1200:
        rg = range(0,transposed_file.shape[1],1200)
        ax.set_xticks(rg)
        labels=[]
        for i in range(len(rg)):
            # so that it displays less numbers on the acis
            labels.append(i*2)
        ax.set_xticklabels(labels,rotation=0)   
        
        plt.xlabel('time (min)')
    else:
        ax.set_xticks(range(0,transposed_file.shape[1],10))
        # must be int because after division is float and it cause an error
        ax.set_xticklabels(range(0,int(transposed_file.shape[1]/10)))
        plt.xlabel('time (s)')
    
    ax.invert_yaxis()
    #plt.show()
    
    
def draw_ct_plot(transposed_file, volt, tonic):
    ''' Function takes transposed file for creating plot current vs time
    
    volt (int) argument specifies which row of the DataFrame choose,
    and tonic (boolean) informs if user wants to create plot with row data or after SDBR
    returns  data as a DataFrame'''

    # checking if DataFrame is transposed in a proper manner
    if transposed_file.shape[1] == 850:
        transposed_file = transposed_file.T
        
    y2 = transposed_file.iloc[volt]
    x2 = range(0,transposed_file.shape[1])
    
    ct_dict = {'time':x2,'current':y2}
    ct_pd = pd.DataFrame(ct_dict)
    #ct_pd.to_excel('ct.xlsx',)
    if transposed_file.shape[1] < 1200:
        # 10 datapoints for each second, so we must divide
        # in order to display seconds on x axis
        x2 = pd.Series(x2)/10
        unit = "time (s)"
    else:
        x2 = pd.Series(x2)/600
        unit = "time (min)"
        
        
    c_time = plt.plot(x2,y2)
    plt.title("current vs time")
    if tonic:
        plt.ylabel("second derivative current")
    else:
        plt.ylabel("current (nA)")
    plt.xlabel(unit)
    
    return ct_pd
    
    
    
def draw_cv_plot(transposed_file, time, tonic):
    ''' Function takes transposed file for creating plot current vs voltage
    
    transposed_file - pd.DataFrame
    time (int) argument specifies which column of the DataFrame choose,
    and tonic (boolean) informs if user wants to create plot with row data or after SDBR'''

    # checking if DataFrame is transposed in a proper manner
    if transposed_file.shape[1] == 850:
        transposed_file = transposed_file.T

    y3 = transposed_file[transposed_file.columns[time]]

    # half of voltage data is for oxydation
    # the rest for reduction
    # data on different lines of the plot
    y4 = y3.tolist()
    y4 = y4[:424]
    x4 = range(0,424)
    
    c_v = plt.plot(x4,y4)
    
    # reduction
    y5 = y3.tolist()
    y5 = y5[426:]
    # reverse because voltage values now decrease
    y5 = list(reversed(y5))
    c_v = plt.plot(x4,y5,color='#1f77b4')
    
    ticks = [0,25,50,75,100,125,150,175,200,225,250,275,300,325,350,375,400,425]
    
    voltage = pd.read_csv("voltage.csv")
    #print(voltage.head())
    voltage = voltage.iloc[:,0]
    
    voltage_index = pd.Series(voltage)
    voltage_index = voltage_index.unique()
    
    plt.xticks(ticks=ticks,labels=voltage_index)
    plt.title("current vs voltage")
    if tonic:
        plt.ylabel("second derivative current")
    else:
        plt.ylabel("current (nA)")
    plt.xlabel("voltage (V)")



def analyze_transients(array, diff_from_noise=2):
    '''Function check number and amplitude of dopamine transients
        
        array - object storing current values from voltammetry (current vs time)
        diff_from_noise (float, default=2) minimal diffrence in amplidude between noise and
        event, events with amplidute greater than difference will be counted
        as transients (default=2)
        
        Function performs data smoothing for better performance.
        Then finds peaks using numpy.find_peaks() function.
        analyze_transients also fitts a polynominal to array and calculates
        standard deviation to estimate noise level.
        Finally function checks which peak has amplitude significantly greater
        than background noise.
        
        analyze_transients draws plot to show which events were counted as transients.
        
        return list of indices from array corresponding to 
        events counted as transients 
    '''
    
    try: 
        array = np.array(array)
    except:
        raise TypeError("Can't convert your data to numpy.array")
        
    try:
        float(diff_from_noise)
    except:
        raise TypeError("Invalid input - diff_from_noise should be float (or int)")
        
    
    
   
    
    # smoothing
    array = savgol_filter(array, window_length=10, polyorder=5)
    #array = calculate_moving_average(array)
    #array = np.array(array)
    
    # find peaks in our array
    peaks,_ = find_peaks(array)
    
    
    # x axis
    x = range(0,len(array),1)
    x = np.array(x)
    
    
    # Fit a 3rd-degree polynomial
    coefficients = np.polyfit(x, array, 3)
    fitted_values = np.polyval(coefficients, x)
    
    # Calculate residuals and standard deviation for assesing noise
    residuals = array - fitted_values
    std_dev = np.std(residuals)
    
    # threshold above which peaks will be counted as transients
    threshold = diff_from_noise * std_dev
    
    transients = []
    
    for peak in peaks:
        
        if array[peak] >= (fitted_values[peak] + threshold):
            transients.append(peak)
    
    
    # Plotting
    plt.plot(x, array, label='Data')
    #plt.scatter(peaks, array[peaks], label='Peaks', color='green')
    plt.scatter(transients, array[transients], label='Transients', color='red')
    plt.legend()
    plt.show()
    
    return transients
    
    
    
    
pydoc.writedoc("voltammetry")