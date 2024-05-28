import os
import logging
import logging.handlers
import random

import numpy as np
import skvideo.io
import cv2
import matplotlib.pyplot as plt
import subprocess
os.chdir('C://Users/den')#put the name of thesource folder
#subprocess.call(['ffmpeg', '-i', 'picture%d0.png', 'output.mp4'])
#subprocess.call(['ffmpeg', '-i', 'output.mp4', '-t', '5', 'out.gif'])

import utils
# without this some strange errors happen
cv2.ocl.setUseOpenCL(False)
random.seed(123)



# Create a VideoCapture object and read from input file
# If the input is taken from the camera, pass 0 instead of the video file name.
 
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
 
 
# ============================================================================
#IMAGE_DIR = "./out"
#VIDEO_SOURCE = "input.mp4"
#SHAPE = (720, 1280)  # HxW


def train_bg_subtractor(inst, cap, num=500):
    '''
        BG substractor need process some amount of frames to start giving result
    '''
    print ('Training BG Subtractor...')
    i = 0
    for frame in cap:
        inst.apply(frame, None, 0.001)
        i += 1
        if i >= num:
            return cap


def main():
    log = logging.getLogger("main")

    # creting MOG bg subtractor with 500 frames in cache
    # and shadow detction
    bg_subtractor = cv2.createBackgroundSubtractorMOG2(
        history=500, detectShadows=True)

    # Set up image source
    # You can use also CV2, for some reason it not working for me
    cap = skvideo.io.vreader(VIDEO_SOURCE)

    # skipping 500 frames to train bg subtractor
    train_bg_subtractor(bg_subtractor, cap, num=500)

    frame_number = -1
    for frame in cap:
        if not frame.any():
            log.error("Frame capture failed, stopping...")
            break

        frame_number += 1

        utils.save_frame(frame, "./out/frame_%04d.png" % frame_number)

        fg_mask = bg_subtractor.apply(frame, None, 0.001)
        
        utils.save_frame(frame, "./out/fg_mask_%04d.png" % frame_number)



if __name__ == "__main__":
    log = utils.init_logging()

    if not os.path.exists(IMAGE_DIR):
        log.debug("Creating image directory `%s`...", IMAGE_DIR)
        os.makedirs(IMAGE_DIR)

    main()

    # When everything done, release the video capture object
cap.release()
# Closes all the frames
cv2.destroyAllWindows()
