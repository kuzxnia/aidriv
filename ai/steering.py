import RPi.GPIO as GPIO

freq = 50

left_in1, left_in2, left_pwm = 26, 19, 21
right_in3, right_in4, right_pwm = 13, 6, 5


class Steering:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.set_gpio_out()
        self.reset_pwm_duty()
        self.set_pwm()
        self.set_qpio_low()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.left_pwm.stop()
        self.right_pwm.stop()
        GPIO.cleanup()

    def set_gpio_out(self):
        for pin in [left_in1, left_in2, left_pwm, right_in3, right_in4, right_pwm]:
            GPIO.setup(pin, GPIO.OUT)

    def set_pwm(self):
        self.left_pwm = GPIO.PWM(left_pwm, freq)
        self.left_pwm.start(self.left_pwm_duty)

        self.right_pwm = GPIO.PWM(right_pwm, freq)
        self.right_pwm.start(self.right_pwm_duty)

    def update_pwm(self):
        self.left_pwm.ChangeDutyCycle(self.left_pwm_duty)
        self.right_pwm.ChangeDutyCycle(self.right_pwm_duty)

    def set_qpio_low(self):
        for pin in [left_in1, left_in2, right_in3, right_in4]:
            GPIO.output(pin, GPIO.LOW)

    def reset_pwm_duty(self):
        self.left_pwm_duty = 0
        self.right_pwm_duty = 0

    def set_gpio(self, l1, l2, r1, r2):
        GPIO.output(left_in1, l1)
        GPIO.output(left_in2, l2)
        GPIO.output(right_in3, r1)
        GPIO.output(right_in4, r2)

    def recalculate_pwm(self, forward, turn):
        '''forward and turn depends from quater'''
        forward = abs(forward)

        self.left_pwm_duty = forward * (turn + 100) / 200
        self.right_pwm_duty = forward - self.left_pwm_duty

    def change_motors_speed(self, forward, turn):
        print(f'change_motors_speed {forward} : {turn}')
        self.left_pwm_duty = 0
        self.right_pwm_duty = 0

        if forward >= 0:
            self.set_gpio(GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.HIGH)
        else:
            self.set_gpio(GPIO.HIGH, GPIO.LOW, GPIO.HIGH, GPIO.LOW)

        self.recalculate_pwm(forward, turn)

        print(f'left_pwm: {self.left_pwm_duty} right_pwm: {self.right_pwm_duty}')
        self.update_pwm()
