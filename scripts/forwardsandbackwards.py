from util.drivecontrol import Controller

mycontroller = Controller()

mycontroller.start()
mycontroller.drive_forwards()

state = 1

while True:
    print(state)
    if state == 1:
        mycontroller.drive_forwards()
        mycontroller.raft.led_off()

        if mycontroller.left_odom.count >= 1000:
            state = 2
            mycontroller.left_odom.reset_count()
    
    if state == 2:
        mycontroller.drive_backwards()
        mycontroller.raft.led_on()

        if mycontroller.left_odom.count <= -1000:
            state = 1
            mycontroller.left_odom.reset_count()

