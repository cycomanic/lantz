# -*- coding: utf-8 -*-
"""
    lantz.drivers.yenista.tunics
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements the driver for Yenista Tunics ECL laser

    :copyright: 2015 by Lantz Authors, see AUTHORS for more details
    :licence: BSD, see LICENSE for more details

"""

from pyvisa import constants
from lantz import Feat, Action
from lantz.errors import InstrumentError
from lantz.messagebased import MessageBasedDriver


class  T100SHP(MessageBasedDriver):
    """Tunics T100S-HP High Power Tunable Laser
    """
:
    DEFAULTS = {'ASRL': {'write_termination': '\r',
                         'baud_rate': 9600,
                         'data_bits': 8,
                         'parity': constants.Parity.none,
                         'stop_bits': constants.StopBits.one,
                         'encoding': 'ascii',
                         'read_termination': '\r> '},
                'GPIB': {'write_termination': '\n'}
                }

    def query(self,  command, *, send_args=(None, None), recv_args=(None, None)):
        answer = super().query(command, send_args=send_args, recv_args=recv_args)
        return answer

    # General system control
    @Feat()
    def idn(self):
        return self.query("*IDN?")

    @Action()
    def init(self):
        return self.query("INIT")

    # Calibration control

    @Action()
    def auto_cal(self):
        ret = self.query("AUTO_CAL")
        if ret.upper() == "REFERENCING ERROR":
            raise InstrumentError

    @Feat(units='mW', limits=(0.3, 0.6))
    def pcal1(self):
        """The first power value (in mW) of the two-point power calibration method.
        """
        return float(self.query("PCAL1?"))

    @pcal1.setter()
    def pcal1(self, value):
        self.query("PCAL1={:.2f}".format(value))

    @Feat(units='mW', limits=(0.3, 0.6))
    def pcal2(self):
        """The first power value (in mW) of the two-point power calibration method.
        """
        return float(self.query("PCAL2?"))

    @pcal2.setter()
    def pcal2(self, value):
        self.query("PCAL2={:.2f}".format(value))

    @Action(values={True: "ENABLE", False: "DISABLE"})
    def output(self, value):
        self.query(value)

    @Action(values=("dBm", "mW"))
    def set_unit(self, value):
        self.query(value.upper())

    #control the output power
    @Feat()
    def power(self):
        return float(self.query("P?"))

    @power.setter
    def power(self, value):
        self.query("P={:.2f}".format(value))

    @Feat(unit="mA", limit=(0, 400))
    def current(self):
        return float(self.query("I?"))

    @current.setter
    def current(self, value):
        self.query("I={:.1f}".format(value))

    # control the wavelength or frequency

    @Feat(unit="nm")
    def wavelength(self):
        return float(self.query("L?"))

    @wavelength.setter
    def wavelength(self, value):
        self.query("L={:.3f}".format(value))

    @Feat(unit="nm")
    def wavelength_max(self):
        return float(self.query("L? MAX"))

    @Feat(unit="nm")
    def wavelength_min(self):
        return float(self.query("L? MIN"))

    @Feat(unit="GHz")
    def frequency(self):
        return float(self.query("F?"))

    @frequency.setter
    def frequency(self, value):
        self.query("F={:.1f}".format(value))

    @Feat(unit="GHz")
    def frequency_max(self):
        return float(self.query("F? MAX"))

    @Feat(unit="GHz")
    def frequency_min(self):
        return float(self.query("F? MIN"))

    @Feat(unit="nm/s")
    def motorspeed(self):
        return float(self.query("MOTOR_SPEED?"))

    @motorspeed.setter
    def motorspeed(self, value):
        self.query("MOTOR_SPEED={:03d}".format(value))

    @Feat(unit="pm", limits=(0,99.9, 0.1))
    def finescan_wavelength(self, value):
        self.query("FSCL={:.1f%}".format(value))

    @Feat(unit="GHz", limits=(0,9.99, 0.01))
    def finescan_frequency(self, value):
        self.query("FSCF={:.1f%}".format(value))

    @Action(values={True: "CTRLON", False: "CTRLOFF"})
    def coherencecontrol(self, value):
        self.query(value)
    
    @Action(values={True: "ACTCTRLON", False: "ACTCTRLOFF"})
    def activecavitycontrol(self, value):
        self.query(value)

    def continuous_sweep(self, power, wl_start, wl_end, motor_speed, Nscans):
        self.power = power
        for i in range(Nscans):
            self.wavelength = wl_start
            self.motorspeed = motor_speed
            self.activecavitycontrol = True
            self.wavelength = wl_stop
            self.motorspeed = 100
            self.activecavitycontrol = False



