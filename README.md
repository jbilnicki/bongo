# bongo "Bongo Offers Neuroscientific Graphs and Outputs" is a python module for analysis of  basic neuroscientific data.
It is based mainly on: Pandas, NumPy, matplotlib.pyplot, openCV, seaborn 

bongo contains submodules for: behaviour, neuroanatomy, cells and fast-scan cyclic voltammetry

bongo is still under development.
Currenly:
behaviour contains class Detector for simple tracking animal movements e.g. in open field paradigm;
cells has one function for counting cells on microscope image;
voltammetry enables user to open files with FSCV data, visualise colorplot, current vs time, current vs voltage plots
and perform operations like: background subtraction, smoothening data with moving average and calculating second derivative for each voltammogram

neuroanatomy.py contains funtions for superimposing images from sterotactic brain atlas onto microscope images in order to validate placement of electrodes/optodes etc. This submodule is not finished yet. There will be also uploded directory with sample atlas masks for nucelus accumbens and ventral tegmental area. 

Future collaboration may involve expanding range of available brain structures for neuroanatomy.py, adding new features to  behaviour.py like better tracking algorithms, ultasonic vocalisation analysis tools. 
