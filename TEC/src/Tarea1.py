# ------------------------------------------------------------------------------
## Carga de módulos
# ------------------------------------------------------------------------------
import json
from machine import Pin, PWM, ADC, SPI, Timer
import math
import time
import sys
import uselect
# ------------------------------------------------------------------------------
SOURCE = 'Procesamiento de Señales'
# ------------------------------------------------------------------------------
# Configuración de entrada/salida 
# ------------------------------------------------------------------------------
led = PWM(Pin(14))
signal_in = ADC(26)
signal_out = PWM(Pin(14))
signal_out.freq(10000)
#buffer = [0,0,0,0,0,0,0,0,0,0] #cambio y creación de buffer
N = 5
buffer = []

# ------------------------------------------------------------------------------
# ADC
# ------------------------------------------------------------------------------
def readInput():
    return signal_in.read_u16()
# ------------------------------------------------------------------------------
# DAC
# ------------------------------------------------------------------------------
def writeOutput(value: int):
    '''Write output to DAC '''
    signal_out.duty_u16(value)
# ------------------------------------------------------------------------------
# Comunicación serie
# ------------------------------------------------------------------------------
def parse_command(cmd):
    global params
    try:
        command = json.loads(cmd)
        # Escribe aquí el código para interpretar las órdenes recibidas
    except Exception as e:
        print('{"result":"unknown or malformed command"}')
# ------------------------------------------------------------------------------
# Bucle principal
# ------------------------------------------------------------------------------
#   1. Espera hasta el siguiente periodo de muestreo (PERIOD_US).
#   2. Genera la siguiente muestra de la señal y la envía a la salida (PWM).
#   3. Lee el valor de la entrada analógica (ADC).
# ------------------------------------------------------------------------------
def FFT(buffer):
    #N = 5
    #buffer = [0 for n in range(N)] => esto debería crear el buffer = [0,0,0,0,0,0...hasta N]
    for n in range (N):
        for k in range (N):
            Wkn[n][k] = cmath.exp(-1j*2*cmath.pi*k*n/N)
            
            
            
    #Genero las funciones par e impar x(2n) y x(2n+1), respectivamente:
    fn = [0 for n in range(N)] #create a list of zeros 
    gn = [0 for n in range(N)] #no necesario 
    for i in range(2*N):
        if i % 2 == 0: #par
            n = int(i/2)
            fn[n] = buffer[i]
        else: #impar
            n = int((i-1)/2)
            gn[n] = buffer[i]
            
    #Se calcula la DFT de las funciones par e impar: f(n) y g(n) F(k) y G(k).
    #El cálculo lo hacemos a través de la matriz de coeficientes Wkn
    #fk = [0 for n in range(N)]
    fk[k] = 0
    gk[k] = 0
    for k in range(N):
        for n in range(N):
        fk[k] = fn[k]*Wkn[n][k]+fk[k]
        gk[k] = gn[k]*Wkn[n][k] + gk[k]

    #Finalmente, calculamos la trans. Fourier de la señal completa X[k] al sumar F[k]+G[k]
    #Hay que tener en cuenta que la fórmula cambia, dependiendo en que rango nos encotramos
    #Para 0<=k<=N/2, la fórmula es: X[k] = F[k] + W*G[k]
    #Para N/2<=k<=N, la fórmula es: X[k] = F[k] - W*G[k]
    #Primero calculamos la matriz W:
    
              








def waitNextPeriod(previous):
    lapsed = time.ticks_us() - previous
    offset = -60
    remaining = PERIOD_US - lapsed + offset
    if 0 < lapsed <= PERIOD_US:
        time.sleep_us(remaining)
    return time.ticks_us()

def loop():
    state = []
    tLast = time.ticks_us()
    t0 = tLast
    spoll = uselect.poll()
    spoll.register(sys.stdin, uselect.POLLIN)
    while True:
        data = []
        for i in range(BUFFER_SIZE):
            try:
              t = waitNextPeriod(tLast)
              u = signal((t-t0)*1e-6)
              y = readInput()
              
              
              buffer[i] = y
              yjw = FFT(buffer)
              for j in range(2*N):
                  ywn = abs(yjw[j])
                  print(f'{u} {y}')
                  
                  
                  
              writeOutput(u)
            except ValueError:
              pass
            data.append([(t-t0)*1e-6, u, y])
            tLast = t
        if spoll.poll(0):
            cmd = str(sys.stdin.readline())
            parse_command(cmd)
        #print(f'{u} {y}')
# ------------------------------------------------------------------------------
# INSTRUCCIONES
# ------------------------------------------------------------------------------
PERIOD_US = 1000 # Periodo de muestreo en microsegundos
BUFFER_SIZE = 10 # Muestras en el buffer

def signal(t):
  # Pon aquí el código necesario para generar tu señal.
  
  signal_o = math.sin(2*math.pi*1000*t)
  return int(math.fabs(signal_o))

# ------------------------------------------------------------------------------
# Comienza la ejecución
# ------------------------------------------------------------------------------
loop()

    
