import machine

#Se crea el objeto I2C
i2c = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16))

#Imprime por consola las direcciones I2C de los dispositivos encontrados
devices = i2c.scan()

if devices:
    for d in devices:
        print(hex(d))