'''
second_stage.py                               
MANSEDS Self-Landing Rocket Code      
Contributors: Alex Koch
Defines the main entry point for the second stage code. Manages the tasks to be performed.                      
Version:  3.0 (Second flight 22/04/18)
'''

from barometer import * 

import time
import thread # Allows multi-threading. This is important to allow two different while true loops to run at the same time. 
# This is much more efficient than defining the loop ourselves as the camera and barometer might read at different rates. The
# processor will figure out the best order to execute these processes. This works even though the pi zero is a single cored processor.
import subprocess #  for calling bash commands
import sys # For sys.exit() call
from picamera import PiCamera

t_0 = time.time()

def current_time(): # returns the current time, by subtracting off the epoch time
    return time.time() - t_0

def abort(log_file): # Defines the exit point for the application if something goes wrong
    print("Aborting")
    log_file.write(str(current_time()) + ": Abort called, saving files...\n")
    sys.exit()

def bash_command(command, log_file):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    bash_output, bash_error = process.communicate()
    log_file.write(str(current_time()) + ": Bash command: " + command + " ; with output: " + bash_output + "\n") # check if need to convert to string
    #if(len(bash_error) != 0):
    #    log_file.write(str(current_time()) + ": Bash command failure, error: " + bash_error + "\n")
    #    abort(log_file)

def initialise_I2C(log_file): # Initialises I2C using bash scripts
    bash_command("sudo modprobe i2c-dev", log_file)
    bash_command("sudo modprobe i2c-bcm2708", log_file)
    time.sleep(0.1) # Give it a little time
    bash_command("sudo chmod 666 /dev/i2c-1", log_file)


def record():
    print("Recording")
    camera = PiCamera()
    #camera.start_preview()
    camera.start_recording('launch_videao.h264')
    time.sleep(1 * 60) # The length of time the camera record for in seconds
    camera.stop_recording()
    #camera.stop_preview()
    print("Recording ended")

if __name__ == '__main__':

    log_file = open("log_file_" + ".txt", "w")
    log_file.write("Current time: " + time.strftime("%d:%m:%Y H:%M:%S", time.gmtime()) + "\n")
    log_file.write("Time / ms     |       Comment \n")
    log_file.write(str(current_time()) + ": Initialising... \n")

    # Initialise I2C using bash scripts
    initialise_I2C(log_file) # Will call abort() if failure occurrs

    invalid_input = True
    while(invalid_input):
        start_camera = input("Start the camera y [0]  / n [1] ?: " )
        if (start_camera == 0):
            #try:
                #thread_1 = thread.start_new_thread(record_pressure) # Starts reading the Barometer
                #thread_2 = thread.start_new_thread(record) #  Starts the camera module
                #thread_1 = threading.Thread(name='Thread 1: Barometer', target=)
                #thread_2 = threading.Thread(name='Thread 2: Camera', target=record)
                #thread_1.start()
                #thread_2.start()
            #except:
                #log_file.write(str(current_time()) + ": ERROR! Initialisation of threads unsuccessful! \n")
                #abort(log_file)
            #log_file.write(str(current_time()) + ": Successfully Initialised threads. \n")
	        #record()
            print("Recording")
            camera = PiCamera()
            camera.start_recording('launch_videao.h264')
            log_file.write(str(current_time())  + ": Successfully Started Camera. \n")
	    record_pressure()
            camera.stop_recording()
            print("Recording ended")
            invalid_input = False
        elif( start_camera == 1):
            # Exit
            invalid_input = False
            abort(log_file)
        else:
            print("Invalid input")
    
    #thread_1.join()
    #thread_2.join()
    
    log_file.write(str(current_time()) + ": Program end point reached, saving data... \n")

    # Save files

    log_file.close()

    # End program
