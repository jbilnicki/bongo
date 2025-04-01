# -*- coding: utf-8 -*-

import cv2
import pandas as pd
import pydoc
import matplotlib.pyplot as plt
import re
from datetime import datetime, timedelta


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
 
class Med_PC_Data_Extractor():

    ''' 
    Class for extracting data about infusion number, active/inactive lever presses and time spent by rat in Skinner box
    class takes as a source file generated by Med-PC IV software 

    please be aware that this script is suited for very specific use case - analysis of lever presses in 6 hours oxycodone seeking rats.
    For analysis of different data changes in script (especially regular expressions) might be necessary
    '''
    
    def __init__(self, file):
        
        ''' file (string) - path to the file with raw data from MED-PC IV'''
        
        self.file = file

        # create new data frame for our data and take experiment date
        boxes = pd.DataFrame(columns=["Box", "Date", "Procedure", "Duration", "Duration [s]", "Duration [min]", "Infusions 1h", "Total infusions", "Total active", "Total inactive", "Total active time-out"])
        date = re.sub(r".*!","", file.readline())

        self.boxes = boxes
        self.date = date


    def time_to_seconds(self, time_str):
    
        ''' function takes time in format of h:min:s and converts it to value in seconds'''
        
        hours, minutes, seconds = map(int, time_str.split(':'))
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return total_seconds


    def find_sequence(self, content, index, column, st):
    
        '''find sequence starting from desired string and save it to proper row and column of DataFrame'''
        
        match = re.search(f"({st}:\s+)(\d+\.\d+)", content)
        match = re.sub(f"{st}:", "", match.group(0))
        self.boxes.loc[index,column] = match

    def extract_data(self, data):
    
        ''' function for extracting data from file in a proper manner'''
        
        content = self.file.read()
    
        # divide file to segments starting with "Box: " and ending with "Start Date" strings
        box_matches = re.findall(r"(Box:\s*(\d+).+?)(?=Start Date:|\Z)", content, re.DOTALL)
    
        # number of row to which insert data for each box
        index = 0
        # extract data for each box
        for box_match in box_matches:
    
            
            box_content = box_match[0].strip()
            # box number
            box_number = box_match[1]
            
            self.boxes.loc[index, "Box"] = box_number
            self.boxes.loc[index,"Date"] = self.date.rstrip()
    
            # extract start and end times
            start_time_match = re.search(r"Start Time:\s*(\d+:\d+:\d+)", box_content)
            end_time_match = re.search(r"End Time:\s*(\d+:\d+:\d+)", box_content)        
            
            
            if start_time_match:
                start_time = start_time_match.group(1)
            else:
                None
    
            if end_time_match:
                end_time = end_time_match.group(1)
            else:
                None
    
            
            # calculate time spent in cage
            time_spent_in_cage = None
            if start_time and end_time:
                try:
                    fmt = "%H:%M:%S"
                    start_dt = datetime.strptime(start_time, fmt)
                    end_dt = datetime.strptime(end_time, fmt)
                    if end_dt < start_dt:  # Handle overnight case
                        end_dt += timedelta(days=1)
                    time_spent_in_cage = end_dt - start_dt
                except Exception as e:
                    time_spent_in_cage = f"Error: {e}"
    
            # add info about time spend in experiments
            self.boxes.loc[index,"Duration"] = time_spent_in_cage
    
            # add info about time spend in experiments in seconds
            time_s = self.time_to_seconds(str(time_spent_in_cage))
            self.boxes.loc[index,"Duration [s]"] = time_s
    
            # add info about time spend in experiments in minutes
            time_min = time_s/60
            self.boxes.loc[index,"Duration [min]"] = time_min

            # info about behavioural procedure
            procedure = re.search(r"(?<=MSN:\s)(.*?)(?=\sA:)", box_content)
            # extracting only the procedure name
            self.boxes.loc[index, "Procedure"] = procedure.group(1)
    
            # how the brightest minds that designed original program
            # coded lever press data
            '''
            A: number of active lever presses
            B: number of inactive lever presses
            C: infusions
            D: number of ctive lever presses in time-out
            E: number of inactive lever presses in time-out
            U: 10 minutes (or not....) bins active
            V: 10 minutes (or not....) bins inactive
            W: 10 minutes (or not....) bins infusions
            X: 10 minutes (or not....) bins active time-out
            Y: 10 minutes (or not....) bins inactive time-out
            '''
    
    
            self.find_sequence(box_content, index, "Total infusions", "C")
            self.find_sequence(box_content, index, "Total active", "A")
            self.find_sequence(box_content, index, "Total inactive", "B")
            self.find_sequence(box_content, index, "Total active time-out", "D")
    
            # infusions for first hour of experiment
            # so I assume (mayby incorrect) that it is 6 first values
            infusions = re.search(r"(W:\s*(\d+).+?)(?=X:|\Z)", box_content, re.DOTALL)
            
            # remove the 'W:'
            infusions = re.sub(r"W:", "", infusions.group(0))
        
            # now infusions is a string so group(0) is not necessary
            infusions = re.sub(r"\d+:", "", infusions)
            
            # store values as separate list elements
            infusions = infusions.split()
            
            # extract only 6 first values
            infusions_1h = infusions[0:6]
    
            # change to float
            for i in range(len(infusions_1h)):
                infusions_1h[i] = float(infusions_1h[i])
            
            # save to the proper column
            self.boxes.loc[index,"Infusions 1h"] = infusions_1h
            
            index += 1

        # change 'Duration' column type to time for proper excel save
        self.boxes["Duration"] = pd.to_datetime(self.boxes['Duration'], format='%H:%M:%S').dt.time
        
        return self.boxes
 
#pydoc.writedoc("behaviour")
