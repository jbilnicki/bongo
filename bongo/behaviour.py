# -*- coding: utf-8 -*-

import cv2
import pandas as pd
import pydoc
import matplotlib.pyplot as plt

class Detector():
    ''' Class implementing openCV to track 2 animals in the same time'''
    
    def __init__(self, path, roi, animal_colour='dark', min_perimeter=120):
        '''path (string) path to a viedofile,
        animal_colour (string) "light" or "dark"
        is important during binarisation, so that object (an animal) is white
        and the background is black, default "dark"
        roi (list with four elements) stores coordinates for selecting part 
        of the image
        min_perimeter (int) objects smaller than that will not be conssidered as an animal,
        default 120'''
        
        self.path = path
        detections = {}
        self.detections = detections
        self.animal = animal_colour
        self.roi = roi
        self.min_perimeter = min_perimeter

        
    def detect(self):
        '''Main function of the class that serves as engine for tracking system'''
        
        cap = cv2.VideoCapture(self.path)

        '''
        for i in range(no_of_animals):
            self.detections[f'animal{i}_x'] = []
            self.detections[f'animal{i}_y'] = []
        '''
        self.detections['animal_x'] = []
        self.detections['animal_y'] = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
        
            if len(self.roi) != 4:
                raise ValueError(f"ROI list should have 4 elements, but {len(self.roi)} were given")                
        
            roi_img = frame[self.roi[0]:self.roi[1], self.roi[2]:self.roi[3]]
            
            height, width, _ = roi_img.shape
            
            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
            
            try:
                if self.animal == "light":
                    _, mask = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY)
                    
                elif self.animal == "dark":
                    _, mask = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY_INV)
            except:
                raise ValueError("animal_colour must be string, either 'light' or 'dark'.")
                
            contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
                    
            for contour in contours:
                #area = cv2.contourArea(contour)
                # cloesd figure - True, just a curve - False
                #perimeter = cv2.arcLength(contour,False)
                perimeter2 = cv2.arcLength(contour,True)
                #if perimeter > 200 or perimeter2 >150:
                if perimeter2 > self.min_perimeter:
                   
                    # calculate moments for each contour
                    M = cv2.moments(contour)
                    # calculate x, y coordinate of center
                    if M["m00"] != 0: cX, cY = int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"])
                    else: cX, cY = 0, 0
                    # draw the contour and centroid on the image
                    #cv2.drawContours(frame, [contour], -1, (0,255,0), 1)
                    #cv2.circle(frame, (cX,cY), 3, (0,0,255), -1)
                    cv2.circle(roi_img, (cX,cY), 3, (0,0,255), -1)
                    
        
                    #detections[iteration].append([cX,cY])
                    try:self.detections[f"animal_x"].append(cX), self.detections[f'animal_y'].append(cY)
                    except: pass
            
            cv2.imshow("ROI", roi_img)
            
        
            key = cv2.waitKey(30)
            if key == ord("q"):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        #return detections_df, height, width
        return self.detections, height, width

       
    # data saving
    def get_detections(self):
        ''' function that stores data about tracked animals in pd.DataFrame'''
        
        detections, height, width = self.detect()
        detections_df = pd.DataFrame.from_dict(detections, orient='index')
        detections_df = detections_df.transpose()
        #detections_df = pd.DataFrame(detections)
        return detections_df, height, width
        
        
    def plot_results(self, detections_df, height, width):
        """ Function uses matplotlib.pyplot to display trajectory of the animal
            detections_df - pd.DataFrame with coordinates of the animal's centroid
            height, width - int,  size of the frame from video, plot will be scaled
            in a proper manner
        """
        
        
    
        # coordinates of the  animal
        x_0 = detections_df["animal_x"]
        y_0 = detections_df["animal_y"]
        
        
        plt.figure()
        plt.plot(x_0,y_0)
        
        plt.xlim(0,width)
        plt.ylim(0,height)
        plt.gca().invert_yaxis()
        
pydoc.writedoc("behaviour")
