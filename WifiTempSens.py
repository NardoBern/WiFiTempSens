########################################
#### IMPORTAZIONE LIBRERIE E CLASSI ####
########################################
from threading import Timer
import time
import socket
from time import sleep
import sys
import site
site.addsitedir(sys.path[0]+'/lib')
site.addsitedir(sys.path[0]+'/class')
site.addsitedir(sys.path[0]+'/modules')
from temperatureSensor import temperatureSensor
from cadenziatore import cadenziatore
###############################
#### IMPOSTAZIONE COSTANTI ####
###############################

#########################################
#### FUNZIONE DI INTERRUPT AD 1 MIN. ####
#########################################
def oneMinFunction():
    selettore.indice = selettore.indice + 1
    print 'Il valore del indice:'
    print selettore.indice
    if selettore.indice == 1:
        UDP_PORT = sensTempCucina.UdpPort
        UDP_IP = sensTempCucina.IpAdr
        try:
            MESSAGE = sensTempCucina.wakeUpMsg    
            sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            sock.bind(("",UDP_PORT))
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            sock.settimeout(10.0)
            print("Aspetto dei dati")
            data, addr = sock.recvfrom(1024)
            print(data)
        except socket.timeout:
            sock.settimeout(None)
            print("Time-out di comunicazione")
        MESSAGE = "STOP"
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.bind(("",UDP_PORT))
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    elif selettore.indice == 15:
        print 'Qui salviamo tutto...'
        print 'Resetto il indice'
        selettore.indice = 0
    print 'INTERRUPT ad 1 Min.'
    t = Timer(1.0,oneMinFunction)
    t.start()

###################################
#### CICLO DI INIZIALIZZAZIONE ####
###################################
try:
    print "Inizializzazione sensore temperatura cucina"
    sensTempCucina = temperatureSensor()
    sensTempCucina.wakeUpMsg = "sveglia"
    sensTempCucina.IpAdr = "10.0.1.108"
except Exception,e:
    print ("Errore inizializzazione sensore temperatura cucina: ",e)

#######################################
#### INIZIALIZZAZIONE CADENZIATORE ####
#######################################
try:
    print 'INIZIALIZZAZIONE CADENZIATORE'
    selettore = cadenziatore()
    selettore.inizializzazione()
except Exception,e:
    print 'ERRORE NELLA INIZIALIZZAZIONE DEL CADENZIATORE'
    print e
####################################################
#### INIZIALIZZAZIONE TIMER INTERRUPT AD 1 MIN. ####
####################################################
try:
    print 'INIZIALIZZAZIONE ONE MINUTE INTERRUPT'
    t = Timer(1.0,oneMinFunction)
    t.start()
except:
    print 'ERRORE NELLA INIZIALIZZAZIONE DEL TIMER DI INTERRUPT'
    t.cancel()
print 'FINE CICLO DI INIZIALIZZAZIONE'









