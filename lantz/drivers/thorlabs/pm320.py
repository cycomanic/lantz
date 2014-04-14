from lantz import Feat
from lantz.drivers.usbtmc import USBTMCDriver
from lantz.drivers.ieee4882 import IEEE4882Driver

class PM320E(USBTMCDriver,IEEE4882Driver):
    """Thorlabs dual port  power meter"""
    name = "PM320E"
    idVendor = 0x1313
    idProduct = 0x8072

    def __init__(self, serial_number=None, **kwargs):
        super().__init__(self.idVendor, self.idProduct, serial_number, **kwargs)

    def GetError(self):
        return int(self.instrument.ask(':STAT:ERR:CND?'))

    def SetAveraging(self, avg, channel):
        """set averaging for channel 1/2"""
        try:
            self._Write(":AVER%d %d" %(channel, avg))
        except InstrumentException, detail:
            print "%s Error: %s" %(self.name, detail)

    def GetAveraging(self, channel):
        """get the averaging for channel 1/2"""
        try:
            return self._Ask(":AVER%d:VAL?"%channel)
        except InstrumentException, detail:
            print "%s Error: %s" %(self.name, detail)

    def GetPower(self, channel):
        """get the measured power value"""
        self._Write(':Meas:init%d'%channel)
        while int(self._Ask(':Meas:check%d?'%channel)):
            pass
        return float(self._Ask(":Fetch:Pow%d:Val?"%channel))
        
#        try:
 #           return float(self._Ask(":POW%d:VAL?"%channel))
  #      except InstrumentException, detail:
   #         print "%s Error: %s" %(self.name, detail)
 
    def SetWavelength(self, wl, channel):
        """set the wavelength to a value in nm"""
        try:
            self._Write(":WAVE%d %d" %(channel,wl))
        except InstrumentException, detail:
            print "%s Error: %s" %(self.name, detail)
 
    def GetWavelength(self, channel):
        """get the measurement wavelength in nm"""
        try:
            return int(self._Ask(":WAVE%d:VAL?"%channel))
        except InstrumentException, detail:
            print "%s Error: %s" %(self.name, detail)
 

class PM100(LabInstrument):
    """Thorlabs single port power meter"""
    name = 'PM100'
    def __init__(self, fulladdress, timeout=20):
        super(PM100, self).__init__(fulladdress=fulladdress, timeout=timeout)

    def GetError(self):
        return 0 #return int(self.instrument.ask(":ERROR?"))

    def GetID(self):
        return self._Ask('*IDN?')

    def SetAveraging(self, avg):
        try:
            self._Write(":AVERAGE:COUNT %d"%avg)
        except InstrumentException, detail:
            print "%s Error: %s" %(self.name, detail)

    def GetAveraging(self):
        return int(self._Ask(":AVERAGE:COUNT?"))

    def SetUnit(self, unit):
        self._Write(":POW:UNIT %s"%unit)

    def GetUnit(self):
        return self._Ask(":POW:UNIT?")

    def GetPower(self):
        self._Write(":MEASURE:POW")
        return float(self._Ask("READ?"))
    
    def SetWavelength(self, wl):
        self._Write(':corr:wav %f'%wl)
    
    def GetWavelength(self):
        return self._Ask(':corr:wav?')
        
