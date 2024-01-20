"""
This tutorial serves to introduce you to functionality of Raft and basics of micropython

topics covered:
- how to import a module
- how to instantiate raft and setup peripheral devices
- how to setup gpio pins as inputs and outputs

reminder:
use F12 to see definitions of RCC helper functions:)
"""

#to begin, import module from RCC library called Raft
from include.rcc_library import Raft

#use F12 to see all the functions within the Raft class
#to use any of these functions, we must instantiate the Raft class
myraft = Raft()
#when myraft is instantiated, everything inside the __init__() function is run
#the LED onboard the pico is setup using the first line of the init function
#inside the REPL, call the led functions to see what happens:)

#to call the functions from inside the REPL, type: myraft.led_on(), etc
myraft.led_on()
#note: we use the "." or dot operator to call functions (or methods) from within the class

######

#for the button built into the raft, its a little more complicated
#first, lets setup the button by calling the button setup helper function
myraft.setup_button()
#leaving the input to this function blank defaults to the Pins.BUTTON number which is 22 
#alternatively if you wanted to explicitly pass in the button pin, would first need to import the Pins class
from include.rcc_pins import Pins
#this class does not require instantiation, rather we can just call any value within it by using "." dot operator
#so another way to setup the button would be:
myraft.setup_button(Pins.BUTTON)
#since this is the default, it leads to same result

#first thing is setting up the GPIO as an input pin with a "pull-up" 
#when the button is not pressed, or just sitting there, the pull-up means that the gpio will always read +3.3V or 3v3
#this is important because any potential noise could cause a false button press to be read by the pico

#when the button is pressed, GPIO 22 will be connected to ground(GND), 
#in other words, the button signal will fall from high to low
#to detect this "falling" edge, we use an interupt request
#within the setup_button function, there is a irq or interupt request. 
#when the callback function within the irq is run, the button_pressed flag will become true
#to read the button's value call myraft.get_button() inside the REPL

#lets run a little loop to see how many times we can press the button in 3 seconds
#to use timing, need to import utime
import utime

#setup variables
time_started = utime.ticks_ms()
threeseconds = 3000 #3 thousand microseconds
button_counter = 0

while True:
    current_time = utime.ticks_ms()

    if myraft.get_button():
        button_counter+=1

    if (current_time - time_started >= threeseconds):
        print(button_counter)
        break

#in this example, within the while true loop, we're updating the value of current time
    #we're increasing the button counter when myraft.get_button() is true
    #and after 3 seconds, we print the count and break the while loop


######
#now lets play a reaction game
#when led blinks, press the button, then print how long it took to press the button


