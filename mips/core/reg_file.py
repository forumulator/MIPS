from myhdl import Signal, delay, intbv, always, always_seq, Simulation, ResetSignal, instance, StopSimulation
import random
from random import randrange


def register_file(read_addr1, read_addr2, write_addr, write_data, read_data1, read_data2, write_ctrl, clock, reset, size = 32):
    """The definition of the register file.

    The register file for single cycle MIPS contains of 32
    32 bit registers, each addressable for read and write. Reading 
    and writing are done on the negative edge, so as to not clash with
    other ops.

    Arguments:
        read_addr1 : The read address for the first read signal
        read_addr2 : The read address for the second read signal
        write_addr : IN write address
        write_data : IN the data to be written to the register specified by write_addr
        read_data1 : OUT the data read from the register specified by read_addr1
        read_data2 : OUT the data read from the register specified by read_addr2
        write_ctrl : IN the control signal for the write. 1 for true.
        clock, reset : clock and the reset signals
        size : sizeof the file, by default it is 32 for the single cycle implementation

    """
   
    file_array = [Signal(intbv(0, min = -2**32, max= 2**32 - 1)) for i in range(size)]
    
    @always_seq(clock.negedge, reset = reset)
    def regfile_ops():
        # reads
        read_data1.next = file_array[read_addr1]
        read_data2.next = file_array[read_addr2]

        #write
        if (write_ctrl == True):
            file_array[write_addr].next = write_data
           

    return regfile_ops


def test_regfile():

    clk = Signal(bool(0))
    reset = ResetSignal(0, active=bool(1), async=True)

    size = 32

    read_addr1, read_addr2 = Signal(intbv(0)[5:]), Signal(intbv(0)[5:])
    write_addr = Signal(intbv(0)[5:])
    write_data = Signal(intbv(0, min=-2**32, max=2**32-1)) 
    read_data1, read_data2 = Signal(intbv(0, min=-2**32, max=2**32-1)), Signal(intbv(0, min=-2**32, max=2**32-1)) 

    write_ctrl = Signal(bool(0))

    reg_file = register_file(read_addr1, read_addr2, write_addr, write_data, read_data1, read_data2, write_ctrl, clk, reset, size)

    @always(delay(10))
    def tb_clk():
        clk.next = not clk

    @instance
    def tb_dut():

        for jj in range(100):
            wrlist = []

            yield clk.posedge
            # Write random data
            for ii in range(32):
                dwrite = randrange(-2**32,2**32-1)

                wrlist.append(dwrite)
                write_addr.next = ii
                write_data.next = dwrite
                write_ctrl.next = True
                yield clk.posedge


            write_ctrl.next = False

            yield clk.posedge
            # Verify written data        
            for ii in range(32):
                read_addr1.next = ii
                randread = randrange(32)
                read_addr2.next = randread
                yield clk.posedge
                
                assert read_data1 == wrlist[ii]
                assert read_data2 == wrlist[randread]

        raise StopSimulation

    sim = Simulation(tb_clk, tb_dut, reg_file)
    sim.run()


   


if __name__ == '__main__':
    
    tb_inst = test_regfile()
    sim = Simulation(tb_inst)
    sim.run()  


