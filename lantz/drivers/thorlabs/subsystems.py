from lantz import Feat, Action, Driver

def _convert_bitmask(inp, maskdict):
    set_flags = {}
    for k, v in maskdict.items():
        if inp&v != 0:
            set_flags[k] = True
        else:
            set_flags[k] = False
    return set_flags


measure_types = ['power', 'current', 'voltage', 'energy',
            'frequency', 'pdensity', 'edensity', 'resistence'
            'temperature']

class SubDriver(object):
    def __getattr__(self, name):
        if name[0] = '_':
            return self.parent.name


class System(SubDriver):
    """System subsystem commands for Thorlabs PM100 optical power meter"""

    @Feat()
    def error(self):
        """Returns the latest error code message"""
        return self.parent.query("SYSTem:ERRor?")

    @Feat()
    def version(self):
        """Query level of SCPI standard (1999.0)"""
        return self.parent.query("SYSTem:VERSion?")

    @Feat(values=set((50, 60)))#, units='Hz')
    def lfrequency(self):
        """The instrument's line frequency can be 50 or 60 Hz"""
        return int(self.parent.query("SYSTem:LFRequency?"))

    @lfrequency.setter
    def set_lfrequency(self, value):
        """Set the instrument's line frequency can be 50 or 60 Hz"""
        self.parent.query("SYSTem:LFRequency {:d}".format(int(value)))
   
    @Feat()
    def sensor(self):
        """Information about the connected sensor. The response consists of the
        following fields:
        sensor name             [string]
        sensor serial number    [string]
        calibration message     [string]
        sensor type             [float]
        sensor subtype          [float]
        flags                   [dict]
        """
        
        flag_dict = {'Is power sensor': 1,
                'Is energy sensor': 2,
                'Response settable':16,
                'Wavelength settable': 32,
                'Tau settable':64,
                'Has temperatur sensor':256}
        ret = self.parent.query("SYSTem:SENSor:IDN?")
        ret = ret.split(',')
        flags = _convert_bitmask(int(ret[5]), flag_dict)
        retdict = { 'name': ret[0],
                    'sn': ret[1],
                    'cal_msg': ret[2],
                    'type': float(ret[3]),
                    'subtype': float(ret[4]),
                    'flags': flags
                    }
        return retdict

class Sense(SubDriver):

    @Feat(limits=(9999999999,))
    def average(self):
        return int(self.parent.query("SENSe:AVERage:COUNt?"))

    @average.setter
    def setaverage(self, value):
        self.parent.send("SENSe:AVERage:COUNt {:d}".format(int(value)))

class Measurement(SubDriver):
    """Measurement subsystem commands for Thorlabs PM100 optical power meter"""

    @Action()
    def initiate(self):
        self.parent.send('INITiate:IMMediate')

    @Action()
    def abort(self):
        self.parent.send('ABORt')

    #@quantity.setter
    #def quantity(self, value):
        #if value not in self.measure_types:
            #raise ValueError()
        #self.parent.send('CONFigure:{:s}'.format(value))

    @Feat()
    def fetch(self):


