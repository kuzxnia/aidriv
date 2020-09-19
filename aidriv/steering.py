import pigpio

freq = 50

left_in1 = 27
left_in2 = 23
left_pwm = 13

right_in3 = 4
right_in4 = 17
right_pwm = 12

class Steering:
    def __init__(self):
        self.left_in1 = left_in1
        self.left_in2 = left_in2
        self.left_pwm = left_pwm
        self.right_in3 = right_in3
        self.right_in4 = right_in4
        self.right_pwm = right_pwm
        self.left_pwm_duty = 0
        self.right_pwm_duty = 0
        self.pi = pigpio.pi()
        self.pi.set_mode(self.left_in1, pigpio.OUTPUT)
        self.pi.set_mode(self.left_in2, pigpio.OUTPUT)
        self.pi.set_mode(self.right_in3, pigpio.OUTPUT)
        self.pi.set_mode(self.right_in4, pigpio.OUTPUT)
        self.pi.write(self.left_in1, 0)
        self.pi.write(self.left_in2, 0)
        self.pi.write(self.right_in3, 0)
        self.pi.write(self.right_in4, 0)
    
    def change_motors_speed(self, forward, turn):
        self.left_motor_pwm = 0
        self.right_motor_pwm = 0

        if forward >= 0:
            if forward >= abs(turn):
                if turn >= 0:#1st segment
                    self.left_motor_pwm = forward
                    self.right_motor_pwm = forward - turn
                elif turn < 0:#8th segment
                    self.left_motor_pwm = forward - abs(turn)
                    self.right_motor_pwm = forward
                    
                self.pi.write(left_in1, 0)
                self.pi.write(left_in2, 1)
                self.pi.write(right_in3, 0)
                self.pi.write(right_in4, 1)
            else:
                if turn >= 0:#2nd segment
                    self.left_motor_pwm = forward
                    self.right_motor_pwm = turn - forward
                    self.pi.write(left_in1, 0)
                    self.pi.write(left_in2, 1)
                    self.pi.write(right_in3, 1)
                    self.pi.write(right_in4, 0)
                elif turn < 0:#7th segment
                    self.left_motor_pwm = abs(turn) - forward
                    self.right_motor_pwm = forward
                    self.pi.write(left_in1, 1)
                    self.pi.write(left_in2, 0)
                    self.pi.write(right_in3, 0)
                    self.pi.write(right_in4, 1)
        elif forward < 0:
            if abs(forward) >= abs(turn):
                if turn >= 0:#4th segment
                    self.left_motor_pwm = abs(forward)
                    self.right_motor_pwm = abs(forward) - turn
                elif turn < 0:#5th segment
                    self.left_motor_pwm = abs(forward) - abs(turn)
                    self.right_motor_pwm = abs(forward)
                    
                self.pi.write(left_in1, 1)
                self.pi.write(left_in2, 0)
                self.pi.write(right_in3, 1)
                self.pi.write(right_in4, 0)
            else:
                if turn >= 0:#3rd segment
                    self.left_motor_pwm = abs(forward)
                    self.right_motor_pwm = turn - abs(forward)
                    self.pi.write(left_in1, 1)
                    self.pi.write(left_in2, 0)
                    self.pi.write(right_in3, 0)
                    self.pi.write(right_in4, 1)
                elif turn < 0:#6th segment
                    self.left_motor_pwm =  abs(turn)- abs(forward)
                    self.right_motor_pwm = abs(forward)
                    self.pi.write(left_in1, 0)
                    self.pi.write(left_in2, 1)
                    self.pi.write(right_in3, 1)
                    self.pi.write(right_in4, 0)

        self.pi.hardware_PWM(left_pwm, freq, self.left_motor_pwm*10000)
        self.pi.hardware_PWM(right_pwm, freq, self.right_motor_pwm*10000)
        
    
