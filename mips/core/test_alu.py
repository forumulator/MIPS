from myhdl import *
import pytest
from .alu import def_alu
import random
from random import randrange

random.seed(3)

def test_alu():

    clk = Signal(bool(0))
    reset = ResetSignal(0, active=1, async=True)

    op1, op2 = Signal(intbv(0, min=-2**32, max=2**32)), Signal(intbv(0, min=-2**32, max=2**32))
    alu_op = Signal(intbv(0)[4:])
    alu_z = Signal(bool(0))
    alu_res = Signal(intbv(0, min=-2**32, max=2**32))
        
    alu_inst = def_alu(op1, op2, alu_op, alu_res, alu_z)

    @always(delay(10))
    def tb_clk():
        clk.next = not clk
  
    @instance  
    def tb_alu():
        for ii in range(100):
            op_list = [0,1,2,6,7,12]
            r_op = op_list[randrange(6)]
            r_o2 = randrange(-2**31,2**31)
            r_o1 = randrange(-2**31,2**31)
            #print(r_o1,r_o2,r_op,ii)
            # manually operate on the integers
            if r_op == 0:
                res = r_o1 & r_o2
            elif r_op == 1:
                res = r_o1 | r_o2
            elif r_op == 2:
                res = r_o1 + r_o2
            elif r_op == 6:
                res = r_o1 - r_o2
            elif r_op == 7:
                if r_o1 < r_o2:
                    res = 1
                else: res = 0
            elif r_op == 12:
                res = ~(r_o1 | r_o2)
            
            op1.next, op2.next = r_o1, r_o2
            alu_op.next = r_op
            yield clk.posedge
            if (res >= -2**32 and res < 2**32):     
                assert res == alu_res
            if (res == 0):
                assert alu_z == 1
        raise StopSimulation

    sim = Simulation(alu_inst, tb_clk, tb_alu)
    sim.run()
                            

