#### Temperature sensor class ####
class temperatureSensor:

    def __init__(self):
        self.value      = 0
        self.OldValue   = 0
        self.IpAdr      = ""
        self.UdpPort    = 64123
        self.nFailConn  = 0
        self.wakeUpMsg  = ""
        self.sensId     = ""
        self.maxTimeOut = 3 