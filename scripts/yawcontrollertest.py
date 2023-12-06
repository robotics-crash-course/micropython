from util.drivecontrol import YawControl
import time

mycontroller = YawControl(0, 70)

while True:
    print(mycontroller.boost)
    time.sleep_ms(100)
    