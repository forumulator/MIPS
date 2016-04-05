from myhdl import Signal, intbv, Simulation, StopSimulation, delay, instance, always_comb

import random
from random import randrange


def sign_extend(val_in, val_out):
    """The sign-extend from 16 bit to 32 bit signals

    Sign extends from 16 to 32 bit in the 2's complement form. Currently deals with
    unsigned intbv signals.

    Arguments:
        val_in : IN the 16-bit input
        val_out : OUT the 32-bit sign extended output 
    """

    @always_comb
    def logic():
        if (val_in[15] == True):
            a = (intbv((1 << 32) - 1)[32:16]) << 16
        else:
            a = intbv(0)[32:]

        val_out.next = val_in + a

    return logic       


# to check the 2's complement version of an unsigned int
def two_c(num, bits = 16):
    test = min(num, (1 << bits) - num)
    if (test == num):
        return test
    else:
        return -test


def test_extend():

    val_out = Signal(intbv(32))
    val_in = Signal(intbv(16))

    inst = sign_extend(val_in, val_out)

    @instance
    def tb_dut():

        for ii in range(50):

            rand = randrange(2**16)
            val_in.next = rand
            yield delay(10)

            exrand = val_out

            assert two_c(rand) == two_c(exrand, 32)
        raise StopSimulation

    sim = Simulation(inst, tb_dut)
    sim.run()


