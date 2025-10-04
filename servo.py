#!/usr/bin/env python3
from flask import Flask, render_template
import RPi.GPIO as GPIO
import time

# ---------------- MOTOR SETUP ----------------
IN1, IN2, IN3, IN4 = 17, 18, 22, 23   # Motor control pins
ENA, ENB = 27, 24                     # PWM enable pins

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for pin in (IN1, IN2, IN3, IN4, ENA, ENB):
    GPIO.setup(pin, GPIO.OUT)

# Motor PWM (1 kHz)
pwm_left = GPIO.PWM(ENA, 1000)
pwm_right = GPIO.PWM(ENB, 1000)
pwm_left.start(0)
pwm_right.start(0)

def set_speed(left=100, right=100):
    pwm_left.ChangeDutyCycle(left)
    pwm_right.ChangeDutyCycle(right)

def stop():
    GPIO.output(IN1, 0); GPIO.output(IN2, 0)
    GPIO.output(IN3, 0); GPIO.output(IN4, 0)
    set_speed(0, 0)

def forward(speed=100):
    set_speed(speed, speed)
    GPIO.output(IN1, 1); GPIO.output(IN2, 0)   # Left motor forward
    GPIO.output(IN3, 1); GPIO.output(IN4, 0)   # Right motor forward

def backward(speed=100):
    set_speed(speed, speed)
    GPIO.output(IN1, 0); GPIO.output(IN2, 1)   # Left motor backward
    GPIO.output(IN3, 0); GPIO.output(IN4, 1)   # Right motor backward

def left(speed=100):
    set_speed(speed, speed)
    GPIO.output(IN1, 0); GPIO.output(IN2, 1)   # Left motor backward
    GPIO.output(IN3, 1); GPIO.output(IN4, 0)   # Right motor forward

def right(speed=100):
    set_speed(speed, speed)
    GPIO.output(IN1, 1); GPIO.output(IN2, 0)   # Left motor forward
    GPIO.output(IN3, 0); GPIO.output(IN4, 1)   # Right motor backward

# ---------------- SERVO SETUP ----------------
SERVO_PIN = 26
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo_pwm = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz
servo_pwm.start(0)

def set_angle(angle):
    duty = 2 + (angle / 18)
    GPIO.output(SERVO_PIN, True)
    servo_pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    GPIO.output(SERVO_PIN, False)
    servo_pwm.ChangeDutyCycle(0)

# ---------------- FLASK APP ----------------
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# --- Motor routes ---
@app.route('/api/forward', methods=['POST'])
def go_forward():
    forward()
    return 'OK'

@app.route('/api/backward', methods=['POST'])
def go_backward():
    backward()
    return 'OK'

@app.route('/api/left', methods=['POST'])
def go_left():
    left()
    return 'OK'

@app.route('/api/right', methods=['POST'])
def go_right():
    right()
    return 'OK'

@app.route('/api/stop', methods=['POST'])
def go_stop():
    stop()
    return 'OK'

# --- Servo routes ---
@app.route('/api/servo/<int:angle>', methods=['POST'])
def move_servo(angle):
    if 0 <= angle <= 180:
        set_angle(angle)
        return f"Servo moved to {angle}ï¿½"
    return "Invalid angle", 400

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        stop()
        pwm_left.stop()
        pwm_right.stop()
        servo_pwm.stop()
        GPIO.cleanup()
