from myhdl import *



def def_ctrl(alu_op, funct, alu_ctrl):
    """The ALU control module
    
    Takes in a 2-bit ALUop and the 6-bit funct code
    and generates the 4-bit ALU control input.

    Arguments:
        alu_op : IN The 2-bit ALUop
        funct : IN 6-bit function code
        alu_ctrl : OUT generated ALU control signal.
    """
    @always_comb
    def ctrl():
        if alu_op == 0:         #00,xxxxxx,0010
            tctrl = 2
        elif alu_op == 1:
            tctrl = 6           #01,xxxxxx,0110
        elif alu_op == 2:
            if funct == 32:
                tctrl = 2       #10,100000,0010
            elif funct == 34:
                tctrl = 6       #10,100010,0110
            elif funct == 36:
                tctrl = 0       #10,100100,0000
            elif funct == 37:
                tctrl = 1       #10,100101,0001
            elif funct == 42:
                tctrl = 7       #10,101010,0111
        alu_ctrl.next = tctrl

    return ctrl
