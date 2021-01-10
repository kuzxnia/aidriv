import RPi.GPIO as GPIO
import pigpio

freq = 50
left_in1, left_in2, left_pwm = 27, 23, 13
right_in3, right_in4, right_pwm = 4 ,17, 12
pivot_limit = 25


# klasa abst, zmienić z rpi na pippio

class Steering:
    def __init__(self):
        self.pi = pigpio.pi()
        self.set_gpio_out()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.pi.hardware_PWM(left_pwm, freq, 0)
        self.pi.hardware_PWM(right_pwm, freq, 0)
    
    def set_gpio_out(self):
        for pin in [left_in1, left_in2, right_in3, right_in4]: 
            self.pi.set_mode(pin, pigpio.OUTPUT)
            self.pi.write(pin, 0)

    # na różne algorytmy
    def change_motors_speed(self, forward, turn):
        if forward >= 0:
            left_motor = 100 if turn>= 0 else 100 + turn
            right_motor = 100 - turn if turn>= 0 else 100
        else:
            left_motor = 100 - turn if turn>= 0 else 100
            right_motor = 100 if turn>= 0 else 100 + turn

        left_motor *= forward / 100
        right_motor *= forward / 100

        piv_scale = 0 if abs(forward)>pivot_limit else 1-abs(forward)/pivot_limit

        left_motor = int((1 - piv_scale) * left_motor + piv_scale * (turn))
        right_motor = int((1 - piv_scale) * right_motor + piv_scale * (-turn))
        
        if left_motor >= 0:
            self.pi.write(left_in1, 0)
            self.pi.write(left_in2, 1)
        else:
            self.pi.write(left_in1, 1)
            self.pi.write(left_in2, 0)

        if right_motor >= 0:
            self.pi.write(right_in3, 0)
            self.pi.write(right_in4, 1)
        else:
            self.pi.write(right_in3, 1)
            self.pi.write(right_in4, 0)

        self.pi.hardware_PWM(left_pwm, freq, abs(left_motor)*10000)
        self.pi.hardware_PWM(right_pwm, freq, abs(right_motor)*10000)


class AiSteering:
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
