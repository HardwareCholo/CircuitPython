import machine
import bme280
import utime

#Se crea el objeto I2C
i2c = machine.I2C(0,scl=machine.Pin(17),sda=machine.Pin(16))

#Se crea el objeto BME280
bme = bme280.BME280(i2c=i2c, adress=0x76)

#Bucle infinito
while True:
    #Se imprime la lectura
    print("Presión: ",bme.values[1],"Humedad: ",bme.values[2])
    utime.sleep(0.5)
