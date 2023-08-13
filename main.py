from intcode import IntCodeCPU

with open("input_7.txt") as input:
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


def run_all_amplifiers(initial_signal, phase_A, phase_B, phase_C, phase_D, phase_E):
    amp_A.input_queue.put(phase_A)
    amp_A.input_queue.put(initial_signal)
    amp_A.run()

    amp_B.input_queue.put(phase_B)
    amp_B.input_queue.put(amp_A.output_value)
    amp_B.run()
        
    amp_C.input_queue.put(phase_C)
    amp_C.input_queue.put(amp_B.output_value)
    amp_C.run()

    amp_D.input_queue.put(phase_D)
    amp_D.input_queue.put(amp_C.output_value)
    amp_D.run()

    amp_E.input_queue.put(phase_E)
    amp_E.input_queue.put(amp_D.output_value)
    amp_E.run()  

    return amp_E.output_value   


def main():
    print(run_all_amplifiers(0, 0, 1, 2, 3, 4))
 
        



if __name__ == "__main__":
    main()