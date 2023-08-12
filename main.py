from intcode import IntCodeCPU

def main():
    with open("BOOST.txt") as input:
        code = input.readline()

        amp_A = IntCodeCPU(0)
        amp_A.load_program(code)
        amp_B = IntCodeCPU(1)
        amp_B.load_program(code)
        amp_C = IntCodeCPU(2)
        amp_C.load_program(code)
        amp_D = IntCodeCPU(3)
        amp_D.load_program(code)
        amp_E = IntCodeCPU(4)
        amp_E.load_program(code)

        amp_A.run()

           

if __name__ == "__main__":
    main()