from machine import Timer, Pin

led = Pin("LED", Pin.OUT)


def interrupt_handler(timer):
    led.toggle()

#timers run in ms periods
timer = Timer(mode=Timer.PERIODIC, period=100, callback=interrupt_handler)
