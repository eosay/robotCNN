import pyb 

class Stepper():
    def __init__(self, step, direc, enable, freq):
        # initialize pins as push pull
        self.step = pyb.Pin(step, pyb.Pin.OUT_PP)
        self.direc = pyb.Pin(direc, pyb.Pin.OUT_PP)
        self.enable = pyb.Pin(enable, pyb.Pin.OUT_PP)
        self.freq = freq

        self.speed = 0
        self.count = 0
        self.rate = 1
        self.count = 0

        self.enable.low()
        self.direc.high()

    def turn(self):
        # counter incremented in timer callback, effectively changes the freq
        if self.speed != 0:
            self.count = (self.count+1)%self.rate
            if self.count == 0:
                self.step.high()
                # the stepper motor driver needs a 2us pulse
                pyb.udelay(2)
                self.step.low()

    def set_speed(self, value):
        if value > 0:
            self.rate = self.freq//value
            self.speed = value
        else:
            self.speed = 0
    
    def halt(self):
        # lock the stepper motor, this draws power
        # enable low is needed to send step instructions to the motor
        self.enable.low()
    
    def off(self):
        # turn the motor off and allow free spin
        self.enable.high()
        self.step.low()

# objects needed for callbacks
tim1 = pyb.Timer(8, freq=10000)
stepper = Stepper('X1', 'X2', 'X3', tim1.freq())
# virtual comm port connection
com = pyb.USB_VCP()

# limit switch callback
# delay and interupt enabling/disabling for switch debouncing 
def limit_cb(line):
    limit.disable()
    pyb.delay(10)
    stepper.off()
    pyb.LED(2).toggle()
    limit.enable()
    print('[pyboard] limit switch active: stepper off')

def stepper_cb(t):
    stepper.turn()

tim1.callback(stepper_cb)
limit = pyb.ExtInt('X4', pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_DOWN, limit_cb)

while True:
	if com.any():
		data = com.read()
		stepper.halt()
		
		print(data)
		
		if data == b'10':
			stepper.direc.low()
            print('[pyboard] direction 0')
		elif data == b'01':
			stepper.direc.high()
            print('[pyboard] direction 1')
		else:
			print('[pyboard] unknown command')
        
        # accelerate the stepper
		for i in range(0, 800, 200):
			stepper.set_speed(i)
        
        # run for 100 ms
		pyb.delay(100)

	else:
        # if no command sent, decelerate the stepper
		if stepper.speed != 0:
			for i in reversed(range(0, 800, 200)):
				stepper.set_speed(i)
		stepper.off()
	

            
        



