#########################################
# camera_module.py                      #
# MANSEDS Self-Landing Rocket Code      #
# Contributors: Matthew Asker           #
# Uses data written to a file from      #
# barometer to indicate when to start   #
# and stop recording using the PiCamera #
#########################################

import picamera # imports module from picamera needed
import time

recording = 0 # a boolean variable to be set to 0 when camera is not recording and 1 when camera is recording

with picamera.PiCamera() as camera:

    camera.resolution = (640,480)

    while True:

        f = open('video_start.txt','r') # create an object f containing the file written to by the barometer
        start = f.read() # reads the text from the file and stores in start
        
        print(start)
        f.close();

        if start == "Going down!\n" and recording == 0: # if the rocket is travelling downwards and recording has not yet been started
            camera.start_recording('video.h264') # uses PiCamera method for camera object to start recording
            recording = 1 # indicate that recording is started
        elif start == "The rocket has landed!\n" and recording == 1: # if the rocket is stationary then it has landed
            camera.stop_recording() # uses PiCamera method for camera object to stop recording
        time.sleep(2)
