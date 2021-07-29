    """
    El rango del sensor es de entre 2 cm y 4 m.
    Los tiempos de espera recibidos al escuchar el pin de eco
    se convierten a OSError ('Fuera de rango')
    """
import machine, time
from machine import Pin
 
class HCSR04:
         
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=500*2*30):
        
        #trigger_pin: Pin de salida para enviar pulsos
        #echo_pin: Pin de solo lectura para medir la distancia.
        #echo_timeout_us: Tiempo de espera en microsegundos para escuchar el pin de eco.
        
        self.echo_timeout_us = echo_timeout_us
        # Inicia pin de salida(out)
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.value(0)
 
        # Inicia pin de entrada(in)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)
 
    def _send_pulse_and_wait(self):
        
        self.trigger.value(0) # estabiliza sensor 
        time.sleep_us(5)
        self.trigger.value(1)
        
        time.sleep_us(10)
        self.trigger.value(0)
        try:
            pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110:
                raise OSError('Out of range')
            raise ex
 
    def distance_mm(self):
        
        pulse_time = self._send_pulse_and_wait()
 
        # Para calcular la distancia obtenemos el pulse_time y lo dividimos por 2
        # (el pulso recorre la distancia dos veces) y por 29.1 porque
        # la velocidad del sonido en el aire (343,2 m / s), que es equivalente a
        # 0.34320 mm / us que es 1 mm cada 2.91us
        # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582
        
        mm = pulse_time * 100 // 582
        return mm
 
    def distance_cm(self):
        
        pulse_time = self._send_pulse_and_wait()
 
        # Para calcular la distancia obtenemos el pulse_time y lo dividimos por 2
        # (el pulso recorre la distancia dos veces) y por 29.1 porque
        
        cms = (pulse_time / 2)
        return cms