import logging
import logging.handlers
import os
import time
import sys


import cv2
import numpy as np
import skvideo.io
import utils
import matplotlib.pyplot as plt
# without this some strange errors happen
# this imports the feed from camera
#cv2.ocl.setUseOpenCL(False)
from pipeline import (
    PipelineRunner,
    CapacityCounter,
    ContextCsvWriter
)

#CONFIGURE THIS FROM YOUR END THE FEED SOURCE EUTHER USE THIS I HAVE COMMENTED ON IT
import os
import subprocess
os.chdir('C://Users/den')#put the name of thesource folder
#subprocess.call(['ffmpeg', '-i', 'picture%d0.png', 'output.avi'])
#subprocess.call(['ffmpeg', '-i', 'output.avi', '-t', '5', 'out.gif'])
# ============================================================================

cap = cv2.VideoCapture('input.mp4')

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('input.mp4')
 
# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")
 
# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
 
    # Display the resulting frame
    cv2.imshow('Frame',frame)
 
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
 
  # Break the loop
  else: 
    break
 
# When everything done, release the video capture object
#cap.release()
 

#OR THIS ONE
#IMAGE_DIR = "./den" #MY VIDEO FEED DIRECTORY
#VIDEO_SOURCE = '../den/input.mp4'
SHAPE = (720, 1280)
AREA_PTS = np.array([[780, 716], [686, 373], [883, 383], [1280, 636], [1280, 720]]) 


#----------------------------------------------------------------
# Create a VideoCapture object and read from input file
# If the input is taken from the camera, pass 0 instead of the video file name.
 




# ============================================================================


def main():
    log = logging.getLogger("main")

    base = np.zeros(SHAPE + (3,), dtype='uint8')
    area_mask = cv2.fillPoly(base, [AREA_PTS], (255, 255, 255))[:, :, 0]

    pipeline = PipelineRunner(pipeline=[
        CapacityCounter(area_mask=area_mask, save_image=True, image_dir=IMAGE_DIR),
        # saving every 5 seconds
        ContextCsvWriter('./report.csv', start_time=1505494325, fps=1, faster=5, field_names=['capacity'])
    ], log_level=logging.DEBUG)

    # Set up image source
    cap = skvideo.io.vreader(VIDEO_SOURCE)

    frame_number = -1
    st = time.time()
    
    try:
        for frame in cap:
            if not frame.any():
                log.error("Frame capture failed, skipping...")

            frame_number += 1

            pipeline.set_context({
                'frame': frame,
                'frame_number': frame_number,
            })
            context = pipeline.run()

            # skipping 5 seconds
            for i in xrange(240):
                cap.next()
    except Exception as e:
        log.exception(e)
# ============================================================================

if __name__ == "__main__":
    log = utils.init_logging()

    if not os.path.exists(IMAGE_DIR):
        log.debug("Creating image directory `%s`...", IMAGE_DIR)
        os.makedirs(IMAGE_DIR)

    main()
