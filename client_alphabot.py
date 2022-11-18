#ALPHABOT CLIENT
#creator: Coppola Carmine Mattia & Olivero Tommaso

import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

s.connect(("192.168.0.135", 8000))  #IP SERVER

def main():
    
    while True:
        messaggio = input("COMANDO: ") # input comando utente

        if messaggio == "stop":         # in caso fosse inserito "stop" non si richiede il valore secondario e si ferma l'alphabot
            messaggio += "|0"
        else:
            tempo = input("VALORE: ")   # richiesta valore secondatrio
            messaggio += "|" + tempo

        s.sendall(messaggio.encode())   # invio comando

        if messaggio == "quit" or messaggio == "q" or messaggio == "QUIT" or messaggio == "Q":  # comando per fermare l'ALPHABOT in caso di "emergenza"
            break
        
    s.close()

if __name__ == "__main__":  # richiamo al main
    main()

# 19 cm : 1 s 
# R_90° : 0.34 s
# L_90° : 0.34 s