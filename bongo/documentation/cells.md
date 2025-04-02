# **cells**
  
## **Modules**

[cv2](https://pypi.org/project/opencv-python/)  

[numpy](https://numpy.org/doc/stable/)  

[pydoc](https://docs.python.org/3/library/pydoc.html)  

  
### **Functions**

**count_cells**(image, best_channel='green', threshold=200, min_size=50, display=True) -> int

function binarizing microscope image and counting cells based on contrast  
  
input: image: path to image file, best_channel: str (red/r, green/g, blue/b - default "green")  
which channel from image should be used for further analysis  
threshold: int (default 200) pixel values above threshold will be changed to 255 (white), below set to 0 (black),  
min_size: int (default 50) objects with area less than min_size will not be recognized as cells  
display: boolean (default True) if true create windows with images for each step of analysis  
  
return int: number of cells counted on the image