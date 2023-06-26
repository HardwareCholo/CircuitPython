import machine
import utime,time
import bme280
from mpu6500 import MPU6500
from math import sqrt, atan2, pi, copysign
import sdcard
import uos, os, ustruct
from micropyGPS import MicropyGPS

#Led para checar el funcionamiento
led = machine.Pin(25, machine.Pin.OUT)

#Se asigna el pin CS
cs = machine.Pin(5, machine.Pin.OUT)

#Inicialización de los periféricos
spi = machine.SPI(0,
                  baudrate = 1000000,
                  polarity = 0,
                  phase = 0,
                  bits = 8,
                  firstbit = machine.SPI.MSB,
                  sck = machine.Pin(2),
                  mosi = machine.Pin(3),
                  miso = machine.Pin(4))
i2c = machine.I2C(1 ,sda=machine.Pin(26), scl=machine.Pin(27))

#Se crea el objeto gps
gpsModule = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1))
#print(gpsModule)

#Se inicializa la SD card
sd = sdcard.SDCard(spi, cs)

#Mount filesystem
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

#Se crea el objeto del MPU
mpu = MPU6500(i2c)

#Se crea el objeto BME280
#bme = bme280.BME280(i2c=i2c, adress=0x76)

#Algunas variables necesarias
buff = bytearray(255)

TIMEOUT = False
FIX_STATUS = False

latitude = "" 
longitude = ""
satellites = ""
GPStime = ""

#Crea el encabezado del txt
with open("/sd/lecturas.txt", "w") as file:
    file.write("Posición en X\tPosición en Y\tLatitud\tLongitud\tSatelites Humedad Presión Temperatura\r\n")

#Funciones para el GPS
def getGPS(gpsModule):
    global FIX_STATUS, TIMEOUT, latitude, longitude, satellites, GPStime
    
    timeout = time.time() + 8 
    while True:
        gpsModule.readline()
        buff = str(gpsModule.readline())
        parts = buff.split(',')
    
        if (parts[0] == "b'$GPGGA" and len(parts) == 15):
            if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
                print(buff)
                
                latitude = convertToDegree(parts[2])
                if (parts[3] == 'S'):
                    latitude = "-"+latitude
                longitude = convertToDegree(parts[4])
                if (parts[5] == 'W'):
                    longitude = "-"+longitude
                satellites = parts[7]
                GPStime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
                FIX_STATUS = True
                break
                
        if (time.time() > timeout):
            TIMEOUT = True
            break
        utime.sleep_ms(500)
        
def convertToDegree(RawDegrees):

    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat/100) 
    nexttwodigits = RawAsFloat - float(firstdigits*100) 
    
    Converted = float(firstdigits + nexttwodigits/60.0)
    Converted = '{0:.6f}'.format(Converted) 
    return str(Converted)

while True:
    led.value(1)
    
    #Lectura del GPS    
    getGPS(gpsModule)

    if(FIX_STATUS == True):
        #print("Printing GPS data...")
        #print(" ")
        #print("Latitude: "+latitude+"\tLongitud: "+longitude+"\tSatellites: "+satellites+"\tTime: "+GPStime)
        lectura_gps = latitude+"\t"+longitude+"\t"+satellites
        
        FIX_STATUS = False
        
    if(TIMEOUT == True):
        #print("No GPS data is found.")
        lectura_gps = "No GPS"+"\tNo GPS"+"\t No GPS"
        TIMEOUT = False
    
    
    #Se calcula el ángulo
    ax = mpu.acceleration[0]
    ay = mpu.acceleration[1]
    az = mpu.acceleration[2]
    x = atan2(ax,sqrt((ay*ay)+(az*az)))
    y = atan2(ay,sqrt((ax*ax)+(az*az)))
    
    #Se imprime la lectura
    #print("Temperatura interna: ",bme.values[0],"Presión: ",bme.values[1],"Humedad: ", bme.values[2], x,"x, ",y,"y")
    #print(x,"x, ",y,"y")
    
    #Se concatenan los sensores leídos
    lectura = str(x) + "\t" + str(y) + "\t" + lectura_gps + "\r\n"
    
    #Crea un archivo y le escribe algo
    with open("/sd/lecturas.txt", "r") as file:
     #file.write("Temperatura interna: ",bme.values[0],"Presión: ",bme.values[1],"Humedad: ", bme.values[2], x,"x, ",y,"y\r\n")
     lectura_existente = file.read()
     print(lectura_existente)
     lectura_nueva = lectura_existente + lectura
     
    with open("/sd/lecturas.txt", "w") as file:
     file.write(lectura_nueva)
    led.value(0)
    utime.sleep(1)
    

