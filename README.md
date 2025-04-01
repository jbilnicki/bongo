# bongo "Bongo Offers Neuroscientific Graphs and Outputs" is a python package for analysis of  basic neuroscientific data.

![logo](./logo.ico)  

Author: Jakub Bilnicki  
Version: 1.2  
Language: Python 3.11.7  
It is based mainly on: Pandas, NumPy, matplotlib.pyplot, openCV, seaborn 

---

bongo contains submodules for: 
  - behaviour,
  - neuroanatomy, 
  - cells counting 
  - fast-scan cyclic voltammetry
  - fiber photometry

---

**Acknowledgments:**   
bongo.neuroanatomy uses images from "The Rat Brain in Stereotactic Coordinates" 5th Edition (2004) by George Paxinos and Charles Watson 
coordinates from bregma can be accesed from files' names.

**How to use:**
In bongo subdirectory there is a file example.py with some usefull code snippts.  
For behavioural data there is also self_administration_analysis.py file with GUI

**Currenly:**    
behaviour contains class Detector for simple tracking animal movements e.g. in open field paradigm  
and Med_PC_Data_Extractor for analysis of self-administration experiments;

cells has one function for counting cells on microscope image;

voltammetry enables user to open files with FSCV data, visualise colorplot, current vs time, current vs voltage plots
and perform operations like: background subtraction, smoothening data with moving average and calculating second derivative for each voltammogram

neuroanatomy.py contains funtions for superimposing images from sterotactic brain atlas (see Acknowledgments section)  
onto microscope images in order to validate placement of electrodes/optodes etc. There is already directory with images of nucleus accumbens and ventral tegmental area;  

photometry has functions for finding maximal peak in fluorescence and calculating area under the curve.

---

Future collaboration may involve expanding range of available brain structures for neuroanatomy.py, adding new features to  behaviour.py like better tracking algorithms, ultasonic vocalisation analysis tools. 
