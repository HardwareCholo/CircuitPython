#Ejemplo de parpadeo de un LED
import board, digitalio, time

led = digitalio.DigitalInOut(board.led)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)

