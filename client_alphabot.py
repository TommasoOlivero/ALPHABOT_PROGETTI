#ALPHABOT CLIENT
#creator: Coppola Carmine Mattia & Olivero Tommaso

import socket
import time
import pygame as pg

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stringa = ""
pg.init()
screen = pg.display.set_mode((10, 10))

s.connect(("192.168.0.135", 8000))  #INSERIRE IP SERVER

def main():
    while True:
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:#Legge quali tasti sono premuti e invia un messaggio di conseguenza
                if event.__dict__["unicode"]=="w":#Avanti
                    messaggio="g|10"
                    s.sendall(messaggio.encode())
                    time.sleep(0.3)
                if event.__dict__["unicode"]=="d" :#Gira a destra
                    messaggio="c|50"
                    s.sendall(messaggio.encode())
                    time.sleep(0.3)
                if event.__dict__["unicode"]=="a" :#Gira a sinistra
                    messaggio="c|-50"
                    s.sendall(messaggio.encode())
                    time.sleep(0.3)
                if event.__dict__["unicode"]=="s":#Indietro
                    messaggio="g|10"
                    s.sendall(messaggio.encode())
                    time.sleep(0.3)
    s.close()

if __name__ == "__main__":# richiamo al main
    main()

# 19 cm : 1 s ---> 
# R_90° : 0.34 s --->
# L_90° : 0.34 s --->