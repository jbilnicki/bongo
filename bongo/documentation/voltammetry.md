  
# **voltammetry**



## -*- coding: utf-8 -*-

  
**Modules**

[numpy](https://numpy.org/doc/stable/)   

[pandas](https://pandas.pydata.org/docs/)  

[matplotlib.pyplot](https://matplotlib.org/stable/tutorials/pyplot.html)    

[pydoc](https://docs.python.org/3/library/pydoc.html)  

[seaborn](https://seaborn.pydata.org/)  

---

  
**Functions**

**analyze_transients**(array, diff_from_noise=2, window=10, order=3)

Function check number and amplitude of dopamine transients  
  
array - object storing current values from voltammetry (current vs time)  
diff_from_noise (float, default=2) minimal diffrence in amplidude between noise and  
event, events with amplidute greater than difference will be counted  
as transients (default=2)  
window (int, default=10) length of window for smoothing  
with savitzky-golay filter  
order (int, default=3) order of fitted polynominal  
  
Function performs data smoothing for better performance.  
Then finds peaks using numpy.find_peaks() function.  
analyze_transients also fitts a polynominal to array and calculates  
standard deviation to estimate noise level.  
Finally function checks which peak has amplitude significantly greater  
than background noise.  
  
analyze_transients draws plot to show which events were counted as transients.  
  
return list of indices from array corresponding to  
events counted as transients  
and smoothed array

**calculate_background_subtraction**(file, bg=0)

Subtracts background (default: first row) from all rows in DataFrame

**calculate_moving_average**(array, window_size=5)

Calculates rolling moving average for reducing noise

**calculate_sdbr**(file, bg=0)

Combines background subtraction second derivative calculation  
and moving average to perform SDBR on voltamperometric data.  
file - pd.DataFrame with voltammetric data  
bg (int) number of column in file which will be used to background subtraction  
default = 0

**draw_ct_plot**(transposed_file, volt, tonic)

Function takes transposed file for creating plot current vs time  
  
volt (int) argument specifies which row of the DataFrame choose,  
It should be integer from 0 to 849 as it describes index of a row  
that corresponds to our desired voltage value'  
and tonic (boolean) informs if user wants to create plot with row data or after SDBR  
returns data as a DataFrame

**draw_cv_plot**(transposed_file, time, tonic)

Function takes transposed file for creating plot current vs voltage  
  
transposed_file - pd.DataFrame  
time (int) argument specifies which column of the DataFrame choose,  
there are 10 voltammograms for each second - and each column stores one voltammogram  
and tonic (boolean) informs if user wants to create plot with row data or after SDBR

**draw_heatmap**(transposed_file)

Creates colorplot - heatmap for whole voltamperometric dataset,  
using seaborn and matplotlib.pyplot  
  
Takes transposed file so that time is on x axis and voltage on y axis

**open_data**(path)

function reads data from excel or csv file and creates pd.DataFrame.  
path (string)

**sdbr**(current, voltage)

function reduces noise  
and calculates second derivative using savitzky-golay filter  
takes two arguments: current i voltage
