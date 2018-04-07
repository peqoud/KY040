#KY040 Python Class
#Erich Ebenhoch

from gpiozero import DigitalInputDevice

class KY040:

    CLOCKWISE     = 0
    ANTICLOCKWISE = 1

    def __init__(self, clockPin, dataPin, switchPin=None, rotaryCallback=None, switchCallback=None, rotaryBouncetime=0.050, switchBouncetime=0.050):
        # persist values
        self.clockPin       = DigitalInputDevice(clockPin, pull_up=False, bounce_time=rotaryBouncetime)
        self.dataPin        = DigitalInputDevice(dataPin,  pull_up=False, bounce_time=rotaryBouncetime)
        if None != switchPin:
            self.switchPin = DigitalInputDevice(switchPin, pull_up=False, bounce_time=switchBouncetime)
        else:
            self.switchPin = None
        self.rotaryCallback   = rotaryCallback
        self.switchCallback   = switchCallback
        self.rotaryBouncetime = rotaryBouncetime
        self.switchBouncetime = switchBouncetime

        # handle falling edge is a change to closed 
        # http://henrysbench.capnfatz.com/henrys-bench/arduino-sensors-and-input/keyes-ky-040-arduino-rotary-encoder-user-manual/
        self.clockPin.pin.edges  = "falling"
        self.dataPin.pin.edges   = "falling"
        self.switchPin.pin.edges = "falling"


    def start(self):
        self.clockPin.pin.when_changed = self._clockCallback
        
        if None != self.switchPin:
            self.switchPin.pin.when_changed = self._switchCallback

    def stop(self):
        self.clockPin.pin.when_changed = None

        if None != self.switchPin:
            self.switchPin.pin.when_changed = None

    def _clockCallback(self):
        if self.clockPin.pin.state == 0:
            data = self.dataPin.pin.state
            if data == 1:
                self.rotaryCallback(self.ANTICLOCKWISE)
            else:
                self.rotaryCallback(self.CLOCKWISE)

    def _switchCallback(self):
        if None == self.switchPin:
            return

        if self.switchPin.pin.state == 0:
            self.switchCallback()

