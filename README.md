# bongo "Bongo Offers Neuroscientific Graphs and Outputs" is a python module for analysis of  basic neuroscientific data.
Author: Jakub Bilnicki
Language: Python 3.11.7
It is based mainly on: Pandas, NumPy, matplotlib.pyplot, openCV, seaborn 

bongo contains submodules for: 
  -behaviour,
  -neuroanatomy, 
  -cells  
  -fast-scan cyclic voltammetry

Acknowledgments: bongo.neuroanatomy uses images from "The Rat Brain in Stereotactic Coordinates" 5th Edition by George Paxinos and Charles Watson 
coordinates from bregma can be accesed from files' names.


Warning: bongo is still under active development.
Currenly:
behaviour contains class Detector for simple tracking animal movements e.g. in open field paradigm;

cells has one function for counting cells on microscope image;

voltammetry enables user to open files with FSCV data, visualise colorplot, current vs time, current vs voltage plots
and perform operations like: background subtraction, smoothening data with moving average and calculating second derivative for each voltammogram

neuroanatomy.py contains funtions for superimposing images from sterotactic brain atlas onto microscope images in order to validate placement of electrodes/optodes etc. This submodule is not finished yet. There is already directory with images of nucleus accumbens but images for ventral tegmental area will be uploded soon.

Future collaboration may involve expanding range of available brain structures for neuroanatomy.py, adding new features to  behaviour.py like better tracking algorithms, ultasonic vocalisation analysis tools. 
