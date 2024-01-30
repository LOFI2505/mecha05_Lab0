"""!
@file main.py
This file contains code which does the tasks for the second checkpoint of lab0week1, a step response function and
an interrupt calback function. This code is uploaded to the NUCLEO main.py to produce an output in conjunction with 

TODO:

@author Lab05 Group05
@date   29-Jan-2024
"""

import utime
import cqueue

def timer_cb(timmy, my_queue, adc0):
    """!
    interrupt callback function to measure voltage and store it in queue
    @param timmy The timer number
    @param my_queue The queue storing the data
    @param adc0 The adc port
    """
    # measures voltage
    voltage = adc0.read()
    
    # adds to queue
    my_queue.put(voltage)
    
    # if queue is full, disable callback
    if my_queue.full():
        timmy.callback(None)

def step_response ():
    """!
    measures the time response of the output voltage at pin B0 in response to a change from 0V to 3.3V at the input at pin C0
    Have the program print measurements in two columns, CSV style: the time in milliseconds since the input step, and the voltage at that time
    """
    # configure pins
    pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)
    adc0 = pyb.ADC(pyb.Pin.board.PB0)
    
    # configure queue
    my_queue = cqueue.IntQueue(1000)
    
    # reset pin (make it low)
    pinC0.low()
    #utime.sleep(1)
    
    # configure and enable the callback
    timmy = pyb.Timer(1, freq=1000)
    timmy.callback(lambda tim: timer_cb(timmy, my_queue, adc0))
    
    # set the trigger high
    pinC0.high()
    
    # wait for a full queue
    while not my_queue.full():
        pass
    
    # iterate through queue to print data with a loop
    time = 1
    while my_queue.any():
        ADC = my_queue.get() / 1000
        print(f"{time},{ADC}")
        time = time + 1
            
    print("End")
    
    # set the trigger low
    pinC0.low()

if __name__ == "__main__":
    step_response()