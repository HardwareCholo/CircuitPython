#Este código utiliza el bus SPI para acceder a una tarjeta SD
import board, time, busio, sdcardio, storage, microcontroller

MOSI = board.GP3
MISO = board.GP4
clk = board.GP2
cs = board.GP15

spi = busio.SPI(clk, MOSI = MOSI, MISO = MISO)
sd = sdcardio.SDCard(spi, cs)
vfs = storage.VfsFat(sd)
storage.mount(vfs, '/sd')

while True:
    temp = microcontroller.cpu.temperature
    with open("/sd/pico.txt", "w") as file:
        file.write("El CPU se encuentra a: {0:f} C\n".format(temp))

    with open("/sd/pico.txt", "r") as file:
        for line in file:
            print(line, end='')

    time.sleep(2)

