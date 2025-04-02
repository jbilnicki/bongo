
 
# photometry	

 
## Modules
      	 	
[numpy](https://numpy.org/doc/stable/)  

[pandas](https://pandas.pydata.org/docs/)  

[matplotlib.pyplot](https://matplotlib.org/stable/tutorials/pyplot.html)  

[pydoc](https://docs.python.org/3/library/pydoc.html)

---

### Functions
      	 	
**calculate_z_score**(array)  

function that uses scipy.stats zscore to calculte array of z-score for 
our photometry data
 
array - array-like with fluorescence data
 
return z_array - array-like with standarized values
normalize_auc(array, base_length=5, row_duration=50, event_length=5)
function calculates area under curve for peak in fluorescence and normalize it to the background
 
array - array-like object with fluorescence data
base_length - float number of seconds prioror to our event that will be counted as a baseline
row_duration (int default=50) what is difference in time from one row to the other (in miliseconds)
event_length (float default=5) number of seconds after the baseline
for which area under the curve will be calculated
 
then function plots results
 
return event_auc - float value of area under curve for given by event_length period, 
standarized_auc - float value of area under curve for given by event_length period 
normalized with baseline mean value  

**normalize_peak**(array, base_length=5, row_duration=50, event_length=6)  

function for assesing percentage of change in fluorescence during some event
 
array - array-like object with data from specigic event
base_length - float number of seconds prioror to our event that will be counted as a baseline
row_duration (int default=50) what is difference in time from one row to the other (in miliseconds)
event_length (float default=5) number of seconds after the baseline
for which maximal peak will be found
 
then function plots results
 
return normalised_peak - value of fluorescence in a maximal peak normalised to the baseline  

**open_file**(path, n_cs=10)  

function opens .csv file with photometry data
and extracts necessary collumns
 
path - path to a csv file
n_cs (int, default=10) number of CS witch correspond to number of collumns we need
 
return pandas DataFrame with selected values
set_baseline(array, base_length=5, row_duration=50)
function for dividing array into baseline and values after treatment/event
 
array - array-like object with data from specigic event
base_length - float number of seconds prioror to our event that will be counted as a baseline
row_duration (int default=50) what is difference in time from one row to the other (in miliseconds)
 
return base - array with values for baseline, base_end - index of the last baseline value
