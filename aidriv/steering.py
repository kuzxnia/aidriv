import pigpio

freq = 50
left_in1, left_in2, left_pwm = 27, 23, 13
right_in3, right_in4, right_pwm = 4 ,17, 12
pivot_limit = 25

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
        
    
