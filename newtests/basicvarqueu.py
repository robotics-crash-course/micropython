import _thread
import utime

# var = 0.0
var_queue = []

def second_thread():
    var = 0
    while True:
        utime.sleep_ms(50)
        var +=1
        var_queue.append(var)

second_thread = _thread.start_new_thread(second_thread, ())

while True:
    utime.sleep_ms(1000)
    if var_queue: #check queue exists
        most_recent = var_queue.pop()
        print(most_recent)