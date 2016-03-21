from myhdl import *
import random
from random import randrange

from .alu import def_alu
from .ctrl import def_ctrl

random.seed(4)

def test_ctrl():
    """Test bench for the ALU control.
    
    """
    clk = Signal(bool(0))
    reset = ResetSignal(0, active=1, async=True)

    alu_op = Signal(intbv(0)[2:])
    funct = Signal(intbv(0)[6:])
    alu_ctrl = Signal(intbv(0)[4:])
    alu_op1 = Signal(intbv(0, min=-2**32, max=2**32))
    alu_op2 = Signal(intbv(0, min=-2**32, max=2**32))
    alu_res = Signal(intbv(0, min=-2**32, max=2**32))
    alu_z = Signal(bool(0))

    ctrl_inst = def_ctrl(alu_op, funct, alu_ctrl)
    alu_inst = def_alu(alu_op1, alu_op2, alu_ctrl, alu_res, alu_z)

    @always(delay(10))
    def tb_clk():
        clk.next = not clk

    @instance
    def tb_ctrl():
        oplist = [0,1,2]    # 2bit : [00,01,10]
        functlist = [32,34,36,37,42] #[100000,100010,100100,100101,101010]
        for ii in range(100):
            r_op = oplist[randrange(3)]
            r_func = functlist[randrange(5)]
            op1, op2 = randrange(-2**31, 2**31), randrange(-2**31, 2**31)
            
            if (r_op == 0):
                res = op1 + op2
            elif r_op == 1:
                res = op1 - op2
            elif r_op == 2:
                if r_func == 32:
                    res = op1 + op2
                elif r_func == 34:
                    res = op1 - op2
                elif r_func == 36:
                    res = op1 & op2
                elif r_func == 37:
                    res = op1 | op2
                elif r_func == 42:
                    if op1 < op2:
                        res = 1
                    else: res = 0
                        
            alu_op.next = r_op
            funct.next = r_func
            alu_op1.next,alu_op2.next = op1, op2           
           
            yield delay(10)
            assert res == alu_res

            if res == 0:
                assert alu_z == 1
        raise StopSimulation

    # run simulation on test bench
    sim = Simulation(ctrl_inst, alu_inst, tb_clk, tb_ctrl)
    sim.run()


