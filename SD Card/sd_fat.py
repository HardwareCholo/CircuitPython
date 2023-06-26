import machine
import sdcard
import uos

#Se asigna el pin CS
cs = machine.Pin(9, machine.Pin.OUT)

#Inicializa el periférico (start with 1 MHz)
spi = machine.SPI(1,
                  baudrate = 1000000,
                  polarity = 0,
                  phase = 0,
                  bits = 8,
                  firstbit = machine.SPI.MSB,
                  sck = machine.Pin(10),
                  mosi = machine.Pin(11),
                  miso = machine.Pin(8))

#Se inicializa la SD card
sd = sdcard.SDCard(spi, cs)

#Mount filesystem
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

#Crea un archivo y le escribe algo
with open("/sd/test01.txt", "w") as file:
    file.write("Hello, SD World!\r\n")
    file.wirte("This is a test\r\n")
    
#Abre el archivo que se acaba de crear
with open("/sd/test01.txt", "r") as file:
    data = file.read()
    print(data)