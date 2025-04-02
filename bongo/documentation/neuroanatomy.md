
  
# **neuroanatomy**


## -*- coding: utf-8 -*-

  
**Modules**

[cv2](https://pypi.org/project/opencv-python/)  

[pydoc](https://docs.python.org/3/library/pydoc.html)  


---

### **Functions**

**check_NAc**(tissue_image, ap_cor=1.2, hemisphere='right')

Function to add mask from stereotactic atlas to tissue image from  
nucleus accumbens to check whether roi is in core or shell of this nucleus  
  
tissue_image (string) path to our image  
ap_cor (float) anterior-posterior disatnce in mm from bregma to our ROI  
default = 1.2 specifies which mask program should use  
hemisphere (string) 'right' or 'left' default = 'right' mask images are  
from right orientation so if image is from left hemisphere program flips mask

**check_VTA**(tissue_image, ap_cor=5.2, hemisphere='right')

Function to add mask from stereotactic atlas to tissue image  
and check if our ROI is in ventral tegmental area or in substantia nigra  
  
tissue_image (string) path to our image  
ap_cor (float) anterior-posterior disatnce in mm from bregma to our ROI  
default = 5.2 specifies which mask program should use  
hemisphere (string) 'right' or 'left' default = 'right' mask images are  
from right orientation so if image is from left hemisphere program flips mask

**check_structure**(tissue_image, max_anterior, max_posterior, ap_cor, hemisphere='right')

Function to add mask from stereotactic atlas to brain tissue image  
to check in which subregion is the ROI  
  
tissue_image (string) path to our image  
ap_cor (float) anterior-posterior disatnce in mm from bregma to our ROI  
specifies which mask program should use  
hemisphere (string) 'right' or 'left' default = 'right' mask images are  
from right orientation so if image is from left hemisphere program flips mask

**manual_superimpose**(img1_path, img2_path, direction='right')

Function to superimposing image of stereotactic atlas on microscope image of tissue  
  
function opens two image files and opens window in which user can manually adjust superimposing  
  
img1, img2 - paths to images that should be opened  
direction (string) 'right' or 'left' default 'right' if left flips the second image
