import _thread
from machine import Timer
import utime

from include.rcc_library import Raft
from sensors.mpu6050 import MPU6050

# Global variables
theta = 0.0
theta_lock = _thread.allocate_lock()  # Create a lock object
exit_thread = False
theta_list = []  # Use a list for communication between threads
thread_finished = False  # Flag to signal the main thread

myraft = Raft()
myraft.setup_i2c()

def update_theta(timer):
    global theta
    with theta_lock:  # Acquire the lock before updating theta
        theta += myimu.get_angvel_z() * 0.01
        theta_list.append(theta)  # Append the updated theta value to the list

def updatetheta_thread():
    global exit_thread, thread_finished
    duration = 10  # in milliseconds

    # Set up a timer to call the update_theta function at the specified interval
    # theta_timer = Timer(-1)
    theta_timer= Timer(mode=Timer.PERIODIC, period=duration, callback=update_theta)

    # while not exit_thread:
    #     # Your other thread logic can go here
    #     # ...

    #     # Sleep or perform other operations as needed
    #     utime.sleep_ms(10)  # Adjust as needed

    # Stop the timer when the thread is exiting
    theta_timer.deinit()

    # Signal the main thread that the timer thread has finished
    thread_finished = True

# Create an instance of MPU6050
myimu = MPU6050(myraft.i2c_bus)

# Start the thread
test_thread = _thread.start_new_thread(updatetheta_thread, ())

# Sleep to allow the thread to run
# utime.sleep(60)  # Adjust as needed

# Set exit_thread to True to stop the thread gracefully
exit_thread = True

# Wait for the thread to finish
while not thread_finished:
    utime.sleep_ms(10)  # Adjust the sleep duration as needed

# Retrieve theta values from the list in the main thread
with theta_lock:  # Acquire the lock before accessing theta_list
    for current_theta in theta_list:
        print("Main Thread - Theta:", current_theta)
