from myhdl import *


def def_alu(op1, op2, ctrl, res, z):
    """The ALU module
   
    Arguments:
        op1 : The first operand, 32 bits
        op2 : The second operand, 32 bits
        ctrl : The 4-bit ALU control
        res : The result(output) of the ALU operation, 32 bits
        z: signal zero result

    """
    @always_comb
    def alu():
        if ctrl == 0: #ctrl : 0000
            tres = op1 & op2
        elif ctrl == 1:   #ctrl : 0001
            tres = op1 | op2
        elif ctrl == 2:   #ctrl : 0010
            tres = op1 + op2
        elif ctrl == 6:   #ctrl : 0110
            tres = op1 - op2
        elif ctrl == 7:   #ctrl : 0111
            if op1 < op2:
                tres = 1
            else: tres = 0
        elif ctrl == 12:  #ctrl : 1100
            tres = ~(op1 | op2)
        # set the result
        res.next = tres

    @always_comb
    def zero_sig():
        """Set the zero bit to indicate a zero result.

        """
        if res == 0:
            z.next = 1
        else: z.next = 0 

    return alu, zero_sig
                
         
