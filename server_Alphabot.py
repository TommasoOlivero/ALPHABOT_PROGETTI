#Creator: Coppola-Oliva
import RPi.GPIO as GPIO
import socket
import time as tm
import subprocess as sp
import sqlite3 as sq

con= sq.connect("DB_1.db")#dichiarazione lettore database
cur= con.cursor()#creazione cursore

class AlphaBot(object):
    
    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA  = 50
        self.PB  = 50

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()

    def left(self,tempo):
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        t=tm.time()
        t2=tm.time()+tempo
        while t< t2:
            t=tm.time()
        self.stop()

    def stop(self,t=0):
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def right(self,tempo):
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        t=tm.time()
        t2=tm.time()+tempo
        while t< t2:
            t=tm.time()
        self.stop()

    def forward(self,tempo, speed=30):
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        t=tm.time()
        t2=tm.time()+tempo
        while t< t2:
            t=tm.time()
        self.stop()

    def backward(self,tempo, speed=30):
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        t=tm.time()
        t2=tm.time()+tempo
        while t< t2:
            t=tm.time()
        self.stop()
        
    def set_pwm_a(self, value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def set_pwm_b(self, value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)    
        
    def set_motor(self, left, right):
        if (right >= 0) and (right <= 100):
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif (right < 0) and (right >= -100):
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if (left >= 0) and (left <= 100):
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif (left < 0) and (left >= -100):
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)

bot= AlphaBot() #dichiarazione bot globale

def curve(gradi): #Funzione per curve di gradi->gradi<0 sinistra,gradi>0 destra
    TEMPO=0.25
    time=abs(gradi*TEMPO/90)#proporzione in base ai gradi fatti per tempo
    if gradi < 0 :
        bot.left(time)
    else:
        bot.right(time)

def go(space):#Funzione per andare avanti con space> 0 e indietro <0
    SPAZIO=23.5
    time=abs(space)/SPAZIO#proporzione spazio-tempo
    if space < 0 :
        bot.backward(time)
    else:
        bot.forward(time)

def quad(space):#funzione per fare un quadrato
    go(space)
    curve(90)
    go(space)
    curve(90)
    go(space)
    curve(90)
    go(space)
    curve(90)

def main():
        print(sp.call(["vcgencmd", "get_throttled"]))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("0.0.0.0", 8000))
        s.listen()
        movimenti={"forward":bot.forward,"backward":bot.backward,"stop":bot.stop,"left":bot.left,"right":bot.right,"quit":s.close,"go":go,"curve":curve}#dizionario comandi
        connection, address= s.accept()#accettazione connessione
        print("ascolto")#messaggio informativo
        while(True):
            dati=connection.recv(4096)
            connection.sendall(dati)
            print(dati.decode())
            dati=dati.decode()
            dati=dati.split("|")
            if dati[0] in movimenti:#verifica che il comando sia presente nel dizionario
                movimenti[dati[0]](float(dati[1]))
                if dati== "quit":
                    break
            else:
                f=dati[0]#se il comando non è nel dizionario viene letto nel database
                res=con.execute(f"SELECT movimenti FROM COMANDI WHERE nome== \"{f}\"")#esecuzione comando sql
                comandi=res.fetchone()
                comandi=comandi[0]
                comandi=comandi.split(";")
                for comando in comandi:
                    comando=comando.split(",")
                    if comando[0] in movimenti:
                        movimenti[comando[0]](float(comando[1]))
                    if dati== "quit":
                        break
            
if __name__ == "__main__":
    main()


#19 - 1secondo
#90gradi - 0,34sec
