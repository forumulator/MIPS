from myhdl import *

import random
from random import randrange

random.seed(3)

def mux2(in_1, in_2, out, ctrl):
    """The definition of a 2 to 1 bit mux, with a 1 bit ctrl.

    """

    @always_comb
    def mux():
        if (ctrl == 0):
            out.next = in_1
        elif (ctrl == 1):
            out.next = in_2
    return mux


def mux4(in_1, in_2, in_3, in_4, out, ctrl):
    """The definition of a 4 to 1 bit mux, with a 2 bit ctrl.

    """

    @always_comb
    def mux():
        if (ctrl == 0):
            out.next = in_1
        elif (ctrl == 1):
            out.next = in_2
        elif (ctrl == 2):
            out.next = in_3
        elif (ctrl == 3):
            out.next = in_4
    return mux


def test_mux():

    in_sig = [Signal(bool(0)) for i in range(4)]

    out2 = Signal(bool(0))
    out4 = Signal(bool(0))

    ctrl2 = Signal(bool(0))
    ctrl4 = Signal(intbv(0)[2:])

    inst2 = mux2(in_sig[0], in_sig[1], out2, ctrl2)
    inst4 = mux4(in_sig[0], in_sig[1], in_sig[2], in_sig[3], out4, ctrl4)

    @instance
    def tb_dut():
        
        for ii in range(100):
            ls = [bool(randrange(2)) for i in range(4)]

            for i in range(4):
                in_sig[i].next = ls[i]
            
            ctrl2.next = randrange(2)
            ctrl4.next = randrange(4)

            yield delay(10)

            assert out2 == ls[ctrl2]
            assert out4 == ls[ctrl4]


    sim = Simulation(inst2, inst4, tb_dut)
    sim.run()