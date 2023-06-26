import machine,time
from mpu6500 import MPU6500

led = machine.Pin(25, machine.Pin.OUT)
i2c = machine.I2C(1 ,sda=machine.Pin(26), scl=machine.Pin(27))

#Se crea el objeto del MPU
mpu = MPU6500(i2c)

while True:
    led.value(1)
    print(mpu.acceleration)
    time.sleep(0.5)
    led.value(0)
    time.sleep(0.5)