#########################################
# main.py                               #
# MANSEDS Self-Landing Rocket Code      #
# Contributors: Alex Koch               #
# Defines the main entry point for the  #
# second stage code. Manages the tasks  #
# to be performed.                      #
# Version: First flight 1.0 (09/03/2018)#
# For flight on 11/03/2018              #
#########################################



# Initiate all variables and the time

# Wait for signal that launch has begun and then start the recording

#

from camera_module import * # import everything from camera module, this defines the recording of the camera to a file
from barometer import * 
import time
import thread # Allows multi-threading. This is important to allow two different while true loops to run at the same time. 
# This is much more efficient than defining the loop ourselves as the camera and barometer might read at different rates. The
# processor will figure out the best order to execute these processes. This works even though the pi zero is a single cored processor.
import subprocess #  for calling bash commands
import sys # For sys.exit() call

t_0 = time.time()

def current_time(): # returns the current time, by subtracting off the epoch time
    return time.time() - t_0

def abort(): # Defines the exit point for the application if something goes wrong
    ##!! Open and closed brack is missed after "curren_time".
    ##!! In this case "current_time" is considered as a variable rather than a method
    ##!! I think it should be "current_time()"
    log_file(str(current_time) + ": Abort called, saving files...")
    sys.exit()

def initialise_I2C(): # Initialises I2C using bash scripts
    bash_command_1 = "sudo modprobe i2c-dev"
    ##!! Please look at the "## ******************************** ##" line.
    ##!! If it sounds good, you can substitute the following 6 lines with
    ##!! repeatProcess(bash_command_1).
    process = subprocess.Popen(bash_command_1.split(), stdout=subprocess.PIPE)
    bash_output, bash_error = process.communicate()
    log_file.write(str(current_time) + ": Bash command: " + bash_command_1 + " ; with output: " bash_output) # check if need to convert to string
    if(len(bash_error) != 0): # error in command
        log_file.write(str(current_time) + ": Bash command failure, error: " + bash_error)
        abort()

    bash_command_2 = "sudo modprobe i2c-bcm2708"
    ##!! Should not use "bash_command_2" instead of "bash_command_1".
    ##!! You can do the same thing here if you like. "## ************************ ##"
    process = subprocess.Popen(bash_command_1.split(), stdout=subprocess.PIPE)
    bash_output, bash_error = process.communicate()
    log_file.write(str(current_time) + ": Bash command: " + bash_command_1 + " ; with output: " bash_output) # check if need to convert to string
    if(len(bash_error) != 0): # error in command
        log_file.write(str(current_time) + ": Bash command failure, error: " + bash_error)
        abort()

    time.sleep(0.1)

    bash_command_3 = "sudo chmod 666 /dev/i2c-0"
    ##!! Should not use "bash_command_3" instead of "bash_command_1".
    ##!! You can do the same thing here if you like. "## ************************ ##"
    process = subprocess.Popen(bash_command_1.split(), stdout=subprocess.PIPE)
    bash_output, bash_error = process.communicate()
    log_file.write(str(current_time) + ": Bash command: " + bash_command_1 + " ; with output: " bash_output) # check if need to convert to string
    if(len(bash_error) != 0): # error in command
        log_file.write(str(current_time) + ": Bash command failure, error: " + bash_error)
        abort()

## ******************************** ##
##!! Why not defining a behaviour once and ,then, call it multiple times.
##!! If this approach reasonates with youi, please choose a better name for the function
##!! The changes that I've made to your original code is highlighted with ''' ''' 
##!! def repeatProcess('''address'''):
##!!   	process = subprocess.Popen('''address'''.split(), stdout=subprocess.PIPE)
##!!   	bash_output, bash_error = process.communicate()
##!!   	log_file.write(str(current_time'''()''') + ": Bash command: " + '''adress''' + " ; with output: " bash_output) # check if need to convert to string
##!!   	if(len(bash_error) != 0): # error in command
##!!        	log_file.write(str(current_time'''()''') + ": Bash command failure, error: " + bash_error)
##!!        	abort()

if '__name__' == '__main__':
    log_file = open("log_file" + time.strftime("%d/%m/%Y") + ".txt", "w")
    log_file.write("Time / ms     |       Comment")
    log_file.write(str(current_time) + ": Initialising...")

    # Initialise I2C using bash scripts
    initialise_I2C() # Will call abort() if failure occurrs

    # Initialise files
    

    # Initialise Threads

    try:
	##!! The first argument is not fed into the method parameter.
        thread_1 = thread.start_new_thread( , ("Thread 1: Barometer")) # Starts reading the Barometer
        thread_2 = thread.start_new_thread(initialise_camera, ("Thread 2: Camera")) #  Starts the camera module
        
    except:
	##!! I think there should be a bracket after "current_time"
        ##!! like "current_time()".
        log_file.write(str(current_time) + ": ERROR! Initialisation of threads unsuccessful!")
        abort()
    
    ##!! Same round bracket here after current_time ---> current_time()
    log_file.write(str(current_time) + ": Successfully Initialised threads.")
    
    ##!! Maybe true should be changed to True 
    is_active = true
    while(is_active):
        pass
        # The baromter reading defines when to start the camera recording
        # When the barometer or a certain time reading is reached, then end the program
    
    ##!! Same round bracket here.
    log_file.write(str(current_time) + ": Program end point reached, saving data...")

    # Save files

    log_file.close()

    # End program
