import RPi.GPIO as GPIO
from pins import ObjectCollection

# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

M1B = 10
M1F = 9
M2B = 8
M2F = 7

class Motor(object):
    type = 'Motor'

    def __init__(self, pin_fw, pin_bw):
        self._invert = False
        self.pin_fw = pin_fw
        self.pin_bw = pin_bw
        self._speed = 0

        GPIO.setup(self.pin_fw, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.pin_bw, GPIO.OUT, initial=GPIO.LOW)

        self.pwm_fw = GPIO.PWM(self.pin_fw, 100)
        self.pwm_fw.start(0)

        self.pwm_bw = GPIO.PWM(self.pin_bw, 100)
        self.pwm_bw.start(0)

    def invert(self):
        self._invert = not self._invert
        self._speed = -self._speed
        self.speed(self._speed)
        return self._invert

    def forwards(self, speed=100):

        if self._invert:
            self.speed(-speed)
        else:
            self.speed(speed)

    def backwards(self, speed=100):

        if self._invert:
            self.speed(speed)
        else:
            self.speed(-speed)

    def speed(self, speed=100):
        if speed > 100 or speed < -100:
            raise ValueError("Speed must be between -100 and 100")

        self._speed = speed
        if speed > 0:
            self.pwm_bw.ChangeDutyCycle(0)
            self.pwm_fw.ChangeDutyCycle(speed)
        if speed < 0:
            self.pwm_fw.ChangeDutyCycle(0)
            self.pwm_bw.ChangeDutyCycle(abs(speed))
        if speed == 0:
            self.pwm_fw.ChangeDutyCycle(0)
            self.pwm_bw.ChangeDutyCycle(0)

        return speed

    def stop(self):
        self.speed(0)

    def _add(self, **kwargs):
        for name in kwargs:
            self._add_single(name, kwargs[name])

    forward = forwards
    backward = backwards
    reverse = invert

motor = ObjectCollection()
motor._add(one=Motor(M1F, M1B))
motor._add(two=Motor(M2F, M2B))