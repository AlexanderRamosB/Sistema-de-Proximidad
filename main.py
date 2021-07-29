from hcsr04 import HCSR04
from machine import Pin, SoftI2C
import SSD1306, network, time                            

print("inicio")

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
lcd = SSD1306.SSD1306_I2C(128, 64, i2c)

sensor = HCSR04(trigger_pin=13, echo_pin=12, echo_timeout_us=1000000)
lcd.invert(True)
#cordenadas de la pantalla
cordenadaXTitulo = 30
CordenadaYTitulo = 5
distanciaSensor = 0

#conexion a wifi
def conexionWIFI(SSID, PASSWORD):
    import network                            # importa el módulo network
    import urequests
    global sta_if
    sta_if = network.WLAN(network.STA_IF)     # instancia el objeto -sta_if- para controlar la interfaz STA
    if not sta_if.isconnected():              # si no existe conexión...
        sta_if.active(True)                       # activa el interfaz STA del ESP32
        sta_if.connect(SSID, PASSWORD)            # inicia la conexión con el AP
        print('Conectando a la red', SSID +"...")
        while not sta_if.isconnected():           # ...si no se ha establecido la conexión...
            pass                                  # ...repite el bucle...
        
    response = urequests.get("http://alex1423.pythonanywhere.com/")
    response.close()
    print('Configuración de red (IP/netmask/gw/DNS):', sta_if.ifconfig())

#Funcion del envio del correo
def enviarCorreo():
    import urequests
    response = urequests.get("http://alex1423.pythonanywhere.com/")
    response.close()
    print("Movimiento detectado")

def imprimirTituloPantalla(texto):
    lcd.text(texto, 30, 5)

def imprimirCuerpoPantalla(texto, cordenadaX, cordenadaY):
    lcd.text(texto, cordenadaX, cordenadaY)
    return;


try:
    conexionWIFI("NO DISPONOBLE", "Ds2480748")
    while True:
        lcd.fill(0)  # limpia el contenido de la pantalla
        lecturaDistanciaSensorUltrasonico = sensor.distance_cm()
        imprimirTituloPantalla('Mensaje')
        #imprimirCuerpoPantalla(str(lecturaDistanciaSensorUltrasonico), 30, 40)
        if lecturaDistanciaSensorUltrasonico > 5 and lecturaDistanciaSensorUltrasonico <= 30:
            imprimirCuerpoPantalla("Alerta a 30cm", 10, 30)
            imprimirCuerpoPantalla("Alerta email", 10, 45)
            enviarCorreo()
        elif lecturaDistanciaSensorUltrasonico > 40 and lecturaDistanciaSensorUltrasonico <= 70:
            imprimirCuerpoPantalla("Alerta a 50cm", 10, 40)   
        elif lecturaDistanciaSensorUltrasonico > 100:
            imprimirCuerpoPantalla("Sin novedad", 10, 40)#Los valores 30, 40 centran texto
            
        lcd.show()  # muestra o actualiza los valores centrados en la pantalla        
except KeyboardInterrupt:
    pass