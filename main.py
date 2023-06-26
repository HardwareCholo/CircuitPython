import machine
import utime
import bme280
from mpu6500 import MPU6500
from math import sqrt, atan2, pi, copysign
import sdcard
import uos

#Se asigna el pin CS
cs = machine.Pin(1, machine.Pin.OUT)

#Inicializa el periférico (start with 1 MHz)
spi = machine.SPI(0,
                  baudrate = 1000000,
                  polarity = 0,
                  phase = 0,
                  bits = 8,
                  firstbit = machine.SPI.MSB,
                  sck = machine.Pin(2),
                  mosi = machine.Pin(3),
                  miso = machine.Pin(4))

#Se inicializa la SD card
sd = sdcard.SDCard(spi, cs)

#Mount filesystem
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

#Se crea el objeto i2C
i2c = machine.I2C(0,scl=machine.Pin(17),sda=machine.Pin(16))

#Se crea el objeto del MPU
mpu = MPU6500(i2c)

#Se crea el objeto BME280
bme = bme280.BME280(i2c=i2c, adress=0x76)

while True:
    #Se calcula el ángulo
    ax = mpu.acceleration[0]
    ay = mpu.acceleration[1]
    az = mpu.acceleration[2]
    x = atan2(ax,sqrt((ay*ay)+(az*az)))
    y = atan2(ay,sqrt((ax*ax)+(az*az)))
    
    #Se imprime la lectura
    print("Temperatura interna: ",bme.values[0],"Presión: ",bme.values[1],"Humedad: ", bme.values[2], x,"x, ",y,"y")
    
    #Crea un archivo y le escribe algo
with open("/sd/test01.txt", "w") as file:
     file.write("Temperatura interna: ",bme.values[0],"Presión: ",bme.values[1],"Humedad: ", bme.values[2], x,"x, ",y,"y\r\n")
     
    utime.sleep(1)