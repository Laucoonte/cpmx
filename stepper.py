# ____________________________________________________
# ____________________________________________________
""" import piCamera
# load Camera
camera=piCamera()
camera.resolution (320,240)
camera.capture("olakease.jpg") """
# ____________________________________________________
# SETUP

# Importacion de bibliotecas
import RPi.GPIO as GPIO # Board de Raspberry Pi
import time # "Control" de tiempo

# Numeracion de pines por el sistema GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)

# Asignacion de pines de control del motor a pasos
A1 = 26
B1 = 19
A2 = 13
B2 = 6

# Configuracion del modo de trabajo de los pines
GPIO.setup(A1,GPIO.OUT)
GPIO.setup(B1,GPIO.OUT)
GPIO.setup(A2,GPIO.OUT)
GPIO.setup(B2,GPIO.OUT)

# Asignacion de velocidad del motor a pasos (seg)
esp = 0.001 # Correcto
# ____________________________________________________
# FUNCIONES
# *
# CONFIGURACION:
# Funcion de asignacion de senial de salidas
def setStp(stp1,stp2,stp3,stp4):
    GPIO.output(A1,stp1)
    GPIO.output(B1,stp2)
    GPIO.output(A2,stp3)
    GPIO.output(B2,stp4)
#*
# ADELANTE:
# Funcion de movimiento hacia adelante del motor
def adl(stp): # Recibe numero de pasos
    cnt = 0
    for i in range(0,stp):
        if(cnt == stp): #### 1
            break
        cnt = cnt + 1
        setStp(1,0,1,0)
        time.sleep(esp)
        if(cnt == stp): #### 2
            break
        cnt = cnt + 1
        setStp(0,1,1,0)
        time.sleep(esp)
        if(cnt == stp): #### 3
            break
        cnt = cnt + 1
        setStp(0,1,0,1)
        time.sleep(esp)
        if(cnt == stp): #### 4
            break
        cnt = cnt + 1
        setStp(1,0,0,1)
        time.sleep(esp)

# *
# ATRAS:
# Funcion de movimiento hacia atras del motor
def atr(stp): # Recibe numero de pasos
    cnt = 0
    for i in range(0,stp):
        if(cnt == stp): #### 1
            break
        cnt = cnt + 1
        setStp(1,0,0,1)
        time.sleep(esp)
        if(cnt == stp): #### 2
            break
        cnt = cnt + 1
        setStp(0,1,0,1)
        time.sleep(esp)
        if(cnt == stp): #### 3
            break
        cnt = cnt + 1
        setStp(0,1,1,0)
        time.sleep(esp)
        if(cnt == stp): #### 4
            break
        cnt = cnt + 1
        setStp(1,0,1,0)
        time.sleep(esp)

#*
# DESPLAZAMIENTO:
# Mueve la camara a la posicion deseada
def dsp(pscInc,pscFin): # Requiere posicion inicial y final
    stp = pscFin - pscInc
    if(pscFin < 0):
        time.sleep(0.5)
        setStp(0,0,0,0)
        return pscInc
#   #
    if(stp >= 0):
        adl(stp*2)
        time.sleep(0.5)
        setStp(0,0,0,0)
        return pscFin
    else:
        stp = stp * -1
        atr(stp*2)
        time.sleep(0.5)
        setStp(0,0,0,0)
        return pscFin

#*
# ____________________________________________________

# LOOP
#
"""while True:
    time.sleep(0.5)
    setStp(0,0,0,0)
    pscFin = raw_input("Posicion de destino: ") # 0 - 480
    pscFin = int(pscFin)
    pscInc = dsp(pscInc,pscFin)
    print "Ya estas peinado pa tras!"

"""
