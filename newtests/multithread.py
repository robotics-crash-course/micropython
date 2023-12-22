from time import sleep
import _thread

def core0func():
    counter = 0
    while True:
        print("0, ", counter)
        counter += 2
        sleep(1)

def core1func():
    counter = 1
    while True: 
        print("1, ", counter)
        counter += 2
        sleep(2)

#run second thread
second_thread = _thread.start_new_thread(core1func, ())

#run first thread
core0func()