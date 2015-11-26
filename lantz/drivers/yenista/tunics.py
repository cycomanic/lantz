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

    @Action(values=("ENABLE", "DISABLE"))
    def optical_output(self, value):
        self.query(value)

    @Action(values=("dBm", "mW"))
    def set_unit(self, value):
        self.query(value.upper())
    



        


    

