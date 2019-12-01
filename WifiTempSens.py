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
from db_manager import database_engine
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
            #### Invio il messaggio di sveglia ####
            MESSAGE = sensTempCucina.wakeUpMsg    
            sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            sock.bind(("",UDP_PORT))
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            sock.settimeout(10.0)
            print("Aspetto il id sensore")
            data, addr = sock.recvfrom(1024)
            print(data)
            if data == sensTempCucina.sensId:
                print ("Id confermato - acquisisco temperatura")
                MESSAGE = "GetTemp"
                sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                sock.bind(("",UDP_PORT))
                sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
                data, addr = sock.recvfrom(1024)
                print(data)
                sensTempCucina.valore = float(data)
                print(addr[0])
                sensTempCucina.resetErrore()
            else:
                print ("Id non confermato")
                sensTempCucina.gestioneErrore()
        except socket.timeout:
            sock.settimeout(None)
            print("Time-out di comunicazione")
            sensTempCucina.gestioneErrore()
        #### Invio il messaggio di STOP ####
        MESSAGE = sensTempCucina.sleepMsg
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.bind(("",UDP_PORT))
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    elif selettore.indice == 15:
        print 'Qui salviamo tutto...'
        data_store.scriviTemperatura(sensTempCucina.valore*100,"cucina")
        data_store.salva_dati()
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
    sensTempCucina.wakeUpMsg = "cucinaSveglia"
    sensTempCucina.sleepMsg = "cucinaDormi"
    sensTempCucina.IpAdr = "10.0.1.10"
    sensTempCucina.sensId = "cucina"
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
#############################################################
#### INIZIALIZZAZIONE CONNESSIONA AL DATABASE DATA_STORE ####
#############################################################
try:
    print 'INIZIALIZZAZIONE CONNESSIONE AL DATABASE DATA_STORE'
    data_store = database_engine('/home/pi/dbFolder/data_store.db')
except Exception,e:
    print 'ERRORE NELLA INIZIALIZZAZIONE DEL DATABASE DEI TREND'
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









