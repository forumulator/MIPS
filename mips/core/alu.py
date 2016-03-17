from myhdl import *


def def_alu(op1, op2, opcode, res, z):

    
    @always_comb
    def alu():
        if opcode == 0:
            tres = op1 & op2
        elif opcode == 1:
            tres = op1 | op2
        elif opcode == 2:
            tres = op1 + op2
        elif opcode == 6:
            tres = op1 - op2
        elif opcode == 7:
            if op1 < op2:
                tres = 1
            else: tres = 0
        elif opcode == 12:
            tres = ~(op1 | op2)
        res.next = tres

    @always_comb
    def zero_sig():
        
        if res == 0:
            z.next = 1
        else: z.next = 0 

    return alu, zero_sig
                
         
