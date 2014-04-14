from lantz import Feat, Action
from lantz import Driver
from lantz.drivers.usbtmc import USBTMCDriver
from lantz.drivers.ieee4882 import IEEE4882Driver
from .import subsystems

class PM100(IEEE4882Driver,USBTMCDriver):
    """Thorlabs single port power meter"""
    name = 'PM100'
    _idVendor = 0x1313
    _idProduct = 0x8072
    def __init__(self, serial_number=None, **kwargs):
        super().__init__(self._idVendor, self._idProduct, serial_number, **kwargs)
        self.measurement = subsystems.Measurement(self)
        self.system = subsystems.System(self)

    @Feat()
    def calibration(self):
        """Human readable calibration string"""
        return self.query("CALibration:STRing?")

    def GetError(self):
        return 0 #return int(self.instrument.ask(":ERROR?"))


    def SetAveraging(self, avg):
        try:
            self._Write(":AVERAGE:COUNT %d"%avg)
#        except InstrumentException, detail:
        except:
            print("%s Error: %s" %(self.name, detail))

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
        
