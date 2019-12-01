#### Temperature sensor class ####
class temperatureSensor:

    def __init__(self):
        self.value      = 0
        self.OldValue   = 0
        self.IpAdr      = ""
        self.UdpPort    = 64123
        self.nFailConn  = 0
        self.wakeUpMsg  = ""
        self.sleepMsg   = ""
        self.sensId     = ""
        self.maxTimeOut = 3
        self.numOfErr   = 0
        self.commErr    = False
    
    def gestioneErrore(self):
        self.numOfErr = self.numOfErr + 1
        if self.numOfErr >= self.maxTimeOut:
            self.commErr = True
    
    def resetErrore(self):
        if self.numOfErr != 0:
            self.numOfErr = 0
        if self.commErr:
            self.commErr = False