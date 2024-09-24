# -*- coding: utf-8 -*-

import cv2

def manual_superimpose(img1_path, img2_path, direction='right'):
    
    ''' Function to superimposing image of stereotactic atlas on microscope image of tissue

        function opens two image files and opens window in which user can manually adjust superimposing 

        img1, img2 - paths to images that should be opened
        direction (string) 'right' or 'left' default 'right' if left flips the second image
    '''
    
    
    # Load images
    base_img = cv2.imread(img1_path)
    super_img = cv2.imread(img2_path)
    
    if direction == 'left':
        super_img = cv2.flip(super_img, 1)
        

    if base_img is None:
        print(f"Error: Unable to load image at {img1_path}")
        return
    if super_img is None:
        print(f"Error: Unable to load image at {img2_path}")
        return

    # Ensure both images have the same number of channels
    if len(base_img.shape) != len(super_img.shape):
        if len(base_img.shape) == 2:
            base_img = cv2.cvtColor(base_img, cv2.COLOR_GRAY2BGR)
        if len(super_img.shape) == 2:
            super_img = cv2.cvtColor(super_img, cv2.COLOR_GRAY2BGR)

    # Create a window to display the images
    cv2.namedWindow('Superimpose', cv2.WINDOW_NORMAL)



    # Function to update the superimposed image based on trackbar positions
    def update_superimpose(x):
        #alpha = cv2.getTrackbarPos('Transparency', 'Superimpose') / 100
        alpha=0.3
        scale = cv2.getTrackbarPos('Scale', 'Superimpose') / 100

        # Resize the superimposed image
        new_size = (int(super_img.shape[1] * scale), int(super_img.shape[0] * scale))
        super_img_resized = cv2.resize(super_img, new_size)

        # Create a blank image with the same size as the base image
        combined_img = base_img.copy()

        # Calculate the position to place the resized image
        x_offset = cv2.getTrackbarPos('X Position', 'Superimpose')
        y_offset = cv2.getTrackbarPos('Y Position', 'Superimpose')

        # Ensure the position is within bounds
        x_offset = min(max(0, x_offset), base_img.shape[1] - new_size[0])
        y_offset = min(max(0, y_offset), base_img.shape[0] - new_size[1])

        # Overlay the resized image on the base image
        combined_img[y_offset:y_offset+new_size[1], x_offset:x_offset+new_size[0]] = cv2.addWeighted(
            combined_img[y_offset:y_offset+new_size[1], x_offset:x_offset+new_size[0]],
            1 - alpha,
            super_img_resized,
            alpha,
            0
        )

        cv2.imshow('Superimpose', combined_img)

    # Create trackbars to adjust the transparency, scale, and position of the superimposed image
    #cv2.createTrackbar('Transparency', 'Superimpose', 50, 100, update_superimpose)
    cv2.createTrackbar('Scale', 'Superimpose', 100, 200, update_superimpose)
    cv2.createTrackbar('X Position', 'Superimpose', 0, base_img.shape[1], update_superimpose)
    cv2.createTrackbar('Y Position', 'Superimpose', 0, base_img.shape[0], update_superimpose)

    # Initial display
    update_superimpose(0)

    # Wait until a key is pressed
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def check_structure(tissue_image, max_anterior, max_posterior, ap_cor, hemisphere='right'):
    
    ''' Function to add mask from stereotactic atlas to brain tissue image
        to check in which subregion is the ROI
        
        tissue_image (string) path to our image
        ap_cor (float) anterior-posterior disatnce in mm from bregma to our ROI
        specifies which mask program should use
        hemisphere (string) 'right' or 'left' default = 'right' mask images are 
        from right orientation so if image is from left hemisphere program flips mask
    '''
    
    
    try:
        float(ap_cor)
        mask_img = f'img/slice_{ap_cor}.png'
    except:
        raise TypeError("Inapropriate ap_core inupt: should be float")
        
    
    if ap_cor < 2.0 and ap_cor > 0.9:
        manual_superimpose(tissue_image, mask_img, hemisphere)
        
    else:
        raise ValueError("Sorry provided coordinate is not available")
        
    
    
def check_NAc(tissue_image, ap_cor=1.2, hemisphere='right'):
    ''' Function to add mask from stereotactic atlas to tissue image from
        nucleus accumbens to check whether roi is in core or shell of this nucleus
        
        tissue_image (string) path to our image
        ap_cor (float) anterior-posterior disatnce in mm from bregma to our ROI
        default = 1.2 specifies which mask program should use
        hemisphere (string) 'right' or 'left' default = 'right' mask images are 
        from right orientation so if image is from left hemisphere program flips mask
    '''
    
    # range of available coordinates from sterotactic atlas 
    max_anterior = 2.0
    max_posterior = 0.9
    
    check_structure(tissue_image, max_anterior, max_posterior, ap_cor, hemisphere)
    
    
    
def check_VTA(tissue_image, ap_cor=5.2, hemisphere='right'):
    ''' Function to add mask from stereotactic atlas to tissue image 
        and check if our ROI is in ventral tegmental area or in substantia nigra
        
        tissue_image (string) path to our image
        ap_cor (float) anterior-posterior disatnce in mm from bregma to our ROI
        default = 5.2 specifies which mask program should use
        hemisphere (string) 'right' or 'left' default = 'right' mask images are 
        from right orientation so if image is from left hemisphere program flips mask
    '''
    
    # range of available coordinates from sterotactic atlas 
    max_anterior = 4.8
    max_posterior = 6.0
    
    check_structure(tissue_image, max_anterior, max_posterior, ap_cor, hemisphere)
    