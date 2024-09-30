import cv2
import numpy as np

def count_cells(image, best_channel="green", threshold=200, min_size=50, display=True) -> int:
    ''' function binarizing microscope image and counting cells based on contrast
    
    input: image: path to image file, best_channel: str (red/r, green/g, blue/b - default "green")
    which channel from image should be used for further analysis
    threshold: int (default 200) pixel values above threshold will be changed to 255 (white), below set to 0 (black),
    min_size: int (default 50) objects with area less than min_size will not be recognized as cells
    display: boolean (default True) if true create windows with images for each step of analysis
    
    return int: number of cells counted on the image
    '''

    try:
        img = cv2.imread(image)
        copy_img = img.copy()
    except ValueError:
        raise ValueError("Can't open image. Not appropriate file path")


         ###### Use
    # enhancing contrast
    lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)
    
    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(l_channel)
    
    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl,a,b))
    
    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    ######## Or
    alpha = 1.5 # Contrast control (1.0-3.0)
    beta = 0 # Brightness control (0-100)
    
    adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    

    #######   or this one
    # Create the sharpening kernel 
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) 
      
    # Sharpen the image 
    sharpened_img = cv2.filter2D(img, -1, kernel) 
        
    # spliting image to 3 channels
    #blue, green, red = cv2.split(enhanced_img)
    blue, green, red = cv2.split(sharpened_img)
    #blue, green, red = cv2.split(adjusted)
    #blue, green, red = cv2.split(img)

    # choosing appropriate channel
    if best_channel == "red" or best_channel == "r":
        channel = red
    elif best_channel == "green" or best_channel == "g":
        channel = green
    elif best_channel == "blue" or best_channel == "b":
        channel = blue
    else:
        raise ValueError("Can't choose channel for further analysis, right input: 'red','r', 'green','g', 'blue','b'")

    # binarization of the image with threshold value
    try:
        int(threshold)
    except TypeError:
        raise TypeError("Threshold should be an integer")

    # check if threshold value does not exceed range 0-255 - maximal value for pixel
    if threshold >= 0 and threshold <= 255:
        #binary = cv2.Canny(channel, threshold, 255)
        _, binary = cv2.threshold(channel, threshold, 255, cv2.THRESH_BINARY)
        #binary = cv2.adaptiveThreshold(channel, threshold, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,5)
    else:
        raise ValueError("Threshold should be in range: 0-255")

    # find contours on image which are cells
    contours,_ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # variable counting cells
    n_cells = 0

    # checking area of contour, to get rid of small noise contours
    # which are not cells
    for contour in contours:
        area = cv2.contourArea(contour)
        # checking if min_size is int
        if isinstance(min_size, int):
            if area >= min_size:
                cv2.drawContours(copy_img, [contour], -1, (0,0,255), 1) 
                n_cells += 1
        else:
            raise TypeError("min_size must be integer.")

    # display results
    if display:
        cv2.imshow("Original", img)
        #cv2.imshow("High Contrast", enhanced_img)
        cv2.imshow("Sharpened", sharpened_img)
        #cv2.imshow("Adjusted", adjusted)
        cv2.imshow(f'{best_channel}', channel)
        cv2.imshow("Binary", binary)
        cv2.imshow("Mask", copy_img)

        
        cv2.waitKey(0) & 0xFF == ord("q")
        cv2.destroyAllWindows()

    # return number of cells
    return n_cells
